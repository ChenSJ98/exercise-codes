#include <unistd.h>
#include <stdio.h>
int main(){
  setbuf(stdout,NULL);
  //printf("pid of this process: %d\n",getpid());
  printf("A");
  fork();
  printf("B");
  fork();
  printf("C");
  //while(1){}

  /*
  if(fork()) {
    printf("this is the child process, pid: %d\n", getpid());
  } else {
    printf("this is the parent process, pid: %d\n", getpid());
  }
  */
  return 0;
}
