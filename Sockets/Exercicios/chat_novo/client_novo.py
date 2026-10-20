import socket
import threading
import sys
import time
import os
import shutil
import textwrap
from datetime import datetime

# Ativa suporte a códigos ANSI no terminal do Windows se necessário
os.system('')

# Cores ANSI
RESET = '\033[0m'
AMARELO = '\033[93m'    # Mensagens do servidor
CIANO = '\033[96m'      # Padrão clientes
VERDE = '\033[92m'      # Suas mensagens
ROXO = '\033[95m'       # Timestamps
VERMELHO = '\033[91m'   # Erros e avisos

# Paleta de cores distintas para atribuir a cada usuário diferente
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

cores_clientes = {}      # nick → código de cor ANSI

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001

print_lock = threading.Lock()
running = True


def get_cor_usuario(nick):
    """Garante que cada usuário no chat tenha uma cor exclusiva e diferente."""
    if nick not in cores_clientes:
        cores_em_uso = set(cores_clientes.values())
        disponiveis = [c for c in CORES_USUARIOS if c not in cores_em_uso]
        if disponiveis:
            cores_clientes[nick] = disponiveis[0]
        else:
            cores_clientes[nick] = CORES_USUARIOS[len(cores_clientes) % len(CORES_USUARIOS)]
    return cores_clientes[nick]


def liberar_cor_usuario(nick):
    """Libera a cor quando um usuário sai do chat."""
    cores_clientes.pop(nick, None)


def extrair_nick(linha):
    """Extrai o nickname de mensagens no formato '[HH:MM:SS] [Nick (IP)]: '."""
    try:
        texto = linha[11:] if (linha.startswith("[") and len(linha) > 10 and linha[9] == "]") else linha
        if texto.startswith("["):
            nick_part = texto[1:].split(" (", 1)[0]
            if nick_part and not nick_part.startswith("Servidor"):
                return nick_part.strip()
    except Exception:
        pass
    return None


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


def formatar_direita(prefixo_sem_cor, msg, cor_msg=VERDE):
    """
    Formata mensagem enviada pelo próprio usuário no lado direito (estilo WhatsApp).
    prefixo_sem_cor: ex. '[14:20:10] [Você]: '
    """
    largura = get_terminal_width()
    margem = 2  # Margem à direita para evitar quebra indesejada no terminal
    
    # Limita a largura máxima do balão a ~65% da tela para manter visual de conversa
    max_bubble = max(25, int(largura * 0.65))
    h_len = len(prefixo_sem_cor)
    content_width = max(15, max_bubble - h_len)
    
    lines = textwrap.wrap(msg, width=content_width)
    if not lines:
        lines = ['']
        
    formatted_lines = []
    
    # Se o prefixo tiver timestamp '[HH:MM:SS] '
    if prefixo_sem_cor.startswith("[") and len(prefixo_sem_cor) > 10 and prefixo_sem_cor[9] == "]":
        timestamp_part = prefixo_sem_cor[:11]
        resto_prefixo = prefixo_sem_cor[11:]
        l1_color = f"{ROXO}{timestamp_part}{RESET}{cor_msg}{resto_prefixo}{lines[0]}{RESET}"
    else:
        l1_color = f"{cor_msg}{prefixo_sem_cor}{lines[0]}{RESET}"
        
    l1_clean = f"{prefixo_sem_cor}{lines[0]}"
    formatted_lines.append((l1_color, len(l1_clean)))
    
    # Linhas seguintes alinhadas abaixo do texto da mensagem
    pad = " " * h_len
    for l in lines[1:]:
        l_color = f"{cor_msg}{pad}{l}{RESET}"
        l_clean = pad + l
        formatted_lines.append((l_color, len(l_clean)))
        
    block_width = max(v_len for _, v_len in formatted_lines)
    indent = max(0, largura - block_width - margem)
    
    return "\n".join(" " * indent + l_col for l_col, _ in formatted_lines)


def formatar_esquerda(msg, cor):
    """Formata mensagens recebidas de outros no lado esquerdo com destaque no timestamp."""
    if msg.startswith("[") and len(msg) > 10 and msg[9] == "]":
        timestamp_part = msg[:11]
        resto = msg[11:]
        return f"{ROXO}{timestamp_part}{RESET}{cor}{resto}{RESET}"
    return f"{cor}{msg}{RESET}"


def receber(sock):
    """Recebe mensagens do servidor e as exibe no lado esquerdo com cor exclusiva por usuário."""
    global running
    while running:
        try:
            data = sock.recv(1024).decode("utf-8")
            if not data:
                with print_lock:
                    sys.stdout.write('\r\033[K')
                    sys.stdout.write(f"\n{VERMELHO}[*] Conexão encerrada pelo servidor.{RESET}\n")
                    sys.stdout.flush()
                running = False
                break
            
            linhas = [l for l in data.splitlines() if l.strip()]
            for linha in linhas:
                nick = extrair_nick(linha)
                if nick:
                    # Cada usuário tem sua própria cor diferente
                    color = get_cor_usuario(nick)
                elif "[Servidor]:" in linha:
                    color = AMARELO
                    # Libera cor se o usuário saiu ou foi expulso
                    for termo in ["saiu do chat", "foi expulso"]:
                        if termo in linha:
                            partes = linha.split("[Servidor]:", 1)[1].strip()
                            nick_saiu = partes.split(" ", 1)[0]
                            liberar_cor_usuario(nick_saiu)
                else:
                    color = CIANO
                
                msg_formatada = formatar_esquerda(linha, color)
                with print_lock:
                    # Limpa linha de entrada atual e imprime a mensagem à esquerda
                    sys.stdout.write('\r\033[K')
                    sys.stdout.write(msg_formatada + "\n")
                    # Reexibe o prompt do usuário
                    sys.stdout.write(f"{VERDE}[Você]: {RESET}")
                    sys.stdout.flush()
        except:
            break
    try:
        sock.close()
    except OSError:
        pass


def conectar():
    """Tenta conectar ao servidor com reconexão automática."""
    global running
    max_tentativas = 5
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            print(f"{VERDE}[+] Conectado ao servidor.{RESET}")
            
            # Handshake do nickname
            prompt = client.recv(1024).decode("utf-8")
            if "Digite seu nickname" in prompt:
                nick = input(prompt).strip()
                while not nick:
                    nick = input("Nickname não pode ser vazio. Digite seu nickname: ").strip()
                client.sendall((nick + "\n").encode("utf-8"))
            elif prompt:
                print(prompt)
                client.close()
                return False
            
            running = True
            thread_receber = threading.Thread(target=receber, args=(client,), daemon=True)
            thread_receber.start()
            
            # Loop de envio de mensagens
            while running:
                with print_lock:
                    sys.stdout.write(f"{VERDE}[Você]: {RESET}")
                    sys.stdout.flush()
                
                try:
                    msg = input().strip()
                except (EOFError, KeyboardInterrupt):
                    msg = "sair"
                
                with print_lock:
                    # Remove do terminal a linha bruta digitada pelo usuário
                    sys.stdout.write("\033[A\r\033[K")
                    sys.stdout.flush()
                
                if msg.lower() in ("sair", "/sair"):
                    running = False
                    try:
                        client.sendall("sair\n".encode("utf-8"))
                        client.close()
                    except OSError:
                        pass
                    return False  # Saída normal, não reconecta
                
                if msg:
                    cmd_norm = msg.lower().lstrip("/")
                    if cmd_norm in ("usuarios", "ajuda"):
                        # Comando para o servidor (não formata como balão de conversa local)
                        try:
                            client.sendall((msg + "\n").encode("utf-8"))
                        except OSError:
                            with print_lock:
                                sys.stdout.write(f"{VERMELHO}[-] Erro ao enviar comando.{RESET}\n")
                                sys.stdout.flush()
                            break
                    else:
                        timestamp = get_timestamp()
                        bubble = formatar_direita(f"[{timestamp}] [Você]: ", msg, cor_msg=VERDE)
                        with print_lock:
                            sys.stdout.write(bubble + "\n")
                            sys.stdout.flush()
                        try:
                            client.sendall((msg + "\n").encode("utf-8"))
                        except OSError:
                            with print_lock:
                                sys.stdout.write(f"{VERMELHO}[-] Erro ao enviar mensagem.{RESET}\n")
                                sys.stdout.flush()
                            break
            
        except ConnectionRefusedError:
            tentativa += 1
            print(f"{VERMELHO}[-] Erro ao conectar. Tentando novamente ({tentativa}/{max_tentativas})...{RESET}")
            time.sleep(2)
        except Exception as e:
            print(f"{VERMELHO}[-] Erro: {e}{RESET}")
            tentativa += 1
            time.sleep(2)
    
    return True  # Tentou reconectar mas falhou


if __name__ == "__main__":
    # Loop principal com reconexão automática
    while True:
        if conectar():
            # Se foi kickado ou desconectado abruptamente, tenta reconectar
            print(f"\n{AMARELO}[*] Tentando reconectar em 3 segundos...{RESET}")
            time.sleep(3)
        else:
            # Saída normal com "sair"
            print(f"{AMARELO}[*] Cliente finalizado.{RESET}")
            break
