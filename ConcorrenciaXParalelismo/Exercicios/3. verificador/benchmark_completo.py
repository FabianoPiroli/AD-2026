import asyncio
from etapa1_sequencial import executar_sequencial
from etapa2_pool_fixo import executar_pool_fixo
from etapa2_asyncio import executar_asyncio


def main():
    tempo_seq = executar_sequencial()
    tempo_pool = executar_pool_fixo(10)
    tempo_async = asyncio.run(executar_asyncio())

    print("=" * 50)
    print(f"| {'Implementação':<27} | {'Tempo Total':<15} |")
    print("|" + "-" * 29 + "|" + "-" * 17 + "|")
    print(f"| {'Sequencial':<27} | {tempo_seq:>12.2f} s |")
    print(f"| {'Concorrente (pool fixo)':<27} | {tempo_pool:>12.2f} s |")
    print(f"| {'Concorrente sem limites':<27} | {tempo_async:>12.2f} s |")
    print("=" * 50)


if __name__ == "__main__":
    main()
