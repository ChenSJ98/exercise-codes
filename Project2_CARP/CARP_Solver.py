import numpy as np
import time
from math import inf
from itertools import product
# import ulusoy
import random
import sys
import copy
# import matplotlib as pt
import matplotlib.pyplot as pt
rvsProb = 0.5
sfProb = 0.6
pSize = 800
nSF = 7
backProb = 0
N = 300000
timeout = 130
file1 = "./data/egl-e1-A.dat"
file2 = "./data/egl-s1-A.dat"
file3 = "./data/gdb1.dat"
file4 = "./data/gdb10.dat"
file5 = "./data/val1A.dat"
file6 = "./data/val4A.dat"
file7 = "./data/val7A.dat"
file8 = "./data/test.dat"
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
    file = file2
    spliter =0
    searched = set()
    def __init__(self,path):
        self.file = path
        
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
        self.V = 0
        self.depot = 0
        self.reqE = 0
        self.nReqE = 0
        self.Capacity = 0
        self.cost = 0
        self.demand = 0
        self.edges = []
        self.tasks = []
        self.dist = []
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
    # path scanning
    def scan(self):
        length = len(self.tasks)
        undone = list(range(0, length))
        solution = []
        nextT = 0
        load = 0
        depot = self.depot
        while(len(undone)>0):
            nextT = self.getTask(depot, undone)
            solution.append(nextT)
            # load += self.tasks[nextT][3]
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
        i = random.randint(i, length - 1)
        if(random.random()<0.2):
            while(i < length):
                if(p[i]%2 == 0):
                    p[i] += 1
                else:
                    p[i] -= 1
                i = random.randint(i+1, length)
        else:
            if(p[i]%2 == 0):
                    p[i] += 1
            else:
                p[i] -= 1
        return p
    def shuffle(self, tasks, path):
        size = len(path)
        sfNumber = random.randint(0,size)
        #for i in range(sfNumber):
            # switch routes for sfNumber times
        idx1 = random.randint(0,size-1)
        idx2 = random.randint(0,size-1)
        pathT = path[idx1]
        path[idx1] = path[idx2]
        path[idx2] = pathT
        newSeq = self.toSeq(path, tasks)
        return newSeq
    def shuffleByInsert(self,_tasks,path):
        if(random.random()<0.3):
            index = random.randint(0,len(path)-1)
            index2 = random.randint(0,len(path)-1)
            task = path[index]
            path.remove(task)
            path.insert(index2, task)
            return self.toSeq(path,_tasks)
        else:
            tasks = copy.deepcopy(_tasks)
            index = random.randint(0,len(tasks)-1)
            index2 = random.randint(0,len(tasks)-1)
            task = tasks[index]
            tasks.remove(task)
            tasks.insert(index2, task)
            return tasks
    def toSeq(self,path, tasks):
        seq = []
        for x in path:
            for i in range(int((x[0]-1)/2),int(x[1]/2)):
                seq.append(tasks[i])
        return seq
    
    def genOffspring(self, population):
        # pool = copy.deepcopy(population[:int(len(population)/2)])
        
        # random.shuffle(pool)
        size = int(len(population)/2)
        
        offspring = []
        for i in range(size):
            index = random.randint(0, len(population)-1)
            child = copy.deepcopy(population[index]) 
            newTask = child[0]
            path = child[1]
            if(random.random()<sfProb):
                if(random.random()<0.5):
                    if(random.random()<0.5):
                        newTask = self.shuffle(newTask, path)
                    else:
                        newTask = self.shuffleByInsert(newTask,path)
                else:
                    index = random.randint(0,len(newTask)-1)
                    t = newTask[index]
                    newTask.remove(t)
                    index1 = random.randint(0,len(newTask)-1)
                    newTask.insert(index1,t)

            else:
                newTask = self.reverseTask(newTask,rvsProb)
            tpath, tscore = self.spliter.split(newTask)
            offspring.append([list(newTask),tpath, tscore])
        return offspring
        # pass
    
    def solve(self):
        time0 = time.time()
        self.readData()
        self.dist = self.floyd_warshall(self.V,self.edges)
        pSize = self.reqE*10
        # print("solve, ",pSize)
        

        population = []
        records = []
        for i in range(pSize):
            sol = self.scan()
            #random.shuffle(sol)
            self.spliter = ulusoySpliter(self.dist, self.depot,self.Capacity,self.tasks)
            path, score = self.spliter.split(sol)
            population.append([copy.deepcopy(sol), path, score])
        population.sort(key = lambda x:x[2])
        population = population[:pSize]
        records = []
        mrecords = []
        minVal = population[0][2]
        maxVal = population[len(population)-1][2]
        print(self.file.split()[-1],'  size:', pSize)
        for i in range(N):
            minVal = population[0][2]
            maxVal = population[len(population)-1][2]
            print(time.time()-time0,"  gen ",i,": ", minVal,"----------",maxVal)
            
            offspring = self.genOffspring(population)
            population += offspring
            population.sort(key = lambda x:x[2])
            population1 = population[:int(pSize)]
            population = population1
            
            mrecords.append(maxVal)
            records.append(minVal)
            if(time.time()-time0 > timeout-15):
                break
        # print(self.genSolution(population[0][1],population[0][0]))
        # print('q ',minVal)
        print("time:",time.time()-time0)

        return minVal
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

    # if len(sys.argv) == 6:
    #     file_name = sys.argv[1]
    #     solver = carp_solver()
    #     solver.file = file_name
    #     time_limit = int(sys.argv[3])
    #     timeout = time_limit
    #     seed = int(sys.argv[5])
    #     random.seed(seed)
    # xs =[]
    # records = []
    # carp_solver.readData(carp_solver)
    # carp_solver.dist = carp_solver.floyd_warshall(carp_solver,carp_solver.V,carp_solver.edges)
    # solver = carp_solver()
    # solver.solve()
    filenames = ["./data/dataset/val10C.dat"]
    
    for filename in filenames:
        minv = inf
        maxv = -inf
        
        # solver.file = filename
        for i in range(1):
            solver = carp_solver(filename)
            x = solver.solve()
            print(i,": ",x)
            minv = min(x,minv)
            maxv = max(x,maxv)
        print(filename.split('/')[-1], "min: ",minv," max: ",maxv)

'''
    for pSize1 in range(100,1001,100):
        pSize = pSize1
        print(pSize)
        solver = carp_solver()
        value = solver.solve()
        records.append(value)
        xs.append(pSize)
    l = len(records)

    pt.plot(xs, records, label="cost")
    pt.title("population-cost  dataset:" + carp_solver.file.split('/')[-1])
    pt.xlabel("population")
    pt.ylabel("cost")
    pt.savefig("./report/figures/pop-cost.png")
    pt.close()
    pSize = 500
    print("done")
    records = []
    xs = []
    for rvsProb1 in range(0,11,1):
        solver = carp_solver()
        rvsProb = rvsProb1/10.0
        value = solver.solve()
        records.append(value)
        xs.append(rvsProb)
    l = len(records)

    pt.plot(xs, records, label="cost")
    pt.title("rvsProb-cost  dataset:" + carp_solver.file.split('/')[-1])
    pt.xlabel("rvsProb")
    pt.ylabel("cost")
    pt.savefig("./report/figures/rvsProb-cost.png")
    pt.close()
    rvsProb = 0.9
    print("done")
    xs = []
    records = []
    for sfProb1 in range(0,11,1):
        solver = carp_solver()
        sfProb = sfProb1/10.0
        value = solver.solve()
        records.append(value)
        xs.append(sfProb)
    l = len(records)

    pt.plot(xs, records, label="cost")
    pt.title("sfProb-cost  dataset:" + carp_solver.file.split('/')[-1])
    pt.xlabel("sfProb")
    pt.ylabel("cost")
    pt.savefig("./report/figures/sfProb-cost.png")
    pt.close()
    sfProb = 0.6
    print("done")
    xs = []
    records = []
    for nSF in range(0,11,1):
        solver = carp_solver()
        value = solver.solve()
        records.append(value)
        xs.append(nSF)
    l = len(records)

    pt.plot(xs, records, label="cost")
    pt.title("nSF-cost  dataset:" + carp_solver.file.split('/')[-1])
    pt.xlabel("nSF")
    pt.ylabel("cost")
    pt.savefig("./report/figures/nSF-cost.png")
    pt.close()
    print("done")
    '''