import threading
import time


def tarefa(nome, segundos):
    print(nome, "iniciou")

    time.sleep(segundos)

    print(nome, "terminou")


inicio = time.perf_counter()

t1 = threading.Thread(target=tarefa, args=("A", 3))
t2 = threading.Thread(target=tarefa, args=("B", 2))
t3 = threading.Thread(target=tarefa, args=("C", 4))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

fim = time.perf_counter()

print(f"Tempo: {fim - inicio:.2f} s")
