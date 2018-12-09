import numpy,sys,getopt,copy,random,time,threading

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
        # fromX[int(data[1])].append([int(data[0]),float(data[2])])
        # toX[int(data[0])].append([int(data[1]), float(data[2])])
    f = open(SeedSetFile)
    for r in f.readlines():
        seedSet.add(int(r))
    return toX, fromX,seedSet
    
def IC(fromX, seedSet):
    activated = []
    for i in range(len(fromX)):
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

if __name__ == "__main__":
    N = 1000
    time0 = time.time()
    NetworkFile, SeedSetFile, DiffusionModel, TimeBudget = readArgs()
    toX, fromX, seedSet = readData()
    ans = 0
    ans1 = 0
    for i in range(N):
        # ans += IC(fromX, seedSet)/N
        ans1 += IC(fromX,seedSet)/N
    print(ans1)
    print(time.time()-time0,'s')
        
            