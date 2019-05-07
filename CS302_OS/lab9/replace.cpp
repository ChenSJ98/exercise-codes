/**
 * By Shijie Chen   id:11612028  
 * Usage: input format should conform with 1.in. Just use a file and redirection(<).
 * e.g. g++ replace.cpp && ./a.out < 1.in
 */
#include <iostream>
#include <stdio.h>
#include <map>
#include <unordered_map> // require C++11
#include <unordered_set> // require C++11
#include <list>
using namespace std;
int totalSize;
int algorithm;

double FIFO(){
    int N;
    scanf("%d", &N);
    int hitNum = 0; // Number of page hits.
    int fifoSize = 0; // Size of fifo list to determine if fifo list is full.
    list<int> fifoList; // The fifo list.
    unordered_set<int> fifoSet; // Used to determine page hit in O(1) time.
    
    int x;
    for (int i = 0; i < N; i++) {
        scanf("%d", &x);
        if(fifoSet.find(x) == fifoSet.end()) {
            // page miss
            if(fifoSize < totalSize) {
                // add
                fifoList.push_back(x);
                fifoSet.insert(x);
                fifoSize++;
            } else {
                // replace
                fifoSet.erase(fifoList.front());
                fifoList.pop_front();
                fifoList.push_back(x);
                fifoSet.insert(x);
            }
        } else {
            // page hit
            hitNum++;
        }
    }
    return hitNum * 1.0 / N;
}

double Min(){
    int N;
    scanf("%d", &N);
    int hitNum = 0;
    int minSize = 0;
    int pages[N];
    unordered_set<int> set;
    unordered_map<int, list<int> > map;
    for(int i = 0; i < N; i++) {
        scanf("%d", &pages[i]);
        map[pages[i]].push_back(i);
    }
    int max;
    int toBeReplaced, gap, next;
    for(int i = 0; i < N; i++) {
        if(set.find(pages[i]) != set.end()) {
            // page hit
            hitNum++;
        } else {
            // page miss
            if(minSize == totalSize) {
                unordered_set<int>::iterator iter;
                max = 0;
                for(iter = set.begin(); iter != set.end(); ++iter) {
                    next = map[*iter].begin() == map[*iter].end()? N - 1 : map[*iter].front();
                    gap = next - i;
                    if (gap > max) {
                        toBeReplaced = *iter;
                        max = gap;
                    }
                }
                set.erase(toBeReplaced);                
            } else {
                minSize++;
            }
        }
        set.insert(pages[i]);
        map[pages[i]].pop_front();
    }
    return hitNum * 1.0 / N;
}
double LRU(){
    int N;
    scanf("%d", &N);
    int hitNum = 0;
    int x;
    list<int> LRUlist;
    unordered_set<int> set;
    unordered_map<int, list<int>::iterator> map;
    int LRUsize = 0;
    list<int> :: iterator iter;
    for(int i = 0; i < N; i++) {
        scanf("%d", &x);
        if(set.find(x) != set.end()) {
            // page hit
            LRUlist.remove(x);
            LRUlist.push_front(x);
            hitNum++;
        } else {
            // page miss
            if(LRUsize == totalSize) {
                set.erase(LRUlist.back());
                LRUlist.pop_back();
            } else {
                LRUsize++;
            }
            set.insert(x);
            LRUlist.push_front(x);
        }
    }
    return hitNum * 1.0 / N;
}

double Clock(){
    int N;
    scanf("%d", &N);
    int list[totalSize];
    int valid[totalSize];
    memset(valid, 0, sizeof(valid));
    int hand = 0;
    unordered_set<int> set;
    unordered_map<int, int> map;
    int clockSize = 0;
    int hitNum = 0;
    int x;
    for(int i = 0; i < N; i++) {
        scanf("%d", &x);
        if(set.find(x) == set.end()) {
            // page miss
            if(clockSize < totalSize) {
                // not full
                map[x] = hand;
                valid[clockSize] = 1;
                list[clockSize++] = x;
                
                hand++;
                hand = hand % totalSize;
                set.insert(x);
            } else {
                // replace
                while(valid[hand]) {
                    valid[hand] = 0;
                    hand++;
                    hand = hand % totalSize;
                }
                valid[hand] = 1;
                set.erase(list[hand]);
                list[hand] = x;
                map[x] = hand;
                set.insert(x);
                hand++;                
                hand = hand % totalSize;
            }
        } else {
            // page hit
            hitNum++;
            valid[map[x]] = 1;
        }
        
    }
    return hitNum * 1.0 / N;
}

double Second_chance(){
    int N;
    scanf("%d", &N);
    int hitNum = 0;
    int x;

    int fifoTotalSize = totalSize / 2;
    int LRUTotalsize = totalSize - fifoTotalSize;
    int fifoSize = 0;
    int LRUsize = 0;

    unordered_set<int> fifoSet;
    unordered_set<int> LRUset;
    list<int> fifoList;
    list<int> LRUlist;
    int hitFifo, hitLRU;
    int t;
    for(int i = 0; i < N; i++) {
        scanf("%d", &x);
        hitFifo = fifoSet.find(x) != fifoSet.end();
        hitLRU = LRUset.find(x) != LRUset.end();
        if(!hitFifo && !hitLRU) {
            // page miss
            if(fifoSize < fifoTotalSize) { // fifo not full

                fifoList.push_back(x);
                fifoSet.insert(x);
                fifoSize++;
            } else { // fifo full
                // delete fifo front 
                t = fifoList.front();      
                fifoSet.erase(t);
                fifoList.pop_front();
                fifoList.push_back(x);
                fifoSet.insert(x);

                // add the deleted fifo front to LRU
                if(LRUsize == LRUTotalsize) {
                    LRUset.erase(LRUlist.back());
                    LRUlist.pop_back();
                } else {
                    LRUsize++;
                }
                LRUset.insert(t);
                LRUlist.push_front(t);
                
            }
            
        } else {
            // page hit
            hitNum++;
            if(hitLRU) {
                // delete LRU hit page and insert it into fifo
                LRUset.erase(x);
                LRUlist.remove(x);
                fifoList.push_back(x);
                fifoSet.insert(x);

                // delete fifo front 
                t = fifoList.front();      
                fifoSet.erase(t);
                fifoList.pop_front();

                // add the deleted fifo front to LRU
                LRUlist.push_front(t);
                LRUset.insert(t);
            }
        }
    }
    return hitNum * 1.0 / N;
}

int main() {
    scanf("%d", &totalSize);
    scanf("%d", &algorithm);
    switch(algorithm) {
        case 0 : printf("Hit ratio = %.2f%%\n", 100 * FIFO()); break;
        case 1 : printf("Hit ratio = %.2f%%\n", 100 * LRU()); break;
        case 2 : printf("Hit ratio = %.2f%%\n", 100 * Min()); break;
        case 3 : printf("Hit ratio = %.2f%%\n", 100 * Clock()); break;
        case 4 : printf("Hit ratio = %.2f%%\n", 100 * Second_chance()); break;
        default : break;
    }
}

