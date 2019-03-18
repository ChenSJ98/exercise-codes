from sklearn import svm
import numpy as np
import SVM
import random
import time
def readData(path):
        file=open(path)
        x = []
        y = []
        s = file.readlines()

        for line in s:
                d = []
                l = line.split(',')

                for i in l[:-1]:
                        d.append(float(i))
                x.append(d)
                y.append(float(l[-1][:-1]))
        return x,y

xTrain,yTrain=readData("train_data.txt")
xTest,yTest = readData("train_data.txt")
R = 1
N = len(xTrain)
xTest = xTrain[:int(R*N)]
yTest = yTrain[:int(R*N)]
xTrain = np.array(xTrain)
yTrain = np.array(yTrain)
xTest = np.array(xTest)
yTest = np.array(yTest)
clf = svm.SVC(kernel = 'linear')
time1 = time.time()
clf.fit(xTrain,yTrain)
print(time.time()-time1,'s')
total = 0
N = len(xTest)
for i in range(N):
    xi = xTest[i]
    yi = yTest[i]
    ans = clf.predict(xi.reshape(-1,10))
#     print(i,'  ',yi,'--',ans)
    if (ans == yi):
        total += 1
print("accuracy:",total/len(xTest))

    
    

#clf.fit(x,y)
#print(x)

