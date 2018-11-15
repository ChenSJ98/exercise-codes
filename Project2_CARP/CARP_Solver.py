import numpy as np
import time
from math import inf
from itertools import product
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
    def floyd_warshall(self,n, edge):
        rn = range(n)
        dist = [[inf] * n for i in rn]
        nxt  = [[0]   * n for i in rn]
        for i in rn:
            dist[i][i] = 0
        for u, v, w in edge:
            dist[u-1][v-1] = w
            nxt[u-1][v-1] = v-1
        for k, i, j in product(rn, repeat=3):
            sum_ik_kj = dist[i][k] + dist[k][j]
            if dist[i][j] > sum_ik_kj:
                dist[i][j] = sum_ik_kj
                nxt[i][j]  = nxt[i][k]
        '''
        print("pair     dist    path")
        for i, j in product(rn, repeat=2):
            print(i,j)
            if i != j:
                path = [i]
                while path[-1] != j:
                    path.append(nxt[path[-1]][j])
                print("%d → %d  %4d       %s" 
                    % (i + 1, j + 1, dist[i][j], 
                        ' → '.join(str(p + 1) for p in path))
        '''
        return dist
    def readData(self):
        time1 = time.time()
        f = open("gdb1.dat")
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
        # print(np.zeros(5))
        self.cost = np.zeros((self.V+1,self.V+1),dtype = int)
        # print(self.cost)
        self.demand = np.zeros((self.V+1,self.V+1),dtype = int)
        # print(self.cost)
        while (x != 'END'):
            values = []
            for i in x[:len(x)-1].split(' '):
                if(i != ''):
                    values.append(int(i))
            print(values)
            self.cost[values[0]][values[1]] = values[2]
            self.cost[values[1]][values[0]] = values[2]
            self.demand[values[0]][values[1]] = values[3]
            self.demand[values[1]][values[0]] = values[3]
            self.edges.append([values[0],values[1],values[2]])
            self.edges.append([values[1],values[0],values[2]])
            self.tasks.append([values[0],values[1],values[3]])
            # print(values)
            x = f.readline()
        print(time.time() - time1)
    def solve(self):
        self.readData()
        # print(self.cost)
        # print(self.demand)
        
        print(self.V,' ',self.depot,' ',self.reqE,' ',self.nReqE,' ',self.Capacity)
        print('tasks: ')
        self.printMatrix(self.tasks)
        # print(self.edges)
        print('dist:')
        dist = self.floyd_warshall(self.V,self.edges)
        self.printMatrix(dist)
        # print(self.cost)
    def printMatrix(self,matrix):
        for x in matrix:
            print(x)
if __name__ == "__main__":
    # cost = np.zeros((5,5))
    # x= np.zeros(shape = (3,3))
    # print(x[2][1])
    print("start")
    solver = carp_solver()
    solver.solve()
    # print(cost)
    # print(demand)