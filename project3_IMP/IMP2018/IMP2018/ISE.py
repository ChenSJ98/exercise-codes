import numpy,sys,getopt,copy,random,time
from multiprocessing import Pool, Process, Queue

def readData():
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
    f = open(SeedSetFile)
    for r in f.readlines():
        seedSet.add(int(r))
    return toX, fromX,seedSet,size
    
def IC(size,fromX, seedSet):
    activated = []
    for i in range(size):
        activated.append(0)
    for s in seedSet:
        activated[s] = 1
    activity = set(copy.deepcopy(seedSet))
    count = len(seedSet)
    # activated = set(copy.deepcopy(seedSet))
    while(len(activity)>0):
        newActivity = []
        for seed in activity:
            for neighbor in fromX[seed] :
                # print(neighbor)
                if (activated[neighbor[0]] == 0):
                    x =random.random()
                    # print("rand:",x)
                    if(x <neighbor[1]):
                        newActivity.append(neighbor[0])
                        activated[neighbor[0]] = 1
                        count += 1
        activity = newActivity
    # print("---------------------",count)
    return count
def LT(size,fromX,toX,seedSet):
    # print("call LT")
    activated=[]
    threshold=[]
    activity = copy.deepcopy(seedSet)
    for i in range(size):
        # activated.append(0)
        threshold.append(random.random())
        if(threshold[-1] == 0.0):
            activated.append(1)
            activity.add(i)
        else:
            activated.append(0)
    for i in seedSet:
        activated[i] = 1
    count = len(activity)
    
    while len(activity)>0:
        newActivity = []
        for seed in activity:
            for neighbor in fromX[seed]:
                if(activated[neighbor[0]] == 0):
                    value = 0
                    for nbr in toX[neighbor[0]]:
                        if(activated[nbr[0]] == 1):
                            value += nbr[1]
                    if(value > threshold[neighbor[0]]):
                        activated[neighbor[0]] = 1
                        newActivity.append(neighbor[0])
                        count += 1
        activity = newActivity
    # print("LT: ",count)
    return count
def readArgs():
    opts, args = getopt.getopt(sys.argv[1:],"i:s:m:t:")
    NetworkFile = ""
    SeedSetFile = ""
    DiffusionModel = ""
    TimeBudget = ""
    for op, value in opts:
        if(op == '-i'):
            NetworkFile = value
        if(op == '-s'):
            SeedSetFile = value
        if(op == '-m'):
            DiffusionModel = value
        if(op == '-t'):
            TimeBudget = value
    return NetworkFile, SeedSetFile, DiffusionModel, TimeBudget
def run_IC_Batch(size,fromX,seedSet,Num):
    ans = 0
    for i in range (Num):
        ans += IC(size,fromX,seedSet)/Num
    return ans
def run_LT_Batch(size,fromX,toX,seedSet,Num):
    ans = 0
    for i in range(Num):
        ans += LT(size,fromX,toX,seedSet)/Num
    return ans
if __name__ == "__main__":
    N = 1000
    nProcesses = 8
    time0 = time.time()

    NetworkFile, SeedSetFile, DiffusionModel, TimeBudget = readArgs()
    toX, fromX, seedSet,size = readData()
    # ans = LT(size,fromX,toX,seedSet)
    # print(ans)
    # '''
    time2 = time.time()
    ans = []
    ans1 = []
    pool = Pool(processes = nProcesses)
    if(DiffusionModel == 'IC'):
        for i in range(nProcesses):
            ans.append(pool.apply_async(run_IC_Batch,args=(size,fromX,seedSet,int(N/nProcesses)+1)))
    else:
        for i in range(nProcesses):
            ans.append(pool.apply_async(run_LT_Batch,args=(size,fromX,toX,seedSet,int(N/nProcesses)+1)))
    pool.close()
    pool.join()

    answer = 0
    for v in ans:
        answer += v.get()/nProcesses
    print(answer)
    # '''
            