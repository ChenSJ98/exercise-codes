import math,time
from IMP import readArgs,readData,IMM
import ISE
time0 = time.time()
k = 5
e = 0.1
l = 1
nProcesses = 8
time0 = time.time()

NetworkFile, SeedAmount, DiffusionModel, TimeBudget = readArgs()
toX, fromX, seedSet,size = readData(NetworkFile)

# for i in range (10):
ans = IMM(toX,fromX,size,SeedAmount,e,l,DiffusionModel)
# print("ans:",ans)
print("IMP finish in %fs"%(time.time()-time0))
# for a in ans:
#     print(a)

print(ISE.run_IC_Batch(len(fromX),fromX,ans,2000))
print(ISE.run_LT_Batch(len(fromX),fromX,toX,ans,2000))

