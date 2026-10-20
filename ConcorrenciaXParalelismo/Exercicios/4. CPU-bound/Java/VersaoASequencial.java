public class VersaoASequencial {
    public static final int LIMITE = 10_000_000;

    public static boolean ehPrimo(int n) {
        if (n < 2) return false;
        if (n == 2 || n == 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        int raiz = (int) Math.sqrt(n);
        for (int i = 5; i <= raiz; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }

    public static int contarPrimosIntervalo(int inicio, int fim) {
        int contador = 0;
        for (int n = inicio; n <= fim; n++) {
            if (ehPrimo(n)) {
                contador++;
            }
        }
        return contador;
    }

    public static double executarSequencial() {
        System.out.printf("=== Versão A: Sequencial (1 até %,d) ===%n", LIMITE);
        long t0 = System.nanoTime();

        int totalPrimos = contarPrimosIntervalo(1, LIMITE);

        double tempoTotal = (System.nanoTime() - t0) / 1_000_000_000.0;
        System.out.printf("Total de primos encontrados: %,d%n", totalPrimos);
        System.out.printf("Tempo (Sequencial): %.2f s%n%n", tempoTotal);
        return tempoTotal;
    }

    public static void main(String[] args) {
        executarSequencial();
    }
}
