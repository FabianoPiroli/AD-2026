class Sequencial {
    static void tarefa(String nome, int segundos) throws InterruptedException {
        System.out.println(nome + " iniciou");
        Thread.sleep(segundos * 1000);
        System.out.println(nome + " terminou");
    }

    public static void main(String[] args) throws InterruptedException {
        long inicio = System.currentTimeMillis();

        tarefa("A", 3);
        tarefa("B", 2);
        tarefa("C", 4);

        long fim = System.currentTimeMillis();

        System.out.println("Tempo: " + (fim - inicio) / 1000.0 + " s");
    }
}
