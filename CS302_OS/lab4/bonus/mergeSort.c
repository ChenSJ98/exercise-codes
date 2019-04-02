#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
int N;// = 100000000;
const int maxT = 12;
int tNum = 1;
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
void mergeSort(int a[], int left, int right) {
  if(left == right)
    return;
  int mid = (left+right)>>1;
  mergeSort(a, left, mid);
  mergeSort(a, mid+1, right);
  merge(a, left, mid, right);
}

int main() {
  N = 20;
  int *a = (int*)malloc(sizeof(int)*N);
  srand(time(NULL));
  for(int i = 0; i < N; i++) {
    a[i] = rand()%20;
  }
  for (int i = 0; i < N ; i++) {
      printf("%d ", a[i]);
      //if(a[i] > a[i+1])
       // printf("answer wrong");
  }
  printf("\n");
  struct timespec t1, t2;
  clock_gettime(CLOCK_MONOTONIC, &t1);
  mergeSort(a,0,N-1);
  clock_gettime(CLOCK_MONOTONIC, &t2);
  float timecost = (t2.tv_sec - t1.tv_sec) + (t2.tv_nsec - t1.tv_nsec)*1.0/1000000000;
  printf("%d Numbers\n", N);
  printf("merge time cost:%f\n",timecost);
  for (int i = 0; i < N ; i++) {
      printf("%d ", a[i]);
      //if(a[i] > a[i+1])
       // printf("answer wrong");
  }
  free(a);
}
