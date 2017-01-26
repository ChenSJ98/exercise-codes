#include <stdio.h>
#include<math.h>
int add(int base, int a){
  int sum=base;
  while (sum+a>0){
    sum+=a;
}
  return sum;
    }
int main(){
  int sum,base=1;
  while (10*base>0) {base*=10;};
  sum=base;
  do{
    sum=add(sum,base);
    base=base/10;
  }while (base>=1);
  printf("%d\n",sum);
  return 0; 
}
