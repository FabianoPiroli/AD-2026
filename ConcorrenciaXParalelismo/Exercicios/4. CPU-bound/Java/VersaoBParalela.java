import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;

public class VersaoBParalela {
    public static final int LIMITE = 10_000_000;

    public static List<int[]> dividirIntervalo(int inicio, int fim, int nPartes) {
        int tamanhoTotal = fim - inicio + 1;
        int tamanhoParte = tamanhoTotal / nPartes;
        List<int[]> intervalos = new ArrayList<>();

        int atual = inicio;
        for (int i = 0; i < nPartes; i++) {
            int fimParte = (i < nPartes - 1) ? (atual + tamanhoParte - 1) : fim;
            intervalos.add(new int[]{atual, fimParte});
            atual = fimParte + 1;
        }
        return intervalos;
    }

    public static double executarParalelo(int nWorkers) throws InterruptedException, ExecutionException {
        System.out.printf("=== Versão B: Paralelo com %d Workers (parallelStream) ===%n", nWorkers);
        List<int[]> intervalos = dividirIntervalo(1, LIMITE, nWorkers);

        for (int i = 0; i < intervalos.size(); i++) {
            int[] inter = intervalos.get(i);
            System.out.printf("  Worker %d → %,d até %,d%n", i + 1, inter[0], inter[1]);
        }

        long t0 = System.nanoTime();

        // Define um pool com exatamente nWorkers para que o parallelStream() use N threads
        ForkJoinPool pool = new ForkJoinPool(nWorkers);
        int totalPrimos = pool.submit(() ->
            intervalos.parallelStream()
                .mapToInt(inter -> VersaoASequencial.contarPrimosIntervalo(inter[0], inter[1]))
                .sum()
        ).get();
        pool.shutdown();

        double tempoTotal = (System.nanoTime() - t0) / 1_000_000_000.0;
        System.out.printf("Total de primos encontrados: %,d%n", totalPrimos);
        System.out.printf("Tempo (%d Workers): %.2f s%n%n", nWorkers, tempoTotal);
        return tempoTotal;
    }

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        int[] workers = {2, 4, 8};
        for (int n : workers) {
            executarParalelo(n);
        }
    }
}
