'''
implementation of u-1 Genetic Algorithm solving the One-Max problem
'''
import random
U = 10 # population size
D = 7 # dimension of an object

# evaluation of each object
def funcValue(x):
    Val = 0
    for value in x:
        Val += value
    return Val

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
            if i == 0:
                xStar.append(1)
        print(x)
        y.append(x)
        bsf.append(0)
        
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
    min = float('inf') # should be +infinity
    for i in range(U):
       if (funcValue(p[i])<min):
           min = funcValue(p[i])
           minIndex = i
    print("replace ",p[minIndex])
    return minIndex

def matingSelection(p):
    U = len(p)
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
#print(p)
t = 1
n = 0
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
    if xStar == bsf:
        done = True
