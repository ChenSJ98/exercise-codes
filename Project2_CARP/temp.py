import numpy as np
import time
from math import inf
from itertools import product
import ulusoy
import random
import sys
import copy
import matplotlib.pyplot as pt
rvsProb = 0.3
sfProb = 0.9
pSize = 100
nSF = 4
backProb = 0.1
N = 10
timeout = 10
file1 = "./data/egl-e1-A.dat"
file2 = "./data/egl-s1-A.dat"
file3 = "./data/gdb1.dat"
file4 = "./data/gdb10.dat"
file5 = "./data/val1A.dat"
file6 = "./data/val4A.dat"
file7 = "./data/val7A.dat"
file8 = "./data/test.dat"
time0 = time.time()
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
    spliter =0
    searched = set()
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
                self.tasks.append([values[1],values[0],values[3],values[2]])
            x = f.readline()        
    def getTask(self, current, undone):
        minDist = inf
        ans = []
        for x in undone:
            task = self.tasks[x]
            # print("depot: ", current, " task: ", task)
            distance = self.dist[current][task[0]]
            if(distance < minDist):
                ans.clear()
                ans.append(x)
                minDist = distance
            elif(distance == minDist):
                ans.append(x)
        
        index = random.randint(0,len(ans)-1)
        return ans[index]
        # print("ans)
        pass
 # path scanning
    def scan(self):
        length = len(self.tasks)
        undone = list(range(0, length))
        solution = []
        nextT = 0
        depot = self.depot
        load = 0
        while(len(undone)>0):
            nextT = self.getTask(depot, undone)
            newTask = self.tasks[nextT]
            if(load + newTask[2] < self.Capacity):
                load += newTask[2]
            else:
                if(random.random() < backProb):
                    depot = self.depot
                    load = 0
                    continue
            solution.append(nextT)
            load += self.tasks[nextT][3]
            if(nextT % 2 == 0):
                x1 = nextT
                x2 = nextT + 1
                undone.remove(x1)
                undone.remove(x2)
            else:
                x1 = nextT
                x2 = nextT - 1
                undone.remove(x1)
                undone.remove(x2)
            '''
            if(load > self.Capacity*0.7):
                
                    depot = self.depot
                    load = 0
                    continue
            '''
            depot = self.tasks[solution[len(solution)-1]][1]
        # print("scanned solution:", solution)
        return solution
 
    # genetic operators
    def reverseTask(self, tasks, prab):
        p = copy.deepcopy(tasks)
        # print("p:",p)
        # stop = random.randint(0,len(taskList))
        i = 0
        # for task in taskList:
        length = len(p)
        i = random.randint(i, length)
        while(i < length):
            # if(random.random() < prab):
            if(p[i]%2 == 0):
                p[i] += 1
            else:
                p[i] -= 1
            i = random.randint(i+1, length)
        return p
    def shuffle(self, tasks, path):
        size = len(path)
        sfNumber = random.randint(0,size)
        for i in range(sfNumber):
            # switch routes for sfNumber times
            idx1 = random.randint(0,size-1)
            idx2 = random.randint(0,size-1)
            pathT = path[idx1]
            path[idx1] = path[idx2]
            path[idx2] = pathT
        newSeq = self.toSeq(path, tasks)
        return newSeq
    def toSeq(self,path, tasks):
        seq = []
        for x in path:
            for i in range(int((x[0]-1)/2),int(x[1]/2)):
                seq.append(tasks[i])
        # print("seq: ", seq)
        return seq
    def genRandSequence(self, size):  
        seq = []
        for i in range(0,size,2):
            if(random.random()<0.5):
                seq.append(i)
            else:
                seq.append(i+1)
        random.shuffle(seq)
        while(tuple(seq) in self.searched):
            seq = []
            for i in range(0,size,2):
                if(random.random()<0.5):
                    seq.append(i)
                else:
                    seq.append(i+1)
            random.shuffle(seq)
        self.searched.add(tuple(seq))
        return seq

    def initPopulation(self, size, sfProb):
        length = len(self.tasks)
        population = []
        newTask = range(0, length, 2)
        tpath, tscore = self.spliter.split(newTask)
        population.append([list(newTask),tpath, tscore])
        for i in range(size):
            newTask = self.genRandSequence(length)
            tpath, tscore = self.spliter.split(newTask)
            population.append([list(newTask),tpath, tscore])
        return population
    def genOffspring(self, population):
        pool = copy.deepcopy(population[:int(len(population)/2)])
        random.shuffle(pool)
        size = len(pool)
        
        offspring = []
        for i in range(size):
            child = copy.deepcopy(pool[i]) 
            newTask = child[0]
            path = child[1]
            # print("----------------child", child)
            # print("off: ", newTask, path)
            #newTask = self.reverseTask(p[0], rvsProb)
            if(random.random()<sfProb):
                newTask = self.shuffle(newTask, path)
            else:
                newTask = self.reverseTask(newTask,rvsProb)
            tpath, tscore = self.spliter.split(newTask)
            offspring.append([list(newTask),tpath, tscore])
        return offspring
        # pass
    
    def solve(self):
        self.readData()
        self.dist = self.floyd_warshall(self.V,self.edges)
        population = []
        records = []
        for i in range(pSize):
            sol = self.scan()
            
            self.spliter = ulusoy.ulusoySpliter(self.dist, self.depot,self.Capacity,self.tasks)
            path, score = self.spliter.split(sol)
            records.append(score)
            population.append([sol, path, score])
        
        # population = self.initPopulation(pSize,sfProb)
        print("init solutions:")
        for x in records:
            print(x)
        print(population[0])
        print("initial score:", population[0][2])
        # print("initial population:")
        records = []
        # results = []
        
        for i in range(N):
            # records = []
            offspring = self.genOffspring(population)
            population += offspring

            population.sort(key = lambda x:x[2])
            population1 = population[:int(pSize*0.5)]
            population1 += population[int(0.9*pSize):int(1.4*pSize)]
            population = population1
            
            minVal = population[0][2]
            maxVal = population[len(population)-1][2]
            print("gen ",i,": ", minVal,"----------",maxVal)#, " --- ", path, " with ",population[0])
            records.append(minVal)
            if(time.time()-time0 > timeout):
                break
        print(self.genSolution(population[0][1],population[0][0]))
        print(minVal)
        l = len(records)
        xs = range(1,l+1,1)
        pt.plot(xs,records)
        pt.title(self.file)
        pt.show()
        
    def genSolution(self,path, taskList):
        solution = 's '
        for x in path:
            solution += '0,'
            for i in range(int((x[0]+1)/2),int(x[1]/2)+1):
                solution = solution + '(' + str(self.tasks[taskList[i-1]][0]) + ','+str(self.tasks[taskList[i-1]][1])+'),'
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