#include <stdio.h>
#include <stdlib.h>
#include "calculadora.h"

int main(int argc, char *argv[]) {
    char *host;
    CLIENT *clnt;
    enum clnt_stat status;
    entrada_soma argumentos;
    int resultado;

    if (argc < 4) {
        fprintf(stderr, "Uso: %s <host> <num1> <num2>\n", argv[0]);
        exit(1);
    }
    host = argv[1];
    argumentos.a = atoi(argv[2]);
    argumentos.b = atoi(argv[3]);

    /* Cria o cliente RPC usando o protocolo UDP (TI-RPC integrado) */
    clnt = clnt_create(host, CALC_PROG, CALC_VERS, "udp");
    if (clnt == NULL) {
        clnt_pcreateerror(host);
        exit(1);
    }

    /* Chama o stub gerado pelo rpcgen usando a assinatura thread-safe */
    status = somar_1(&argumentos, &resultado, clnt);
    
    if (status != RPC_SUCCESS) {
        clnt_perror(clnt, "Falha na chamada RPC");
        clnt_destroy(clnt);
        exit(1);
    }

    printf("Resposta recebida do servidor: %d + %d = %d\n", argumentos.a, argumentos.b, resultado);

    clnt_destroy(clnt);
    return 0;
}
