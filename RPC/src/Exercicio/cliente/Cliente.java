package cliente;

import comum.Calculadora;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Cliente {
    public static void main(String[] args) {
        try {
            String ipServidor = (args.length > 0) ? args[0] : "localhost";
            System.out.println("Conectando ao servidor em: " + ipServidor);

            Registry registry = LocateRegistry.getRegistry(ipServidor, 1099);
            Calculadora calc = (Calculadora) registry.lookup("ServicoCalculadora");

            System.out.println("Resultado da Soma (15 + 25): " + calc.somar(15, 25));
            System.out.println("Resultado da Subtração (30 - 10): " + calc.subtrair(30, 10));
            System.out.println("Resultado da Multiplicação (6 * 7): " + calc.multiplicar(6, 7));
            System.out.println("Resultado da Divisão (40 / 4): " + calc.dividir(40, 4));

        } catch (Exception e) {
            System.err.println("Erro no cliente: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
