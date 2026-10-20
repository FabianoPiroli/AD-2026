#include <pthread.h>
#include <stdio.h>

void* func() { printf("Thread em C!\n"); return NULL; }

int main() {
    pthread_t t;
    pthread_create(&t, NULL, func, NULL);
    pthread_join(t, NULL); // Aguarda a thread terminar
}
