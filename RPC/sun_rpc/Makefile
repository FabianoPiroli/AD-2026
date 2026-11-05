# Configurações do compilador e flags da biblioteca moderna
CC = gcc
CFLAGS = -g -Wall -I/usr/include/tirpc
LIBS = -ltirpc

# Arquivos gerados automaticamente pelo rpcgen
RPCGEN_FILES = calculadora.h calculadora_clnt.c calculadora_svc.c calculadora_xdr.c

all: calculadora_server calculadora_client

# Passo 1: Invoca o rpcgen moderno gerando código seguro (-M) e ANSI C (-C)
$(RPCGEN_FILES): calculadora.x
	rpcgen -C -M calculadora.x

# Passo 2: Compila o Servidor
calculadora_server: calculadora_server.o calculadora_svc.o calculadora_xdr.o
	$(CC) -o $@ $^ $(LIBS)

# Passo 3: Compila o Cliente
calculadora_client: calculadora_client.o calculadora_clnt.o calculadora_xdr.o
	$(CC) -o $@ $^ $(LIBS)

# Regra padrão para compilação de objetos
%.o: %.c calculadora.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o calculadora_server calculadora_client $(RPCGEN_FILES)
