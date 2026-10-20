import math
import time

LIMITE = 10_000_000


def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    raiz = math.isqrt(n)
    for i in range(5, raiz + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def contar_primos_intervalo(intervalo: tuple[int, int]) -> int:
    inicio, fim = intervalo
    contador = 0
    for n in range(inicio, fim + 1):
        if eh_primo(n):
            contador += 1
    return contador


def executar_sequencial(limite: int = LIMITE):
    print(f"=== Versão A: Sequencial (1 até {limite:,}) ===")
    t0 = time.perf_counter()

    total_primos = contar_primos_intervalo((1, limite))

    tempo_total = time.perf_counter() - t0
    print(f"Total de primos encontrados: {total_primos:,}")
    print(f"Tempo (Sequencial): {tempo_total:.2f} s\n")
    return tempo_total, total_primos


if __name__ == "__main__":
    executar_sequencial()
