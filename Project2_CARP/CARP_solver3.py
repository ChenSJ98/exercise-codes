import numpy as np
import time
from math import inf
from itertools import product
# import ulusoy
import random
import sys
import copy
# import matplotlib.pyplot as pt
rvsProb = 0.8
sfProb = 0.8
pSize = 100
nSF = 3
backProb = 0
N = 500
timeout = 100
file1 = "./data/egl-e1-A.dat"
file2 = "./data/egl-s1-A.dat"
file3 = "./data/gdb1.dat"
file4 = "./data/gdb10.dat"
file5 = "./data/val1A.dat"
file6 = "./data/val4A.dat"
file7 = "./data/val7A.dat"
file8 = "./data/test.dat"
time0 = time.time()
class ulusoySpliter:
    dist = []
    Capacity = 0
    depot = 0
    tasks = []
    def __init__(self,  dist, depot, capacity, tasks):
        self.dist = dist
        self.tasks = tasks
        self.depot = depot
        self.Capacity = capacity
    def toDirectedGraph(self, taskList, depot,dist):
        length = len(taskList)
        DG = np.full((2*length+1,2*length+1),inf)
        incoming = []
        outgoing = []
        for i in range (2*length+1):
            incoming.append([])
            outgoing.append([])
        for i in range(length):
            load = 0
            x = 2*i+1
            task = taskList[i]
            cost = dist[self.depot][task[0]] + task[3] + dist[task[1]][self.depot]
            DG[x][x+1] = cost
            incoming[x+1].append([x,x+1,cost])
            outgoing[x].append([x,x+1,cost])
            if(x > 1):
                incoming[x].append([x-1,x,0])
                outgoing[x-1].append([x-1,x,0])
            load = task[2]
            cost = dist[self.depot][task[0]] + task[3]
            j = i + 1
            while(True):
                if(j == length):
                    j -= 1
                    break
                if(load + taskList[j][2] <= self.Capacity):
                    load += taskList[j][2]
                    cost += dist[taskList[j-1][1]][taskList[j][0]] + taskList[j][3]
                    DG[x][2*j+2] = cost+dist[taskList[j][1]][self.depot]
                    incoming[2*j+2].append([x,2*j+2,DG[x][2*j+2]])
                    outgoing[x].append([x,2*j+2,DG[x][2*j+2]])
                    j += 1
                    
                else:
                    j -= 1
                    break
            cost += dist[taskList[j][1]][depot]
            DG[x][2*j+2] = cost
            incoming[2*j+2][len(incoming[2*j+2]) - 1 ] = [x,2*j+2,cost]
            outgoing[x][len(outgoing[x]) - 1]=[x,2*j+2,cost]
        return DG, incoming, outgoing
    def getPath(self, DG, incoming, outgoing):
        # print("call getPath")
        # print(len(DG))
        nodeCost=[0]*(len(DG)+1)
        bestPath = [[]]*(len(DG)+1)
        bestPath[1] = []
        for i in range(1,len(DG)):
            minCost = inf
            bestEdge =[]
            # find incoming edge with min cost
            if(i > 1):
                for edge in incoming[i]:
                    if(edge[2] < minCost):
                        minCost = edge[2]
                        bestEdge = edge
                if(i%2 == 0):
                    preBestPath = list(bestPath[bestEdge[0]])
                    preBestPath.append([bestEdge[0],bestEdge[1]])
                    bestPath[i] = preBestPath
                else:
                    bestPath[i] = bestPath[i-1]
            else:
                minCost = 0
            nodeCost[i] += minCost
            # release node, update outgoing edge
            for edge in outgoing[i]:
                index = incoming[edge[1]].index(edge)
                edge[2] += nodeCost[i]
                incoming[edge[1]][index] = edge
        return bestPath[len(DG)-1], nodeCost[len(DG)-1]
    def split(self,p):
        tasks = []
        for x in p:
            tasks.append(self.tasks[x])
        DG, incoming, outgoing = self.toDirectedGraph(tasks,self.depot,self.dist)
        path, score = self.getPath(DG,incoming, outgoing)
        return path, score
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
    file = file4
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
            distance = self.dist[current][task[0]]
            if(distance < minDist):
                ans.clear()
                ans.append(x)
                minDist = distance
            elif(distance == minDist):
                ans.append(x)
        
        index = random.randint(0,len(ans)-1)
        return ans[index]
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
            depot = self.tasks[solution[len(solution)-1]][1]
        return solution
    def reverseTask(self, tasks, prab):
        p = copy.deepcopy(tasks)
        i = 0
        length = len(p)
        i = random.randint(i, length)
        while(i < length):
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
            
            self.spliter = ulusoySpliter(self.dist, self.depot,self.Capacity,self.tasks)
            path, score = self.spliter.split(sol)
            # print("scan score: ", score, " compute score: ", self.genSolution(path,sol )[1])
            population.append([sol, path, score])
        records = []
        
        for i in range(N):
            offspring = self.genOffspring(population)
            population += offspring

            population.sort(key = lambda x:x[2])
            population1 = population[:int(pSize*0.5)]
            population1 += population[int(0.9*pSize):int(1.4*pSize)]
            population = population1
            
            minVal = population[0][2]
            maxVal = population[len(population)-1][2]
            # print("gen ",i,": ", minVal,"----------",maxVal)#, " --- ", path, " with ",population[0])
            records.append(minVal)
            if(time.time()-time0 > timeout):
                break
        bestSolution = population[0]
        # print("best solution:", bestSolution)
        # print("solution length: ", len(bestSolution))
        # print("set length: ", len(set(bestSolution)))
        finalSolution = self.genSolution(population[0][1],population[0][0])
        print(finalSolution[0])
        print(finalSolution[1])
    def genSolution(self,path, taskList):
        taskList = [0]+taskList
        # print("path: ", path, "taskList: ", len(taskList))
        cost = 0
        solution = 's '
        # print("depot: ",self.depot)
        for x in path:
            # print()
            solution += '0,'
            cost += self.dist[self.depot][self.tasks[taskList[int((x[0]+1)/2)]][0]]
            for i in range(int((x[0]+1)/2),int(x[1]/2)+1):
                task = self.tasks[taskList[i-1]]
                solution = solution + '(' + str(task[0]) + ','+str(task[1])+'),'
                
                cost += task[3]
                if(i -int((x[0]+1)/2)> 0):
                    # print("pre: ", self.tasks[taskList[i-2]],"task: ", task )
                    # print("##",self.tasks[taskList[i-2]][1]," , ",task[0],"##: ",self.dist[self.tasks[taskList[i-2]][1]][task[0]])
                    cost+=self.dist[self.tasks[taskList[i-2]][1]][task[0]]
            cost += self.dist[self.depot][self.tasks[taskList[int(x[1]/2)-1]][1]]    
            solution += '0,'
        return solution[:len(solution)-1], cost
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
        timeout = time_limit
        seed = int(sys.argv[5])
    time0 = time.time()
    solver.solve()