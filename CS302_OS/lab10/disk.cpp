#include <stdio.h>
#include <math.h>
#include <algorithm>
using namespace std;
void FCFS(int start, int a[], int nRequest);
void SSTF(int start, int a[], int nRequest, int nTrack);
void SCAN(int start, int a[], int nRequest);
void C_SCAN(int start, int a[], int nRequest, int nTrack);
void LOOK(int start, int a[], int nRequest);
void C_LOOK(int start, int a[], int nRequest);
int main() {
    int startTrack, nTrack, nRequest;
    scanf("%d %d %d", &startTrack, &nTrack, &nRequest);
    int a[nTrack];
    for(int i = 0; i < nRequest; i++) {
        scanf("%d", &a[i]);
    }
    FCFS(startTrack, a, nRequest);
    SSTF(startTrack, a, nRequest, nTrack);
    SCAN(startTrack, a, nRequest);
    C_SCAN(startTrack, a, nRequest, nTrack);
    LOOK(startTrack, a, nRequest);
    C_LOOK(startTrack, a, nRequest);
    return 0;
}
int getDistance(int a, int b) {
    return (int)abs((double)(a - b));
}

int next(int index, int len) {
    if(index == len - 1) {
        return 0;
    } else {
        return ++index;
    }
}

int pre(int index, int len) {
    if (index == 0)
        return len - 1;
    else
        return --index;
    
}

void FCFS(int start, int a[], int nRequest) {
    printf("FCFS\n");
    int total = 0;
    printf("%d ", start);
    for(int i = 0; i < nRequest; i++) {
        printf("-> %d ", a[i]);
        total += getDistance(start, a[i]);
        start = a[i];
    }
    printf ("\n%d\n", total);
}

void SSTF(int start, int a[], int nRequest, int nTrack) {
    printf("SSTF\n");
    int total = 0;
    printf("%d", start);
    int i1 = 0, i2 = 1;
    int d1, d2;
    int min = nTrack;
    int startPos = 0;
    sort(a, a + nRequest);
    for(int i = 0; i < nRequest; i++) {
        if (getDistance(a[i], start) < min) {
            startPos = i;
            min = getDistance(a[i], start);
        }
    }

    if(a[startPos] < start) {
        i1 = startPos;
    } else {
        i1 = startPos - 1;
    }
    i2 = i1 + 1;
    
    for(int i = 0; i < nRequest; i++) {
        d1 = getDistance(start, a[i1]);
        d2 = getDistance(start, a[i2]);
        if(i1 >= 0 && d1 < d2) {
            start = a[i1];
            i1 --;
            total += d1;
        } else {
            start = a[i2];
            i2++;
            total += d2;
        }
        printf(" -> %d", start);
    }
    printf ("\n%d\n", total);
}

void SCAN(int start, int a[], int nRequest) {
    printf("SCAN\n");
    int total = 0;
    printf("%d", start);
    sort(a, a + nRequest);
    int max, startPos, i1, i2;
    for(int i = 0; i < nRequest; i++) {
        if(a[i] <= start && start < a[i + 1]) {
            startPos = i;
        }
    }

    for (int i = startPos; i > -1; i--) {
        printf(" -> %d", a[i]);
    }
    printf(" -> %d", 0);
    for(int i = startPos + 1; i < nRequest; i++) {
        printf(" -> %d", a[i]);
    }

    total = start + a[nRequest - 1];
    printf ("\n%d\n", total);
}

void C_SCAN(int start, int a[], int nRequest, int nTrack) {
    printf("C-SCAN\n");
    int total = 0;
    printf("%d", start);
    sort(a, a + nRequest);
    int max, startPos, i1, i2;
    for(int i = 0; i < nRequest; i++) {
        if(a[i] <= start && start < a[i + 1]) {
            startPos = i;
        }
    }

    for (int i = startPos; i > -1; i--) {
        printf(" -> %d", a[i]);
    }
    printf(" -> %d", 0);
    printf(" -> %d", nTrack - 1);
    for(int i = nRequest - 1; i > startPos; i--) {
        printf(" -> %d", a[i]);
    }

    total = nTrack - (a[startPos + 1] - start) - 1;
    printf ("\n%d\n", total);
}

void LOOK(int start, int a[], int nRequest) {
    printf("LOOK\n");
    int total = 0;
    printf("%d", start);
    sort(a, a + nRequest);
    int max, startPos, i1, i2;
    for(int i = 0; i < nRequest; i++) {
        if(a[i] <= start && start < a[i + 1]) {
            startPos = i;
        }
    }

    for (int i = startPos; i > -1; i--) {
        printf(" -> %d", a[i]);
    }
    for(int i = startPos + 1; i < nRequest; i++) {
        printf(" -> %d", a[i]);
    }

    total = start - a[0] + a[nRequest - 1] - a[0];
    printf ("\n%d\n", total);
}

void C_LOOK(int start, int a[], int nRequest) {
    printf("C-LOOK\n");
    int total = 0;
    printf("%d", start);
    sort(a, a + nRequest);
    int max, startPos, i1, i2;
    for(int i = 0; i < nRequest; i++) {
        if(a[i] <= start && start < a[i + 1]) {
            startPos = i;
        }
    }

    for (int i = startPos; i > -1; i--) {
        printf(" -> %d", a[i]);
    }
    for(int i = nRequest - 1; i > startPos; i--) {
        printf(" -> %d", a[i]);
    }

    total = start - a[0] + a[nRequest - 1] - a[startPos + 1];
    printf ("\n%d\n", total);
}


