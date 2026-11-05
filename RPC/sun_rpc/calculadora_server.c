#include <stdio.h>
#include "calculadora.h"

/* Implementação do procedimento remoto com suporte multithread (-M) */
bool_t somar_1_svc(entrada_soma *argp, int *result, struct svc_req *rqstp) {
    printf("Servidor recebeu requisição: Somar %d + %d\n", argp->a, argp->b);
    
    /* Atribui o resultado diretamente no ponteiro seguro fornecido pelo stub */
    *result = argp->a + argp->b;
    
    /* Retorna TRUE para indicar que o procedimento foi executado com sucesso */
    return TRUE;
}

/* Função exigida pelo rpcgen para liberar memória caso houvesse estruturas dinâmicas */
int calc_prog_1_freeresult(SVCXPRT *transp, xdrproc_t xdr_result, caddr_t result) {
    xdr_free(xdr_result, result);
    return 1;
}
