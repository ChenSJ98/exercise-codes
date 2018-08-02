'''
implementation of u-lamda Genetic Algorithm solving order-3 optimization problem
'''
import random
U = 5 # population size
D = 3 # dimension of an object

# function value for 3-dimension vectors
def funcValue(x):
    s = 0
    j = 1
    while j < len(x):
        t = x[j-1:j+2]
        s = s + order3FuncVal(t)
        j = j + 3
    return s
#evaluation of order3 function value for D-dimension vectors
def order3FuncVal(x):
    s = 0
    if x == [1,1,1]:
        s = 30
    if x in [[1,1,0],[1,0,1],[0,1,1]]:
        s = 0
    if x == [1,0,0]:
        s = 14
    if x == [0,1,0]:
        s = 22
    if x == [0,0,1]:
        s = 26
    if x == [0,0,0]:
        s = 28
    return s
# initialization process
def init(u,D):
    #random.seed(23)
    y = []
    bsf = []
    xStar = []
    for i  in range (u):
        x = []
        for j in range(0,D):
            t = random.random()
            if t > 0.5:
                x.append(1)
            else: 
                x.append(0)
            # initiate bsf and optimal solution
            if i == 0:
                xStar.append(1)
                bsf.append(0)
        print(x)
        y.append(x)
    return xStar,bsf,y

def uniCrossover(x,y,D):
    u = []
    for i in range(0,D):
        t = random.random()
        if(t < 0.5):
            u.append(x[i])
        else:
            u.append(y[i])
    return u

def mutation(x,D,Pm):
    for i in range(0,D):
        t = random.random()
        if(t < Pm):
            if x[i] == 0:
                x[i] = 1
            else:
                x[i] = 0
    return x

def evnSelection(p):
    minIndex = 0
    U = len(p)
    min = float('inf') 
    for i in range(U):
       if (funcValue(p[i])<min):
           min = funcValue(p[i])
           minIndex = i
    print("replace ",p[minIndex])
    return minIndex

def matingSelection(p):
    U = len(p)
    # randomly get 4 different indexes of vectors
    t = random.sample(range(0,U), 4)
    d = int(t[0])
    e = int(t[1])
    f = int(t[2])
    g = int(t[3])
    if funcValue(p[d]) > funcValue(p[e]):
        a = d
    else:
        a = e
    if funcValue(p[f]) > funcValue(p[g]):
        b = f
    else:
        b = g
    return a,b
done = False
xStar,bsf,p = init(U,D)
t = 1
n = 0
print(p[0][0:3])
while done == False:
    # mating selection
    x,y = matingSelection(p) 
    # variation operator1: Crossover
    u = uniCrossover(p[x],p[y],D)
    # mutation
    u = mutation(u,D,1/D)

    n = n + 1
    # update best-so-far solution
    if funcValue(u) > funcValue(bsf):
        bsf = u
    # environment selection
    t = evnSelection(p)
    p[t] = u
    
    t = t + 1
    print(n,"  bsf: ",bsf)
    if (xStar == bsf):
        done = True
