import numpy as np
import time
from math import inf
from itertools import product
import random
import sys
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
    file = file7
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
        '''
        #print("pair     dist    path")
        for i, j in product(rn, repeat=2):
            #print(i,j)
            if i != j:
                path = [i]
                while path[-1] != j:
                    path.append(nxt[path[-1]][j])
                #print("%d â†’ %d  %4d       %s" 
                    % (i + 1, j + 1, dist[i][j], 
                        ' â†’ '.join(str(p + 1) for p in path))
        '''
        return dist
    def readData(self):
        time1 = time.time()
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
        # #print(np.zeros(5))
        self.cost = np.zeros((self.V+1,self.V+1),dtype = int)
        # #print(self.cost)
        self.demand = np.zeros((self.V+1,self.V+1),dtype = int)
        # #print(self.cost)
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
                self.tasks.append([values[0],values[1],values[3]])
            # #print(values)
            x = f.readline()
        # #print(time.time() - time1)
    def toDirectedGraph(self, taskList, depot,dist):
        # print("to directed graph")
        #print(taskList)
        length = len(taskList)
        DG = np.full((2*length+1,2*length+1),inf)
        incoming = []
        outgoing = []
        for i in range (2*length+1):
            incoming.append([])
            outgoing.append([])
        # #print(taskList)
        # #print(outgoing)
        # #print(incoming)
        # print(dist)
        for i in range(length):
            load = 0
            # #print('i:',i)
            # #print(taskList[i],': ')
            x = 2*i+1
            # print("computing edge:", x,' -> ',x+1)
            task = taskList[i]
            cost = dist[self.depot][task[0]] + dist[task[0]][task[1]] + dist[task[1]][self.depot]
            DG[x][x+1] = cost
            incoming[x+1].append([x,x+1,cost])
            outgoing[x].append([x,x+1,cost])
            if(x > 1):
                incoming[x].append([x-1,x,0])
                outgoing[x-1].append([x-1,x,0])
            # print(DG[x][x+1])
            # prepare to merge routes
            load = task[2]
            cost = dist[self.depot][task[0]] + dist[task[0]][task[1]]
            j = i + 1
            while(True):
                if(j == length):
                    j -= 1
                    break
                # #print('j: ',j)
                if(load + taskList[j][2] <= self.Capacity):
                    # #print(taskList[j])
                    load += taskList[j][2]
                    cost += dist[taskList[j-1][1]][taskList[j][0]] + dist[taskList[j][0]][taskList[j][1]]
                    DG[x][2*j+2] = cost+dist[taskList[j][1]][self.depot]
                    # print("add edge: ",x," -> ",2*j+2,"  ", DG[x][2*j+2])
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
        # self.printMatrix(DG)
        # self.printMatrix(outgoing)
        # self.printMatrix(incoming)
        return DG, incoming, outgoing
    def getPath(self, DG, incoming, outgoing):
        path = 0
        nodeCost=[0]*(len(DG)+1)
        bestPath = [[]]*(len(DG)+1)
        bestPath[1] = []
        for i in range(1,len(DG)):
            # print("loop on ", i, " incoming: ",incoming[i])
            minCost = inf
            bestEdge =[]
            # find incoming edge with min cost
            if(i > 1):
                for edge in incoming[i]:
                    # edgeCost = self.dist[edge[0]][edge[1]]
                    if(edge[2] < minCost):
                        minCost = edge[2]
                        bestEdge = edge
                # print(i)
                
                if(i%2 == 0):
                    preBestPath = list(bestPath[bestEdge[0]])
                    print("best edge:", bestEdge)
                    preBestPath.append([bestEdge[0],bestEdge[1]])
                    print("bestPath @", i, "  ", preBestPath)
                    bestPath[i] = preBestPath
                    print()
                else:
                    bestPath[i] = bestPath[i-1]
            else:
                minCost = 0
            # print("best edge: ",bestEdge, "min: ",minCost)
            nodeCost[i] += minCost
            # release node, update outgoing edge
            for edge in outgoing[i]:
                # print("updating edge: ",edge)
                index = incoming[edge[1]].index(edge)
                # print("found, @", index)
                edge[2] += nodeCost[i]
                incoming[edge[1]][index] = edge
            # print("update complete")
            # self.printMatrix(incoming)
        # print('min cost: ',nodeCost[len(DG)-1])
        return bestPath[len(DG)-1], nodeCost[len(DG)-1]
    def solve(self):
        self.readData()
        # #print(self.cost)
        # #print(self.demand)
        print('V:',self.V,' depot: ',self.depot,' tasks: ',self.reqE,' non-task edges: ',self.nReqE,' capacity ',self.Capacity)
        # print('tasks: ')
        # self.printMatrix(self.tasks)
        # #print(self.edges)
        # #print('dist:')
        dist = self.floyd_warshall(self.V,self.edges)
        # self.printMatrix(dist)
        DG, incoming, outgoing = self.toDirectedGraph(self.tasks,self.depot,dist)
        path, score = self.getPath(DG,incoming, outgoing)# #print(self.cost)
        print("original order: ", score)
        print(self.genSolution(path, self.tasks))
        print(path)
    def genSolution(self,path, taskList):
        solution = 's '
        for x in path:
            print(x)
            # print(0)
            solution += '0,'
            for i in range(int((x[0]+1)/2),int(x[1]/2)+1):
                # print(taskList[i - 1])
                solution = solution + '(' + str(taskList[i-1][0]) + ','+str(taskList[i-1][1])+'),'
            # print(0)
            solution += '0,'
        return solution[:len(solution)-1]
    def printPath(self,path, taskList):
        for i in range(len(path)):
            if (i % 2 == 0):
                path[i] = taskList[int(path[i]/2)-1][1]
            else:
                path[i] = taskList[int((path[i]+1)/2)-1][0]
        #print(path)
    def printMatrix(self,matrix):
        i = 0
        for x in matrix:
            print()
            print(i,x)
            i += 1
if __name__ == "__main__":
    solver = carp_solver()
    if len(sys.argv) == 6:
        # print("?????????")
        # print(sys.argv)
        file_name = sys.argv[1]
        solver.file = file_name
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])
    # cost = np.zeros((5,5))
    # x= np.zeros(shape = (3,3))
    # #print(x[2][1])
    time0 = time.time()
    #print("start")
    solver.solve()
    # #print(cost)
    # #print(demand)
    #print("time spent: ", time.time()-time0)