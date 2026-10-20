import threading
import time

saldo = 1000


def realizar_saques():
    global saldo
    for _ in range(100):
        # Lê o saldo atual (início da região crítica)
        saldo_atual = saldo
        # Pequena pausa para simular processamento e forçar a troca de contexto entre threads
        time.sleep(0.0001)
        # Atualiza o saldo (fim da região crítica)
        saldo = saldo_atual - 1


threads = []

# Cria 10 threads
for _ in range(10):
    t = threading.Thread(target=realizar_saques)
    threads.append(t)
    t.start()

# Aguarda todas as threads terminarem
for t in threads:
    t.join()

print(f"Saldo final (sem Lock): R$ {saldo}")

