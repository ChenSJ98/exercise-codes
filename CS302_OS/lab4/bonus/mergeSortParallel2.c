#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include <math.h>
int N;
const int maxT = 8;
int tNum = 0;

typedef struct arg {
    int* a;
    int left;
    int mid; // In mergesort(), mid is not used and set to 0.
    int right;
} arg; 

void merge(arg *args) {
  int *a = args->a;
  int left = args->left;
  int mid = args->mid;
  int right = args->right;

  // Put temp array on the heap to prevent stack overflow
  int *b = (int*)malloc(sizeof(int)*(right-left+1));
  int i = left, j = mid+1, idx = 0;

  // Merge a[left...mid] and a[mid + 1...right]
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


void mergeSort(arg *args) {
  int *a = args->a;
  int left = args->left;
  int right = args->right;
  int mid = (left+right)>>1;
  if(left == right)
    return;
  arg arg1 = {a, left, 0, mid};
  arg arg2 = {a, mid+1, 0, right};
  
  mergeSort(&arg1);
  mergeSort(&arg2);
  arg arg3 = {a, left, mid, right};
  merge(&arg3);
}



int main() {
  // generate N random integers
  N = 200000000;
  int *a = (int*)malloc(sizeof(int)*N);
  srand(time(NULL));
  for(int i = 0; i < N; i++) {
    a[i] = rand();
  }

  struct timespec t1, t2;
  clock_gettime(CLOCK_MONOTONIC, &t1);

  // Partition the input array and create maxT threads. Assume the number of integers to be sorted is way larger than maxT. 
  int depth = (int)log2(maxT);
  depth += maxT > pow(2, depth) ? 1:0;
  int interval = N / maxT;
  pthread_t threads[maxT];

  // Here an array of args is used to prevent synchronization issues of parameters between threads.
  arg ag[maxT];
  for(int i = 0; i < maxT - 1; i++) {
    ag[i].a = a;
    ag[i].left = i*interval;
    ag[i].right = (i+1)*interval-1;
    ag[i].mid = 0;
    pthread_create(&threads[i], NULL, (void*) mergeSort, &ag[i]);
  }

  // The last partition goes to the end of the array.
  int i = maxT - 1;
  ag[i].a = a;
  ag[i].left = i*interval;
  ag[i].right = N - 1;
  ag[i].mid = 0;
  pthread_create(&threads[i], NULL, (void*) mergeSort, &ag[i]);
  for(int i = 0; i < maxT; i++) {
    pthread_join(threads[i], NULL);
  }

  // Merge results from the created threads.
  for(int i = depth - 1; i >=0; i--) {
    int step = maxT / pow(2, i);
    for(int j = 0; j < pow(2, i); j++) {
      int right = (j == pow(2,i) - 1)? N - 1:((j+1)*step*interval - 1);    
      ag[j].a = a;
      ag[j].left = j*step*interval;
      ag[j].right = right;
      ag[j].mid = (j == pow(2,i) - 1)? j*step*interval + step/2*interval -1:(j*step*interval + right) >> 1;
      pthread_create(&threads[j], NULL, (void*) merge, &ag[j]);
    }
    for(int j = 0; j < pow(2,i); j++) {
      pthread_join(threads[j], NULL);
    }
  }
  
  // Calculate time elapsed and output.
  clock_gettime(CLOCK_MONOTONIC, &t2);
  float timecost = (t2.tv_sec - t1.tv_sec) + (t2.tv_nsec - t1.tv_nsec)*1.0/1000000000;
  printf("%d Numbers\n", N);
  printf("%d Threads\n", maxT);
  printf("merge time cost:%f\n",timecost);
  
  free(a);
}
