function tarefa(nome, tempo) {
    return new Promise(resolve => {
        console.log(nome, "iniciou");
        setTimeout(() => {
            console.log(nome, "terminou");
            resolve();
        }, tempo);
    });
}

async function executar() {
    console.time("tempo");
    await Promise.all([
        tarefa("A", 3000),
        tarefa("B", 2000),
        tarefa("C", 4000)
    ]);

    console.timeEnd("tempo");
}

executar();
