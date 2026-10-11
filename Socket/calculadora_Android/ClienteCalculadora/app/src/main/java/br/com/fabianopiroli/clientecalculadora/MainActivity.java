package br.com.fabianopiroli.clientecalculadora;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
public class MainActivity extends AppCompatActivity {
    private EditText edtNum1, edtNum2;
    private Button btnSomar;
    private Spinner spnOperacao;
    private TextView txtResultado;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private static final String IP_SERVIDOR = "192.168.6.183";
    private static final int PORTA = 9000;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        edtNum1 = findViewById(R.id.edtNum1);
        edtNum2 = findViewById(R.id.edtNum2);
        btnSomar = findViewById(R.id.btnCalcular);
        spnOperacao = findViewById(R.id.spnOperacao);
        txtResultado = findViewById(R.id.txtResultado);
        btnSomar.setOnClickListener(v -> {
            String n1 = edtNum1.getText().toString();
            String n2 = edtNum2.getText().toString();
            if (n1.isEmpty() || n2.isEmpty()) {
                Toast.makeText(this, "Informe os dois números.", Toast.LENGTH_SHORT).show();
                return;
            }
            String operacao = spnOperacao.getSelectedItem().toString();
            calcular(operacao, Integer.parseInt(n1), Integer.parseInt(n2));
        });
    }
    private void calcular(String operacao, int num1, int num2) {
        btnSomar.setEnabled(false);
        txtResultado.setText("Calculando...");
        executor.execute(() -> {
            try (Socket socket = new Socket(IP_SERVIDOR, PORTA);
                 PrintWriter saida = new PrintWriter(socket.getOutputStream(), true);
                 BufferedReader entrada = new BufferedReader(new InputStreamReader(
                         socket.getInputStream(), StandardCharsets.UTF_8))) {
                String requisicao = String.format(
                        "{\"operacao\":\"%s\",\"num1\":%d,\"num2\":%d}",
                        operacao, num1, num2);
                saida.println(requisicao);

                String resposta = entrada.readLine();
                if (resposta == null) {
                    throw new IOException("Servidor encerrou a conexão sem responder.");
                }
                int resultado = extrairResultado(resposta);
                runOnUiThread(() -> {
                    txtResultado.setText("Resultado: " + resultado);
                    btnSomar.setEnabled(true);
                });
            } catch (IOException e) {
                runOnUiThread(() -> {
                    txtResultado.setText("Erro ao conectar ao servidor.");
                    btnSomar.setEnabled(true);
                });
            }

        });
    }

    private int extrairResultado(String resposta) throws IOException {
        Matcher matcher = Pattern.compile("\"resultado\"\\s*:\\s*(-?\\d+)").matcher(resposta);
        if (!matcher.find()) {
            throw new IOException("Resposta inválida do servidor: " + resposta);
        }
        return Integer.parseInt(matcher.group(1));
    }

    @Override
    protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }
}