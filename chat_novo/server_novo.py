import socket
import threading
import sys
import queue
import os
import shutil
import textwrap
from datetime import datetime

# Ativa suporte a códigos ANSI no terminal do Windows se necessário
os.system('')

HOST = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001

clientes = {}            # socket → {"nick": str, "ip": str}
cores_clientes = {}      # nick → código de cor ANSI
server_in_chat = True    # servidor participa do chat?
lock = threading.RLock()        # RLock reentrante para evitar deadlock interno
print_lock = threading.RLock()  # RLock reentrante para impressões no terminal
MAX_USERS = 10
running = True           # controla encerramento total
input_queue = queue.Queue()  # Fila para comandos do servidor


# Cores ANSI
RESET = '\033[0m'
AMARELO = '\033[93m'    # Servidor
CIANO = '\033[96m'      # Padrão clientes
VERDE = '\033[92m'      # Comandos / Entradas / Saídas
VERMELHO = '\033[91m'   # Erros
ROXO = '\033[95m'       # Timestamps

# Paleta de cores distintas para atribuir a cada usuário conectado
CORES_USUARIOS = [
    '\033[96m',  # Ciano brilhante
    '\033[94m',  # Azul brilhante
    '\033[33m',  # Âmbar / Laranja
    '\033[36m',  # Ciano suave
    '\033[35m',  # Magenta suave
    '\033[97m',  # Branco brilhante
    '\033[34m',  # Azul suave
    '\033[32m',  # Verde escuro
    '\033[95m',  # Magenta brilhante
    '\033[37m',  # Cinza claro
]


def get_cor_usuario(nick):
    """Garante que cada usuário conectado receba uma cor exclusiva e diferente."""
    with lock:
        if nick not in cores_clientes:
            cores_em_uso = set(cores_clientes.values())
            disponiveis = [c for c in CORES_USUARIOS if c not in cores_em_uso]
            if disponiveis:
                cores_clientes[nick] = disponiveis[0]
            else:
                cores_clientes[nick] = CORES_USUARIOS[len(cores_clientes) % len(CORES_USUARIOS)]
        return cores_clientes[nick]


def liberar_cor_usuario(nick):
    """Libera a cor de um usuário quando ele sai do chat."""
    with lock:
        cores_clientes.pop(nick, None)


def get_terminal_width():
    """Retorna a largura atual do terminal."""
    try:
        w = shutil.get_terminal_size((80, 20)).columns
        return w if w > 20 else 80
    except Exception:
        return 80


def get_timestamp():
    """Retorna timestamp formatado."""
    return datetime.now().strftime("%H:%M:%S")


def formatar_direita(prefixo_sem_cor, msg, cor_msg=AMARELO):
    """
    Formata mensagem enviada pelo próprio servidor no lado direito (estilo WhatsApp).
    prefixo_sem_cor: ex. '[14:20:10] [Servidor]: '
    """
    largura = get_terminal_width()
    margem = 2  # Evita quebra automática de linha na margem direita
    
    max_bubble = max(25, int(largura * 0.65))
    h_len = len(prefixo_sem_cor)
    content_width = max(15, max_bubble - h_len)
    
    lines = textwrap.wrap(msg, width=content_width)
    if not lines:
        lines = ['']
        
    formatted_lines = []
    
    # Se o prefixo contiver timestamp '[HH:MM:SS] '
    if prefixo_sem_cor.startswith("[") and len(prefixo_sem_cor) > 10 and prefixo_sem_cor[9] == "]":
        timestamp_part = prefixo_sem_cor[:11]
        resto_prefixo = prefixo_sem_cor[11:]
        l1_color = f"{ROXO}{timestamp_part}{RESET}{cor_msg}{resto_prefixo}{lines[0]}{RESET}"
    else:
        l1_color = f"{cor_msg}{prefixo_sem_cor}{lines[0]}{RESET}"
        
    l1_clean = f"{prefixo_sem_cor}{lines[0]}"
    formatted_lines.append((l1_color, len(l1_clean)))
    
    pad = " " * h_len
    for l in lines[1:]:
        l_color = f"{cor_msg}{pad}{l}{RESET}"
        l_clean = pad + l
        formatted_lines.append((l_color, len(l_clean)))
        
    block_width = max(v_len for _, v_len in formatted_lines)
    indent = max(0, largura - block_width - margem)
    
    return "\n".join(" " * indent + l_col for l_col, _ in formatted_lines)


def print_server(msg, color=AMARELO, align_right=False):
    """
    Print com suporte a alinhamento:
    - align_right=True: para mensagens enviadas pelo próprio servidor (lado direito).
    - align_right=False: para mensagens de outros clientes e logs de sistema (lado esquerdo).
    """
    with print_lock:
        # Limpa linha de prompt atual
        sys.stdout.write('\r\033[K')
        timestamp = get_timestamp()
        
        if align_right:
            bubble = formatar_direita(f"[{timestamp}] [Servidor]: ", msg, cor_msg=color)
            sys.stdout.write(bubble + "\n")
        elif "\n" in msg:
            sys.stdout.write(f"{color}{msg}{RESET}\n")
        else:
            sys.stdout.write(f"{ROXO}[{timestamp}]{RESET} {color}{msg}{RESET}\n")
            
        sys.stdout.write(f"{AMARELO}[Servidor]: {RESET}")
        sys.stdout.flush()


def broadcast(msg, origem=None):
    """Envia mensagem para todos os clientes, exceto o 'origem'."""
    with lock:
        for c in list(clientes.keys()):
            if c != origem:
                try:
                    c.sendall(msg.encode("utf-8"))
                except OSError:
                    # Conexão fechada, será tratada no finally de tratar_cliente
                    pass


def listar_usuarios():
    lista = "\n--- Usuários conectados ---\n"
    with lock:
        for c, info in clientes.items():
            cor = get_cor_usuario(info['nick'])
            lista += f"  • {cor}{info['nick']}{RESET} ({info['ip']})\n"
        if len(clientes) == 0:
            lista += "  (nenhum usuário conectado)\n"
    return lista


def ajuda_texto():
    sep = "=" * 60
    return (
        f"\n{sep}\n"
        "COMANDOS DISPONÍVEIS NO SERVIDOR\n"
        f"{sep}\n\n"
        "  ajuda (ou /ajuda)          - Mostra esta lista de comandos\n"
        "  usuarios (ou /usuarios)    - Lista todos os clientes conectados\n"
        "  kick <nick>                - Desconecta um usuário pelo nickname\n"
        "  sair (ou /sair)            - Sai do chat (modo gerenciamento ativo)\n"
        "  entrar (ou /entrar)        - Volta a participar ativamente do chat\n"
        "  encerrar (ou /encerrar)    - Derruba todos os clientes e fecha o servidor\n"
        f"\n{sep}\n"
    )


def ajuda_cliente_texto():
    sep = "=" * 50
    return (
        f"\n{sep}\n"
        "COMANDOS DISPONÍVEIS NO CHAT\n"
        f"{sep}\n\n"
        "  usuarios (ou /usuarios)    - Lista todos os usuários conectados\n"
        "  ajuda (ou /ajuda)          - Mostra esta lista de comandos\n"
        "  sair (ou /sair)            - Sai do chat e encerra sua conexão\n"
        f"\n{sep}\n"
    )


def expulsar(nick):
    encontrado = False
    with lock:
        for c, info in list(clientes.items()):
            if info["nick"] == nick:
                try:
                    c.sendall("Você foi expulso do chat.\n".encode("utf-8"))
                except OSError:
                    pass
                del clientes[c]
                c.close()
                encontrado = True
                break
    
    if encontrado:
        liberar_cor_usuario(nick)
        broadcast(f"[{get_timestamp()}] [Servidor]: {nick} foi expulso.\n")
    
    return encontrado


def tratar_cliente(sock, address):
    global running

    try:
        sock.sendall("Digite seu nickname: ".encode("utf-8"))
        nick = sock.recv(1024).decode("utf-8").strip()

        if not nick:
            sock.close()
            return

        with lock:
            if len(clientes) >= MAX_USERS:
                sock.sendall("Chat cheio (máx 10 usuários).\n".encode("utf-8"))
                sock.close()
                return

            clientes[sock] = {"nick": nick, "ip": address[0]}

        cor_usuario = get_cor_usuario(nick)

        # Servidor vê a entrada no lado esquerdo com a cor do usuário
        print_server(f"[Servidor]: {cor_usuario}{nick}{RESET}{VERDE} entrou no chat.", VERDE)

        # Outros clientes veem a entrada (menos o próprio)
        broadcast(f"[{get_timestamp()}] [Servidor]: {nick} entrou no chat.\n", origem=sock)

        while running:
            # Verifica se o socket ainda está na lista (não foi kickado)
            with lock:
                if sock not in clientes:
                    return
            
            data = sock.recv(1024)
            if not data:
                break

            msg = data.decode("utf-8").strip()
            if not msg:
                continue

            cmd = msg.lower()
            if cmd.startswith("/"):
                cmd = cmd[1:]

            if cmd == "sair":
                break

            if cmd == "usuarios":
                lista_msg = listar_usuarios()
                try:
                    sock.sendall(lista_msg.encode("utf-8"))
                except OSError:
                    pass
                continue

            if cmd == "ajuda":
                ajuda_msg = ajuda_cliente_texto()
                try:
                    sock.sendall(ajuda_msg.encode("utf-8"))
                except OSError:
                    pass
                continue

            if cmd.startswith("kick") or cmd == "encerrar" or cmd in ("entrar",):
                try:
                    sock.sendall(f"{VERMELHO}[-] O comando '{msg}' só pode ser executado pelo servidor.{RESET}\n".encode("utf-8"))
                except OSError:
                    pass
                continue

            # Mensagens de clientes aparecem no lado esquerdo para o servidor com cor exclusiva
            cor = get_cor_usuario(nick)
            print_server(f"[{nick} ({address[0]})]: {msg}", cor)

            # Outros clientes recebem a mensagem (aparece no lado esquerdo deles)
            broadcast(f"[{get_timestamp()}] [{nick} ({address[0]})]: {msg}\n", origem=sock)

    except ConnectionResetError:
        pass
    except OSError:
        pass
    except Exception as e:
        print_server(f"[Erro ao processar {address[0]}]: {e}", VERMELHO)
    finally:
        with lock:
            if sock in clientes:
                nome = clientes[sock]["nick"]
                del clientes[sock]
                liberar_cor_usuario(nome)
                print_server(f"[Servidor]: {nome} saiu do chat.", VERDE)
                broadcast(f"[{get_timestamp()}] [Servidor]: {nome} saiu do chat.\n")
        try:
            sock.close()
        except OSError:
            pass


def ler_input():
    """Thread separada para ler comandos e mensagens do servidor."""
    while running:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            msg = line.strip()
            if msg:
                input_queue.put(msg)
            else:
                with print_lock:
                    sys.stdout.write(f"{AMARELO}[Servidor]: {RESET}")
                    sys.stdout.flush()
        except (EOFError, KeyboardInterrupt):
            break
        except:
            break


def main():
    global running, server_in_chat

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_USERS)

    print_server(f"[*] Servidor ativo em {HOST}:{PORT}")

    def aceitar_conexoes():
        global running
        while running:
            try:
                sock, addr = server.accept()
                t = threading.Thread(target=tratar_cliente, args=(sock, addr), daemon=True)
                t.start()
            except OSError:
                break

    # Inicia threads de aceitação e leitura de input
    threading.Thread(target=aceitar_conexoes, daemon=True).start()
    threading.Thread(target=ler_input, daemon=True).start()

    # Loop principal do servidor (processa comandos e mensagens)
    while running:
        try:
            msg = input_queue.get(timeout=1)
        except queue.Empty:
            continue

        cmd = msg.lower()
        if cmd.startswith("/"):
            cmd = cmd[1:]

        if cmd == "ajuda":
            print_server(ajuda_texto(), VERDE)
            continue

        if cmd == "usuarios":
            print_server(listar_usuarios(), VERDE)
            continue

        if cmd == "sair":
            server_in_chat = False
            print_server("[*] Servidor saiu do chat (modo gerenciamento ativo).", AMARELO)
            broadcast(f"[{get_timestamp()}] [Servidor]: Servidor saiu do chat (mas continua ativo).\n")
            continue

        if cmd == "entrar":
            server_in_chat = True
            print_server("[*] Servidor voltou ao chat.", AMARELO)
            broadcast(f"[{get_timestamp()}] [Servidor]: Servidor voltou ao chat.\n")
            continue

        if cmd.startswith("kick"):
            partes = msg.split(" ", 1)
            if len(partes) > 1 and partes[1].strip():
                alvo = partes[1].strip()
                if expulsar(alvo):
                    print_server(f"[*] Usuário {alvo} expulso.", VERDE)
                else:
                    print_server(f"[-] Usuário '{alvo}' não encontrado.", VERMELHO)
            else:
                print_server("[-] Uso correto: kick <nickname>", VERMELHO)
            continue

        if cmd == "encerrar":
            print_server("[*] Encerrando chat...", VERMELHO)
            running = False
            broadcast(f"[{get_timestamp()}] [Servidor]: O servidor encerrou o chat.\n")
            break

        # Se não for comando e o servidor estiver no chat, envia mensagem
        if server_in_chat:
            # Mostra no lado direito para o próprio servidor
            print_server(msg, AMARELO, align_right=True)
            # Envia para os clientes (aparecerá no lado esquerdo deles)
            broadcast(f"[{get_timestamp()}] [Servidor]: {msg}\n")
        else:
            print_server("[-] O servidor está fora do chat. Digite 'entrar' para voltar a conversar.", VERMELHO)

    # Finalização
    with lock:
        for c in list(clientes.keys()):
            try:
                c.close()
            except OSError:
                pass

    server.close()
    print_server("[*] Servidor finalizado.")


if __name__ == "__main__":
    main()
