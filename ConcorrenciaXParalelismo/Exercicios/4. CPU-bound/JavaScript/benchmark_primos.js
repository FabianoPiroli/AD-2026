const { executarSequencial } = require("./versao_a_sequencial");
const { executarParalelo } = require("./versao_b_paralela");

async function main() {
    const { tempoTotal: tempoSeq } = executarSequencial();

    const workers = [2, 4, 8];
    const temposWorkers = {};

    for (const n of workers) {
        const { tempoTotal } = await executarParalelo(n);
        temposWorkers[n] = tempoTotal;
    }

    console.log("=======================================================");
    console.log(`| ${"Versão".padEnd(30)} | ${"Tempo Total".padEnd(18)} |`);
    console.log("|--------------------------------|--------------------|");
    console.log(`| ${"Versão A - Sequencial".padEnd(30)} | ${tempoSeq.toFixed(2).padStart(16)} s |`);
    for (const n of workers) {
        console.log(`| ${`Versão B - ${n} Workers`.padEnd(30)} | ${temposWorkers[n].toFixed(2).padStart(16)} s |`);
    }
    console.log("=======================================================");
}

main();
