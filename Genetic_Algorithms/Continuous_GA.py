'''
Implementation of u-lamda Genetic Algorithm for continuous optimization  problems.

There's no mutation of child in this algorithm. The program may fail to approach global optimal solution.
'''
import numpy as np
import matplotlib.pyplot as pt
import random
import math

U = 5000 # population size (miu)
D = 3 # dimension of an object
L = 100 # number of children (lamda)
NumGen = 100
accuracy = 0.01

minVal = -30
maxVal = 30
objFunc = 2 # choose object function

# object function Sphere
def sphere(x):
    Val = 0
    for value in x:
        Val += math.pow(value,2)
    return Val
# object function Rosenbrock
def Rosenbrock(x):
    Val = 0
    for i in range(len(x) - 1):
        Val += 100*(math.pow(x[i+1]-x[i],2)+math.pow(x[i]-1,2))
    return Val

def funcValue(x):
    if objFunc == 1:
        return sphere(x)
    if objFunc == 2:
        return Rosenbrock(x)

# initialization process
def init(U,D):
    y = []
    bsf = []
    for i  in range (U):
        x = []
        for j in range(D):
            x.append(random.random()*(maxVal - minVal) + minVal)
        y.append(x)
        bsf.append(minVal)
    return bsf,y

def BLX_alpha(x,y,a):
    u = []
    for i in range(0,D):
        A = min(x[i],y[i]) - a*(abs(x[i]-y[i]))
        B = max(x[i],y[i]) + a*(abs(x[i]-y[i]))
        t = random.random()*(B - A) + A
        if t < minVal:
            t = minVal
        if t > maxVal:
            t = maxVal
        u.append(t) 
    return u

def evnSelection(p):
    minIndex = 0
    U = len(p)
    min = float('inf') # should be +infinity
    for i in range(U):
       if (funcValue(p[i])<min):
           min = funcValue(p[i])
           minIndex = i
    print("replace ",p[minIndex])
    return minIndex

def matingSelection(p):
    t = random.sample(range(0,len(p)), 4)
    d = int(t[0])
    e = int(t[1])
    f = int(t[2])
    g = int(t[3])
    if funcValue(p[d]) < funcValue(p[e]):
        a = d
    else:
        a = e
    if funcValue(p[f]) < funcValue(p[g]):
        b = f
    else:
        b = g
    return a,b
done = False
bsf,p = init(U,D)
#print(p)
t = 0
n = 0
Q = []
bsfs = []
while done == False:
    Q = []
    for i in range(L):
        # mating selection
        x,y = matingSelection(p) 
        # variation operator1: Crossover
        u = BLX_alpha(p[x],p[y],0.5)
        n = n + 1
        Q.append(u)
        # update best-so-far solution
        if funcValue(u) < funcValue(bsf):
            bsf = u
            
        
    # environment selection, keep the best half solutions from P|Q
    R = p
    R += Q
    R.sort(key = funcValue)
    p = R[:int(len(R)/2)]
    t = t + 1
    bsfs.append(funcValue(bsf))  
    if funcValue(bsf) < accuracy:
        done = True
    
print(t," generations, bsf: ",bsf,"  with optimal value: ", funcValue(bsf))

x = np.arange(1 , t + 1,1)
y = bsfs
pt.plot(x,y)

pt.title("function val")
pt.show()
