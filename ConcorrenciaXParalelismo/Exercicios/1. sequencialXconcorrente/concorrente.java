class Concorrente {
    static void tarefa(String nome, int segundos) {
        System.out.println(nome + " iniciou");

        try {
            Thread.sleep(segundos * 1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println(nome + " terminou");
    }

    public static void main(String[] args) throws InterruptedException {
        long inicio = System.currentTimeMillis();

        Thread t1 = new Thread(() -> tarefa("A", 3));
        Thread t2 = new Thread(() -> tarefa("B", 2));
        Thread t3 = new Thread(() -> tarefa("C", 4));

        t1.start();
        t2.start();
        t3.start();

        t1.join();
        t2.join();
        t3.join();

        long fim = System.currentTimeMillis();

        System.out.println("Tempo: " + (fim - inicio) / 1000.0 + " s");
    }
}
