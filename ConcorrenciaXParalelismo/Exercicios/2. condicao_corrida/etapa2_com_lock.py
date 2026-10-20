import threading
import time

saldo = 1000
lock = threading.Lock()


def realizar_saques():
    global saldo
    for _ in range(100):
        # Protege a região crítica com exclusão mútua (Lock)
        with lock:
            saldo_atual = saldo
            time.sleep(0.0001)
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

print(f"Saldo final (com Lock): R$ {saldo}")

