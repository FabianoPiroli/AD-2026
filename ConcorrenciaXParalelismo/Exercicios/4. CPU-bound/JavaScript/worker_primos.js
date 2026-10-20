const { isMainThread, parentPort } = require("worker_threads");
const { contarPrimosIntervalo } = require("./versao_a_sequencial");

// Função exportada para uso com Piscina ou Worker Pool
function processarIntervalo({ inicio, fim }) {
    return contarPrimosIntervalo(inicio, fim);
}

// Suporte direto ao worker_threads nativo do Node.js
if (!isMainThread && parentPort) {
    parentPort.on("message", (tarefa) => {
        const resultado = processarIntervalo(tarefa);
        parentPort.postMessage(resultado);
    });
}

module.exports = processarIntervalo;
