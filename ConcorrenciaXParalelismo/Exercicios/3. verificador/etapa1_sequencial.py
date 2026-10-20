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


def verificar_url(nome, url):
    inicio = time.perf_counter()
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=5)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        if resposta.status_code < 400:
            print(f"{nome:<14} → OK   → {tempo_ms:.0f} ms")
        else:
            print(f"{nome:<14} → ERRO ({resposta.status_code}) → {tempo_ms:.0f} ms")
    except requests.RequestException:
        print(f"{nome:<14} → ERRO")


def executar_sequencial():
    print("=== Etapa 1: Sequencial Síncrono ===")
    inicio_total = time.perf_counter()

    for nome, url in URLS:
        verificar_url(nome, url)

    tempo_total = time.perf_counter() - inicio_total
    print(f"\nTempo Total (Sequencial): {tempo_total:.2f} s\n")
    return tempo_total


if __name__ == "__main__":
    executar_sequencial()
