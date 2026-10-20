from concurrent.futures import ProcessPoolExecutor
import time
from versao_a_sequencial import LIMITE, contar_primos_intervalo


def dividir_intervalo(inicio: int, fim: int, n_partes: int) -> list[tuple[int, int]]:
    tamanho_total = fim - inicio + 1
    tamanho_parte = tamanho_total // n_partes
    intervalos = []

    atual = inicio
    for i in range(n_partes):
        fim_parte = atual + tamanho_parte - 1 if i < n_partes - 1 else fim
        intervalos.append((atual, fim_parte))
        atual = fim_parte + 1

    return intervalos


def executar_paralelo(n_workers: int, limite: int = LIMITE):
    print(f"=== Versão B: Paralelo com {n_workers} Workers (ProcessPoolExecutor) ===")
    intervalos = dividir_intervalo(1, limite, n_workers)

    for idx, (ini, fim) in enumerate(intervalos, start=1):
        print(f"  Worker {idx} → {ini:,} até {fim:,}")

    t0 = time.perf_counter()

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        resultados = list(executor.map(contar_primos_intervalo, intervalos))

    total_primos = sum(resultados)
    tempo_total = time.perf_counter() - t0

    print(f"Total de primos encontrados: {total_primos:,}")
    print(f"Tempo ({n_workers} Workers): {tempo_total:.2f} s\n")
    return tempo_total, total_primos


if __name__ == "__main__":
    for n in (2, 4, 8):
        executar_paralelo(n)
