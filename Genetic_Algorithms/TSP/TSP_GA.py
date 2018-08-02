'''
This is a simple implementation of genetic algorithm for solving TSP problems.

Using the Western Sahara's 29 city problem (wi29) dataset with cities indexed from 0 to 28, I get a best solution of [0,1,5,4,3,2,6,8,7,9,10,11,12,13,16,17,14,18,21,22,20,28,27,25,19,15,24,26,23] with optimal value 23727.13694 which is below the reference value of 27603. (weird but plausible result)
'''


import csv
import math
import random

# read cordinate of cities from a file
d = []
with open('TSP/wi29.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        d.append([float(c) for c in row])


#initiate data matrix
D = len(d)
dd = []
for i in range(D):
    temp = []
    for j in range(D):
        t = (math.sqrt(pow((d[i][1]-d[j][1]),2) + pow((d[i][2] - d[j][2]),2)))
        temp.append(t)
    dd.append(temp)

U = 100 # population size (miu)
D = 29 # dimension of an object
L = 10 # number of children (lamda)
NumGen = 10000 # number of generations to be computed

# evaluation of each solution
def funcValue(x):
    D = len(x)
    L = 0
    for i in range(D - 1):
        L += dd[x[i]][x[i+1]]
    return L

# initialization process
def init(u,D):
    #random.seed(23)
    p = []
    for i in range(u):
        x = list(range(D))
        for j in range(D):
            k = random.randint(0,j)
            t = x[j]
            x[j] = x[k]
            x[k] = t
        p.append(x)
    bsf = list(range(D))
    return bsf,p
# crossover function
def OXCrossover(x,y,D):
    x = tuple(x)
    u = list(x)
    c2 = random.randint(1,D-1)
    c1 = random.randint(0,c2-1)
    s = set(x[c1:c2+1])
    px = c2 + 1
    py = c2 + 1

    if px == D:
        px = 0
    if py == D:
        py = 0
    while px != c1:
        if (y[py] not in s):

            u[px] = y[py]
            px += 1
        py += 1
        if px == D:
            px = 0
        if py == D:
            py = 0    
    return u

def mutation(x,D,Pm):
    m2 = random.randint(1,D-1)
    m1 = random.randint(0,m2-1)
    h = int((m2 - m1) /2)
    m1 += 1
    for k in range(h):
        l = x[m1+k]
        x[m1+k] = x[m2 - k]
        x[m2-k] = l
    return x

def evnSelection(p):
    minIndex = 0
    U = len(p)
    min = float('inf') # should be +infinity
    for i in range(U):
       if (funcValue(p[i])<min):
           min = funcValue(p[i])
           minIndex = i
    #print("replace ",p[minIndex])
    return minIndex

def matingSelection(p):
    U = len(p)
    t = random.sample(range(0,U), 4)
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

t = 1
n = 0
Q = []
p.append([16,17,18,14,21,22,20,28,27,25,19,24,26,23,15,13,12,8,6,2,3,7,11,9,10,5,1,0,4])
p.append([0,1,5,4,3,2,6,8,7,9,10,11,12,13,16,17,14,18,21,22,20,28,27,25,19,15,24,26,23])
for x in p:
    print("solution: ", x, "  value:  ", funcValue(x))

while done == False:
    Q = []
    for i in range(L):
        # mating selection
        x,y = matingSelection(p) 
        # variation operator1: Crossover
        u = OXCrossover(p[x],p[y],D)
        # mutation
        u = mutation(u,D,1/D)
        n = n + 1
        Q.append(u)
        # update best-so-far solution
        if funcValue(u) < funcValue(bsf):
            bsf = u
    # environment selection
    R = p
    R += Q
    R.sort(key = funcValue)
    p = R[:int(len(R)/2)]
    t = t + 1
    if t == NumGen:
        done = True

print("the best solution is: ",bsf, " with optimal value:" ,funcValue(bsf))
