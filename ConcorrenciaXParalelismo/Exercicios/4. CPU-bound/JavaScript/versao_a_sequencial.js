const { performance } = require("perf_hooks");

const LIMITE = 10_000_000;

function ehPrimo(n) {
    if (n < 2) return false;
    if (n === 2 || n === 3) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;
    const raiz = Math.floor(Math.sqrt(n));
    for (let i = 5; i <= raiz; i += 6) {
        if (n % i === 0 || n % (i + 2) === 0) {
            return false;
        }
    }
    return true;
}

function contarPrimosIntervalo(inicio, fim) {
    let contador = 0;
    for (let n = inicio; n <= fim; n++) {
        if (ehPrimo(n)) {
            contador++;
        }
    }
    return contador;
}

function executarSequencial(limite = LIMITE) {
    console.log(`=== Versão A: Sequencial (1 até ${limite.toLocaleString("pt-BR")}) ===`);
    const t0 = performance.now();

    const totalPrimos = contarPrimosIntervalo(1, limite);

    const tempoTotal = (performance.now() - t0) / 1000;
    console.log(`Total de primos encontrados: ${totalPrimos.toLocaleString("pt-BR")}`);
    console.log(`Tempo (Sequencial): ${tempoTotal.toFixed(2)} s\n`);
    return { tempoTotal, totalPrimos };
}

if (require.main === module) {
    executarSequencial();
}

module.exports = { LIMITE, ehPrimo, contarPrimosIntervalo, executarSequencial };
