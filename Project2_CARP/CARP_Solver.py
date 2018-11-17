import numpy as np
import time
from math import inf
from itertools import product
import ulusoy
import random
import sys
import copy
rvsProb = 0.6
sfProb = 0.7
pSize = 20
nSF = 2
file1 = "./data/egl-e1-A.dat"
file2 = "./data/egl-s1-A.dat"
file3 = "./data/gdb1.dat"
file4 = "./data/gdb10.dat"
file5 = "./data/val1A.dat"
file6 = "./data/val4A.dat"
file7 = "./data/val7A.dat"
file8 = "./data/test.dat"
class carp_solver:
    V = 0
    depot = 0
    reqE = 0
    nReqE = 0
    Capacity = 0
    cost = 0
    demand = 0
    edges = []
    tasks = []
    dist = []
    file = file2
    def floyd_warshall(self,n, edge):
        rn = range(n+1)
        dist = [[inf] * (n+1) for i in rn]
        nxt  = [[0]   * (n+1) for i in rn]
        for i in rn:
            dist[i][i] = 0
        for u, v, w in edge:
            dist[u][v] = w
            nxt[u][v] = v
        for k, i, j in product(rn, repeat=3):
            sum_ik_kj = dist[i][k] + dist[k][j]
            if dist[i][j] > sum_ik_kj:
                dist[i][j] = sum_ik_kj
                nxt[i][j]  = nxt[i][k]
        return dist
    def readData(self):
        f = open(self.file)
        f.readline()
        self.V = int(f.readline().split(' : ')[1])
        self.depot = int(f.readline().split(' : ')[1])
        self.reqE = int(f.readline().split(' : ')[1])
        self.nReqE = int(f.readline().split(' : ')[1])
        f.readline()
        self.Capacity = int(f.readline().split(' : ')[1])
        f.readline()
        f.readline()
        x = f.readline()
        self.cost = np.zeros((self.V+1,self.V+1),dtype = int)
        self.demand = np.zeros((self.V+1,self.V+1),dtype = int)
        while (x != 'END'):
            values = []
            for i in x[:len(x)-1].split(' '):
                if(i != ''):
                    values.append(int(i))
            self.cost[values[0]][values[1]] = values[2]
            self.cost[values[1]][values[0]] = values[2]
            self.demand[values[0]][values[1]] = values[3]
            self.demand[values[1]][values[0]] = values[3]
            self.edges.append([values[0],values[1],values[2]])
            self.edges.append([values[1],values[0],values[2]])
            if(values[3] != 0):
                self.tasks.append([values[0],values[1],values[3],values[2]])
            x = f.readline()
    
    def reverseTask(self, tasks, prab):
        taskList = copy.deepcopy(tasks)
        # stop = random.randint(0,len(taskList))
        i = 0
        # for task in taskList:
        length = len(taskList)
        i = random.randint(i, length)
        while(i < length):
            # if(random.random() < prab):
            task = taskList[i]
            t = task[0]
            task[0] = task[1]
            task[1] = t
            i = random.randint(i+1, length)
        return taskList
    def shuffle(self, tasks, sfNumber):
        size = len(tasks)
        for i in range(sfNumber):
            idx1 = random.randint(0,size-1)
            idx2 = random.randint(0,size-1)
            task = tasks[idx1]
            tasks[idx1] = tasks[idx2]
            tasks[idx2] = task
        return tasks

    def initPopulation(self, size, sfProb):
        length = len(self.tasks)
        population = []
        for i in range(size):
            newTask = self.reverseTask(self.tasks, rvsProb)
            if(random.random()<sfProb):
                newTask = self.shuffle(newTask, int(length/nSF))
            population.append(list(newTask))
        return population
    def genOffspring(self, population):
        pool = copy.deepcopy(population)
        random.shuffle(pool)
        size = len(population)
        length = len(population[0])
        offspring = []
        for i in range(int(size/2)):
            newTask = self.reverseTask(pool[i], rvsProb)
            if(random.random()<sfProb):
                newTask = self.shuffle(newTask, int(length/nSF))
            offspring.append(list(newTask))
        return offspring
        # pass
    def solve(self):
        self.readData()
        self.dist = self.floyd_warshall(self.V,self.edges)
        spliter = ulusoy.ulusoySpliter(self.dist, self.depot,self.Capacity)
        # while(True):
        random.shuffle(self.task)
        taskList = self.tasks
        minVal = inf
        
        population = (self.initPopulation(pSize,sfProb))
        population.append(self.tasks)
        path, score = spliter.split(self.tasks)
        print("initial score:", score)
        print("initial population:")
        records = []
        # results = []
        for i in range(1000):
            # records = []
            offspring = self.genOffspring(population)
            population += offspring
            # for p in population:
                # path, score = spliter.split(p)
                # minVal = min(score, minVal)
                # records.append((p,score))
            # print("generation ", i,' : ')
            # sorted(records, key = lambda record:record[1])
            # print(records)
            population.sort(key = lambda x:spliter.split(x)[1])
            population = population[:pSize]
            # records.sort(key = lambda x:x[1])
            # for r in records:
                # print(r[1])
            minVal = spliter.split(population[0])[1]
            print("gen ",i,": ", minVal)
            records.append(minVal)
            # print(self.genSolution(path,taskList)) 
            # print(score)
            self.reverseTask(taskList, rvsProb)
            # random.shuffle(taskList)

        print(minVal)
    def genSolution(self,path, taskList):
        solution = 's '
        for x in path:
            solution += '0,'
            for i in range(int((x[0]+1)/2),int(x[1]/2)+1):
                solution = solution + '(' + str(taskList[i-1][0]) + ','+str(taskList[i-1][1])+'),'
            solution += '0,'
        return solution[:len(solution)-1]
    def printPath(self,path, taskList):
        for i in range(len(path)):
            if (i % 2 == 0):
                path[i] = taskList[int(path[i]/2)-1][1]
            else:
                path[i] = taskList[int((path[i]+1)/2)-1][0]
if __name__ == "__main__":
    solver = carp_solver()
    if len(sys.argv) == 6:
        file_name = sys.argv[1]
        solver.file = file_name
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])
    time0 = time.time()
    solver.solve()