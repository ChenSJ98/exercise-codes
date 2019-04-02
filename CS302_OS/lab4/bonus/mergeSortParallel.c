#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
int N;// = 100000000;
const int maxT = 30;
int tNum = 0;
void merge(int a[], int left,int mid, int right) {
  int *b = (int*)malloc(sizeof(int)*(right-left+1));
  int i = left, j = mid+1, idx = 0;
  while(i <= mid || j <= right) {
    while((j == right+1 || a[i] <= a[j]) && i <= mid) {
      b[idx++] = a[i];
      i++;
    }
    while((a[j] < a[i] || i == mid + 1) && j <= right) {
      b[idx++] = a[j];
      j++;
    }
  }
  memcpy(a+left, b,(right-left+1)*sizeof(int));
  free(b);
}
typedef struct arg {
    int* a;
    int left;
    int right;
} arg;

void mergeSort(arg *args) {
  int *a = args->a;
  int left = args->left;
  int right = args->right;
  int mid = (left+right)>>1;
  if(left == right)
    return;
  arg arg1 = {a, left, mid};
  arg arg2 = {a, mid+1, right};
  
  pthread_t tid1, tid2;
  if(tNum >= 0 && tNum < maxT) {
    usleep(10);
    if(tNum >= 0 && tNum < maxT) {
      tNum += 2;
      printf("%d threads created", tNum);
      pthread_create(&tid1,NULL, (void*)mergeSort, &arg1);
      pthread_create(&tid2,NULL, (void*)mergeSort, &arg2);
      pthread_join(tid1,NULL);
      pthread_join(tid2,NULL);
      //tNum -= 2;
    } 
  }else {
      mergeSort(&arg1);
      mergeSort(&arg2);
    }
  merge(a, left, mid, right);
}

int main() {
  N = 200000000;
  int *a = (int*)malloc(sizeof(int)*N);
  srand(time(NULL));
  for(int i = 0; i < N; i++) {
    a[i] = rand()%20;
  }
  
  struct timespec t1, t2;
  clock_gettime(CLOCK_MONOTONIC, &t1);
  arg args = {a, 0, N-1};
  mergeSort(&args);
  clock_gettime(CLOCK_MONOTONIC, &t2);
  float timecost = (t2.tv_sec - t1.tv_sec) + (t2.tv_nsec - t1.tv_nsec)*1.0/1000000000;
  printf("%d Numbers\n", N);
  printf("%d Threads\n", maxT);
  printf("merge time cost:%f\n",timecost);
  
  free(a);
}
