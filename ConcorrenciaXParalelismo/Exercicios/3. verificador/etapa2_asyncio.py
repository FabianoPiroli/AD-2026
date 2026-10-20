import asyncio
import ssl
import time
import aiohttp
import certifi

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


async def verificar_url_async(session, nome, url):
    inicio = time.perf_counter()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resposta:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            if resposta.status < 400:
                return f"{nome:<14} → OK   → {tempo_ms:.0f} ms"
            return f"{nome:<14} → ERRO ({resposta.status}) → {tempo_ms:.0f} ms"
    except Exception:
        return f"{nome:<14} → ERRO"


async def executar_asyncio():
    print("=== Etapa 2B: Concorrente sem limites (asyncio + aiohttp) ===")
    inicio_total = time.perf_counter()

    # Usa o pacote de certificados do certifi (o mesmo que o requests utiliza)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector, headers=HEADERS) as session:
        tarefas = [verificar_url_async(session, nome, url) for nome, url in URLS]
        resultados = await asyncio.gather(*tarefas)
        for resultado in resultados:
            print(resultado)

    tempo_total = time.perf_counter() - inicio_total
    print(f"\nTempo Total (Concorrente sem limites - asyncio): {tempo_total:.2f} s\n")
    return tempo_total


if __name__ == "__main__":
    asyncio.run(executar_asyncio())
