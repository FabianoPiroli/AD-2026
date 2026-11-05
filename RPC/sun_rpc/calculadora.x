/* Estrutura que encapsula os dois parâmetros de entrada */
struct entrada_soma {
    int a;
    int b;
};

/* Definição do programa RPC */
program CALC_PROG {
    version CALC_VERS {
        int SOMAR(entrada_soma) = 1; /* Procedimento número 1 */
    } = 1;                           /* Versão do programa 1 */
} = 99;                              /* Número do programa */
