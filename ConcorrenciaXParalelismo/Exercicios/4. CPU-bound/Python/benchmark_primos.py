from versao_a_sequencial import executar_sequencial
from versao_b_paralela import executar_paralelo


def main():
    tempo_seq, _ = executar_sequencial()

    tempos_workers = {}
    for n in (2, 4, 8):
        tempo_w, _ = executar_paralelo(n)
        tempos_workers[n] = tempo_w

    print("=" * 55)
    print(f"| {'Versão':<30} | {'Tempo Total':<18} |")
    print("|" + "-" * 32 + "|" + "-" * 20 + "|")
    print(f"| {'Versão A - Sequencial':<30} | {tempo_seq:>15.2f} s |")
    for n, tempo in tempos_workers.items():
        print(f"| {f'Versão B - {n} Workers':<30} | {tempo:>15.2f} s |")
    print("=" * 55)


if __name__ == "__main__":
    main()
