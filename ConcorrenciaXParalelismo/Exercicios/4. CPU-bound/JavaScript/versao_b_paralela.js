const path = require("path");
const { Worker } = require("worker_threads");
const { performance } = require("perf_hooks");
const { LIMITE } = require("./versao_a_sequencial");

// Implementação de Worker Pool nativo (mesma interface do Piscina)
class WorkerPool {
    constructor({ filename, maxThreads }) {
        this.filename = filename;
        this.maxThreads = maxThreads;
        this.workers = [];
        this.livres = [];
        this.fila = [];

        for (let i = 0; i < maxThreads; i++) {
            const worker = new Worker(this.filename);
            this.workers.push(worker);
            this.livres.push(worker);
        }
    }

    run(tarefa) {
        return new Promise((resolve, reject) => {
            this.fila.push({ tarefa, resolve, reject });
            this._despachar();
        });
    }

    _despachar() {
        while (this.livres.length > 0 && this.fila.length > 0) {
            const worker = this.livres.pop();
            const { tarefa, resolve, reject } = this.fila.shift();

            const onMessage = (resultado) => {
                worker.removeListener("error", onError);
                this.livres.push(worker);
                resolve(resultado);
                this._despachar();
            };

            const onError = (erro) => {
                worker.removeListener("message", onMessage);
                this.livres.push(worker);
                reject(erro);
                this._despachar();
            };

            worker.once("message", onMessage);
            worker.once("error", onError);
            worker.postMessage(tarefa);
        }
    }

    async destroy() {
        await Promise.all(this.workers.map((w) => w.terminate()));
    }
}

function dividirIntervalo(inicio, fim, nPartes) {
    const tamanhoTotal = fim - inicio + 1;
    const tamanhoParte = Math.floor(tamanhoTotal / nPartes);
    const intervalos = [];

    let atual = inicio;
    for (let i = 0; i < nPartes; i++) {
        const fimParte = i < nPartes - 1 ? atual + tamanhoParte - 1 : fim;
        intervalos.push({ inicio: atual, fim: fimParte });
        atual = fimParte + 1;
    }
    return intervalos;
}

async function executarParalelo(nWorkers, limite = LIMITE) {
    console.log(`=== Versão B: Paralelo com ${nWorkers} Workers (Worker Pool) ===`);
    const intervalos = dividirIntervalo(1, limite, nWorkers);

    intervalos.forEach((inter, idx) => {
        console.log(
            `  Worker ${idx + 1} → ${inter.inicio.toLocaleString("pt-BR")} até ${inter.fim.toLocaleString("pt-BR")}`
        );
    });

    const t0 = performance.now();

    const pool = new WorkerPool({
        filename: path.resolve(__dirname, "worker_primos.js"),
        maxThreads: nWorkers,
    });

    const resultados = await Promise.all(
        intervalos.map((intervalo) => pool.run(intervalo))
    );

    await pool.destroy();

    const totalPrimos = resultados.reduce((acc, val) => acc + val, 0);
    const tempoTotal = (performance.now() - t0) / 1000;

    console.log(`Total de primos encontrados: ${totalPrimos.toLocaleString("pt-BR")}`);
    console.log(`Tempo (${nWorkers} Workers): ${tempoTotal.toFixed(2)} s\n`);
    return { tempoTotal, totalPrimos };
}

async function main() {
    for (const n of [2, 4, 8]) {
        await executarParalelo(n);
    }
}

if (require.main === module) {
    main();
}

module.exports = { dividirIntervalo, executarParalelo };
