#include"init.h"

void *writer(int *buffer){
    sem_wait(&db); // acquire write lock
    (*buffer)++;
    printf ("write ::%d\n", *buffer);
    sem_post(&db); // release write lock
}

