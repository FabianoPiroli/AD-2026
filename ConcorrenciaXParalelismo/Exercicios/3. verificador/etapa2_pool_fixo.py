from concurrent.futures import ThreadPoolExecutor
import time
import requests

URLS = [
    ("Google", "https://www.google.com"),
    ("GitHub", "https://www.github.com"),
    ("Wikipedia", "https://www.wikipedia.org"),
    ("Python", "https://www.python.org"),
    ("StackOverflow", "https://stackoverflow.com"),
    ("MDN", "https://developer.mozilla.org"),
    ("Reddit", "https://www.reddit.com"),
    ("Cloudflare", "https://www.cloudflare.com"),
    ("NPM", "https://www.npmjs.com"),
    ("PyPI", "https://pypi.org"),
    ("Docker", "https://www.docker.com"),
    ("Kubernetes", "https://kubernetes.io"),
    ("Linux", "https://www.kernel.org"),
    ("Apache", "https://www.apache.org"),
    ("Mozilla", "https://www.mozilla.org"),
    ("W3C", "https://www.w3.org"),
    ("IANA", "https://www.iana.org"),
    ("Example", "https://www.example.com"),
    ("HTTPBin", "https://httpbin.org/get"),
    ("Servidor X", "https://servidor-inexistente-teste-12345.com"),
]


HEADERS = {"User-Agent": "Mozilla/5.0"}


def verificar_url(item):
    nome, url = item
    inicio = time.perf_counter()
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=5)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        if resposta.status_code < 400:
            return f"{nome:<14} → OK   → {tempo_ms:.0f} ms"
        return f"{nome:<14} → ERRO ({resposta.status_code}) → {tempo_ms:.0f} ms"
    except requests.RequestException:
        return f"{nome:<14} → ERRO"


def executar_pool_fixo(num_threads=10):
    print(f"=== Etapa 2A: Concorrente (ThreadPoolExecutor - {num_threads} threads) ===")
    inicio_total = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        resultados = executor.map(verificar_url, URLS)
        for resultado in resultados:
            print(resultado)

    tempo_total = time.perf_counter() - inicio_total
    print(f"\nTempo Total (Pool fixo de {num_threads} threads): {tempo_total:.2f} s\n")
    return tempo_total


if __name__ == "__main__":
    executar_pool_fixo(10)
