public class BenchmarkPrimos {
    public static void main(String[] args) throws Exception {
        double tempoSeq = VersaoASequencial.executarSequencial();

        int[] workers = {2, 4, 8};
        double[] temposWorkers = new double[workers.length];

        for (int i = 0; i < workers.length; i++) {
            temposWorkers[i] = VersaoBParalela.executarParalelo(workers[i]);
        }

        System.out.println("=======================================================");
        System.out.printf("| %-30s | %-18s |%n", "Versão", "Tempo Total");
        System.out.println("|--------------------------------|--------------------|");
        System.out.printf("| %-30s | %16.2f s |%n", "Versão A - Sequencial", tempoSeq);
        for (int i = 0; i < workers.length; i++) {
            System.out.printf("| %-30s | %16.2f s |%n", "Versão B - " + workers[i] + " Workers", temposWorkers[i]);
        }
        System.out.println("=======================================================");
    }
}
