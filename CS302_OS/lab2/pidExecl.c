#include <stdio.h>
#include <unistd.h>
int main() {
  printf("PID of current program = %d\n",getpid());
  // if(!fork())
  int subpid = fork();
  if(!subpid){
    execl("/bin/ls","/bin/ls",NULL);
    printf("11612028 Shijie Chen");}
  else {
  wait(subpid);
  printf("back to caller\n");


  }  return 0;
}
