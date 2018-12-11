import numpy,sys,getopt,copy,random,time,math
# import ISE
from multiprocessing import Pool, Process, Queue
def readData(NetworkFile):
    f = open(NetworkFile)
    fromX = []
    toX = []
    seedSet = set()
    size = int(f.readline().split(' ')[0])
    for i in range (size+1):
        fromX.append([])
        toX.append([])
    for r in f.readlines():
        data = r.split(' ')
        fromX[int(data[0])].append([int(data[1]),float(data[2])])
        toX[int(data[1])].append([int(data[0]), float(data[2])])
    
    return toX, fromX,seedSet,size
def readArgs():
    opts, args = getopt.getopt(sys.argv[1:],"i:k:m:t:")
    NetworkFile = ""
    SeedAmount = ""
    DiffusionModel = ""
    TimeBudget = ""
    for op, value in opts:
        if(op == '-i'):
            NetworkFile = value
        if(op == '-k'):
            SeedAmount = value
        if(op == '-m'):
            DiffusionModel = value
        if(op == '-t'):
            TimeBudget = value
    return NetworkFile, int(SeedAmount), DiffusionModel, TimeBudget
def NodeSelection1(R,k,size):
    # print()
    # print("NS")
    # print(len(R))
    time0 = time.time()
    V = set(range(1,size))
    S = set()
    for i in range(k):
        hitnum = [0 for i in range(size+1)]
        for r in R:
            if len(set(r).intersection(S))==0:
                for x in r:
                    hitnum[x]+=1
        maxScore = 0
        pick = 0
        for v in V:
            x = hitnum[v]
            if(x > maxScore):
                maxScore = x
                pick = v
        if pick > 0:
            S.add(pick)
            V.remove(pick)
    # # print("node Selection finish in %f s"%(time.time()-time0))
    # print()
    return S
def NodeSelection(R,k,size):
    # # print()
    # # print("NS")
    # # print(len(R))
    time0 = time.time()
    S = set()
    RRofNode = dict()
    hitnum = [0 for i in range(size+1)]
    for i in range(len(R)):
        RR = R[i]
        if(len(set(RR).intersection(S))==0):
            for x in RR:
                hitnum[x] +=1
                if(x not in RRofNode.keys()):
                    RRofNode[x] = []
                    RRofNode[x].append(i)
                else:
                    RRofNode[x].append(i)

    for i in range(k):
        pick = hitnum.index(max(hitnum))
        if pick > 0:
            S.add(pick)
            # V.remove(pick)
            # hitnum[pick] = 0
            rrList = copy.deepcopy(RRofNode[pick])
            for iRR in rrList:
                for x in R[iRR]:
                    hitnum[x] -= 1
                    RRofNode[x].remove(iRR)
    # print("node Selection finish in %f s"%(time.time()-time0))
    # print()
    return S

def genRR_IC(toX,v):  
    activatedSet = set()
    activatedSet.add(v)
    activity = set()
    activity.add(v)
    while(len(activity)>0):
        newActivity = []
        for seed in activity:
            for neighbor in toX[seed] :
                if (neighbor[0] not in activatedSet):
                    x =random.random()
                    if(x <neighbor[1]):
                        newActivity.append(neighbor[0])
                        activatedSet.add(neighbor[0])
        activity = newActivity
    return activatedSet

def genRR_LT(toX,v):
    # RR = 0
    # # print("call LT")
    activatedSet = set()
    activatedSet.add(v)
    # threshold=[]
    activity = set()
    activity.add(v)
    
    
    while len(activity)>0:
        newActivity = []
        for seed in activity:
            # length = len()
           
            if(len(toX[seed])>0):
                score = 0
                for e in toX[seed]:
                    score += e[1]
                if(random.random()<score):
                    index = random.randint(0,len(toX[seed])-1)
                    # # print(toX[seed])
                    # # print(index)
                    edge = toX[seed][index]
                    if(edge[0] not in activatedSet):
                        activatedSet.add(edge[0])
                        newActivity.append(edge[0])
            else:
                continue
        activity = newActivity
    # # print("LT: ",count)
    return activatedSet
    
def FR(R,S:set):
    time0 = time.time()
    count = 0
    for r in R:
        if len(set(r).intersection(S))>0:
            count += 1
    # # print("FR takes %fs"%(time.time()-time0))
    return count/len(R)
def Sampling(toX,fromX,n,k,e,l,DiffusionModel):
    # # print("start sampling", len(toX))
    R = []
    LB = 1
    e1 = math.sqrt(2)*e
    f=math.factorial
    lambda1 = (2+2/3*e1)*(math.log(f(n)//f(k)//f(n-k))+l*math.log(n)+math.log(math.log2(n)))*n/(e1*e1)


    alpha = math.sqrt(l*math.log(n)+math.log(2))
    beta = math.sqrt((1-1/math.e)*(math.log(f(n)//f(k)//f(n-k)))+l*math.log(n)+math.log(2))
    lambdaS = 2*n*(((1-1/math.e)*alpha+beta)**2)*e**(-2)
    for i in range (1,int(math.log2(n)-1)+1):
        ans = []
        x = n / math.pow(2,i)
        thetaI = lambda1/x
        time1 = time.time()
        # print("start paralell ")
        nProcesses = 8
        pool = Pool(processes=nProcesses)
        # # print(thetaI)
        # while(len(R) <= thetaI):
        for i in range(nProcesses):
            ans.append(pool.apply_async(sample,args=(toX,n,thetaI/nProcesses,DiffusionModel)))
        # R+=(sample(toX,n,int(thetaI/8)))
        pool.close()
        pool.join()
        # print("finish parallel in %fs"%(time.time()-time1))
        for a in ans:
            R+=a.get()
        time1 = time.time()
        Si = NodeSelection(R,k,n)
        # print("finish node selection* in %fs"%(time.time()-time1))
        
        if(n*FR(R,Si)>=(1+e1)*x):
            LB = n*FR(R,Si)/(1+e1)
            # # print("break")
            break
    theta = lambdaS/LB
    time1 = time.time()
    # print("start ending sample")
    while(len(R)<=theta):
        R+=(sample(toX,n,int(theta/8),DiffusionModel))
        # x = random.randint(1,n)
        # RR = genRR_IC(toX,x)
        # R.append(tuple(RR))
    # print("finish ending sample in %fs"%(time.time()-time1))
        
    return R
def sample(toX,n,theta,DiffusionModel):
    # # print("start sample")
    time0 = time.time()
    R = []
    for i in range(int(theta)):
        x = random.randint(1,n)
        if(DiffusionModel == 'IC'):
            RR = genRR_IC(toX,x)
        else:
            RR = genRR_LT(toX,x)
        R.append(tuple(RR))
    # # print("sample takes %fs"%(time.time()-time0))
    return R

def IMM(toX,fromX,n,k,e,l,DiffusionModel):
    time0 = time.time()
    # print("model:",DiffusionModel)
    l = l*(1+math.log(2)/math.log(n))
    R = Sampling(toX,fromX,n,k,e,l,DiffusionModel)
    # print("sampling finished in %fs"%(time.time()-time0))
    AnsSk = NodeSelection(R,k,n)
    # print("Node selection finished in %fs"%(time.time()-time0))
    return AnsSk
DiffusionModel = ''
if __name__ == "__main__":
    time0 = time.time()
    k = 5
    e = 0.05
    l = 1
    nProcesses = 8
    time0 = time.time()
    
    NetworkFile, SeedAmount, DiffusionModel, TimeBudget = readArgs()
    
    toX, fromX, seedSet,size = readData(NetworkFile)
    ans = IMM(toX,fromX,size,SeedAmount,e,l,DiffusionModel)
    for a in ans:
        print(a)
