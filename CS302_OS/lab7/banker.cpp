#include<vector>
#include<iostream>
#include<stdio.h>
#include<map>
#include<string.h>
using namespace std;
int resourcesNum;
int processNum;
vector<int> finished;
vector<int> available;
vector<int*> allocated;
vector<int*> maxRequest;
vector<int*> want;

bool newProcess(int totalResources[]) {
    int ok = 1;
    int x[resourcesNum];
    for(int i = 0; i < resourcesNum; i++) {
        scanf("%d", &x[i]);
        if(x[i] > totalResources[i]) {
            printf("NOT OK\n");
            ok = 0;
        }
    }
    if(!ok)
        return false;
    finished.push_back(0);
    allocated.push_back(new int(resourcesNum));
    maxRequest.push_back(new int(resourcesNum));
    want.push_back(new int(resourcesNum));
    for(int i = 0; i < resourcesNum; i++) {
        maxRequest[processNum][i] = x[i];
        allocated[processNum][i] = 0;
        want[processNum][i] = x[i];
    }
    return true;
}
bool checkSafety() {
    bool checked[resourcesNum];
    for(int i = 0; i < resourcesNum; i++) {
        checked[i] = 0;
    }
    int allGet = 0;
    for(int k = 0; k < allocated.size(); k++) {
        for(int i = 0; i < allocated.size(); i++) {
            if(!checked[i]) {
                allGet = 1;
                for(int j = 0; j < resourcesNum; j++) {
                    if(want[i][j] > available[j])
                        allGet = 0;
                    }
                if(!allGet)
                    break;
                for(int j = 0; j < resourcesNum; j++)
                    available[j] += allocated[i][j];
                checked[i] = true;
            }
        }
    }
    for(int i = 0; i < allocated.size(); i++) {
        if(!checked[i])
            return false;
    }
    return true;
}

bool requestResource(int i, int request[]) {
    for(int j = 0; j < resourcesNum; j++) {
        if(allocated[i][j] + request[j] > maxRequest[i][j] || request[j] > available[j])
            return false;
    }

    for(int j = 0; j < resourcesNum; j++) {
        allocated[i][j] += request[j];
        available[j] -= request[j];
        want[i][j] -= request[j];
    }
    if(!checkSafety()) {
        for(int j = 0; j < resourcesNum; j++) {
            allocated[i][j] -= request[j];
            available[j] += request[j];
            want[i][j] += request[j];
        }
        return false;
    }
    return true;
}
int main() {
    processNum = 0;
    scanf("%d", &resourcesNum);
    int totalResources[resourcesNum];

    for(int i = 0; i < resourcesNum; i++) {
        scanf("%d",&totalResources[i]);
        available.push_back(totalResources[i]);
    }
    map<int, int> pidToIndex;
    int pid;
    char* opt;
    while(scanf("%d %s", &pid, opt) != EOF) {
        if(!strcmp(opt,"new")) {
            pidToIndex[pid] = processNum;
            if(newProcess(totalResources)) {
                processNum++;
                printf("OK\n");
            } else {
                printf("NOT OK\n");
            }
            
            
        }
        if(!strcmp(opt, "request")) {
            int requested[resourcesNum];
            for(int i = 0; i < resourcesNum; i++) {
                scanf("%d", &requested[i]);
            }
            if(requestResource(pidToIndex[pid], requested)) {
                printf("OK\n");
            } else {
                printf("NOT OK\n");
            }
        }
        if(!strcmp(opt, "terminate")) {
            finished[pidToIndex[pid]] = true;
            printf("OK\n");
        }

    }

}

