import numpy as np
import time
class carp_solver:
    V = 0
    depot = 0
    reqE = 0
    nReqE = 0
    Capacity = 0
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
        print(np.zeros(5))
        self.cost = np.zeros((5,5))
        
        self.demand = np.zeros((self.V+1,self.V+1),dtype = int)
        print(self.cost)
        while (x != 'END'):
            values = []
            for i in x[:len(x)-1].split(' '):
                if(i != ''):
                    values.append(int(i))
                self.cost[values[0]][values[1]] = values[2]
                self.demand[values[0]][values[1]] = values[3]
            print(values)
            x = f.readline()
        print(time.time() - time1)
    def solve(self):
        self.readData()
        print(self.V,' ',self.depot,' ',self.reqE,' ',self.nReqE,' ',self.Capacity)
        

        print(self.cost)
    
if __name__ == "__main__":
    solver = carp_solver()
    solver.solve()