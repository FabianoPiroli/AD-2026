package sockets.servidoravancado;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CalculadoraServidorAvancado {
    private static final int PORTA = 9000;
    private static final int TIMEOUT = 5000;
    private static final ExecutorService pool = Executors.newFixedThreadPool(10);

    public static void main(String[] args) {
        try (ServerSocket servidor = new ServerSocket(PORTA)) {
            System.out.println("Servidor JSON rodando na porta " + PORTA);
            while (true) {
                Socket cliente = servidor.accept();
                System.out.println("Cliente conectado: " + cliente.getRemoteSocketAddress());
                pool.execute(() -> processarCliente(cliente));
            }
        } catch (IOException e) {
            System.err.println("Erro no servidor: " + e.getMessage());
        } finally {
            pool.shutdown();
        }
    }

    private static void processarCliente(Socket cliente) {
        try (Socket socket = cliente;
                BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream(),
                        StandardCharsets.UTF_8));
                PrintWriter saida = new PrintWriter(
                        new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8),
                        true)) {
            socket.setSoTimeout(TIMEOUT);
            String requisicao = entrada.readLine();
            if (requisicao == null)
                return;
            System.out.println("Recebido: " + requisicao);
            String resposta = processarOperacao(requisicao);
            saida.println(resposta);
            System.out.println("Enviado: " + resposta);
        } catch (SocketTimeoutException e) {
            System.err.println("Timeout aguardando dados do cliente.");
        } catch (IOException e) {
            System.err.println("Erro na comunicação com cliente: " + e.getMessage());
        }
    }

private static String processarOperacao(String json) {
try {
String operacao = extrairValor(json, "operacao");
int num1 = Integer.parseInt(extrairValor(json, "num1"));
int num2 = Integer.parseInt(extrairValor(json, "num2"));
int resultado;
switch (operacao) {
case "SOMAR":
resultado = num1 + num2;
break;
case "SUBTRAIR":
resultado = num1 - num2;
break;
case "MULTIPLICAR":
resultado = num1 * num2;
break;
case "DIVIDIR":
if (num2 == 0) return respostaErro("Divisão por zero.");
resultado = num1 / num2;
break;
default:
return respostaErro("Operação inválida.");
}
return String.format("{\"status\":\"SUCESSO\",\"resultado\":%d,\"mensagem\":\"OK\"}", resultado);
} catch (Exception e) {
return respostaErro("Falha ao processar a requisição.");
}
}

private static String respostaErro(String mensagem) {
return String.format("{\"status\":\"ERRO\",\"resultado\":0,\"mensagem\":\"%s\"}", mensagem);
}

    // Parser propositalmente simplificado para fins didáticos.
    // Em uma aplicação real, deve-se utilizar uma biblioteca JSON.
    private static String extrairValor(String json, String chave) {
        Pattern pattern = Pattern.compile("\"" + chave + "\"\\s*:\\s*\"?([^,\"}]+)\"?");
        Matcher matcher = pattern.matcher(json);
        return matcher.find() ? matcher.group(1).trim() : "";
    }
}