package sockets.servidorsimples;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class CalculadoraServidorSimples {
    private static final int PORTA = 9000;

    public static void main(String[] args) {
        try (ServerSocket servidor = new ServerSocket(PORTA)) {
            System.out.println("Servidor rodando na porta " + PORTA);
            while (true) {
                System.out.println("Aguardando conexão...");
                try (Socket cliente = servidor.accept();
                        DataInputStream entrada = new DataInputStream(cliente.getInputStream());
                        DataOutputStream saida = new DataOutputStream(cliente.getOutputStream())) {
                    System.out.println("Cliente conectado: " + cliente.getRemoteSocketAddress());
                    int num1 = entrada.readInt();
                    int num2 = entrada.readInt();
                    int resultado = num1 + num2;
                    System.out.println("Recebido: " + num1 + " + " + num2);
                    saida.writeInt(resultado);
                    saida.flush();
                    System.out.println("Resultado enviado: " + resultado);
                }
            }
        } catch (IOException e) {
            System.err.println("Erro no servidor: " + e.getMessage());
        }
    }
}