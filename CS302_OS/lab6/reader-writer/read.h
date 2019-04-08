#include"init.h"
void *reader(int *buffer){
    sem_wait(&rc); // acquire lock to change readcount
    readcount++;
    if(readcount == 1) { // I'm the first thread to read, block writer
        sem_wait(&db);
    }
    sem_post(&rc);    
    printf("\nReader Inside..%d\n", *buffer); 
    sem_wait(&rc);
    readcount--;
    if(readcount == 0) { // I'm the last thread that finishes reading, release write lock
        sem_post(&db);
    }
    sem_post(&rc);
}

