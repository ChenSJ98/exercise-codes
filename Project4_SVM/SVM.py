import time
import sys
import numpy as np

def readData(path):
    file=open(path)
    x = []
    y = []
    s = file.readlines()
    for line in s:
        d = []
        l = line.split(' ')

        for i in l[:-1]:
            d.append(float(i))
        d.append(1)

        x.append(d)
        y.append(float(l[-1][:-1]))
    
    return x,y
if __name__ == "__main__":
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    xTrain,yTrain = readData(trainFile)
    xTest,yTest = readData(testFile)
    _lambda = 0.05
    t = 0
    w = []
    for i in range(len(xTrain[0])):
        w.append(0)
    w = np.array(w)
    t = 0
    for i in range(20):
        for j in range(len(xTrain)):
            t += 1.0
            n_t = 1 / (t * _lambda)
            x_j = np.array(xTrain[j])
            if yTrain[j] * (np.dot(w, x_j)) < 1:
                delta = n_t * (_lambda * w - yTrain[j] * x_j)
            else:
                delta = n_t * _lambda * w
            w = w - delta
    correct = 0.0
    for i in range(len(xTest)):
        x_i = np.array(xTest[i])
        predict = np.sign(np.dot(x_i, w))
        print(predict)
        ans = yTest[i]
        if predict == ans:
            correct += 1
    accuracy = round(correct /len(xTest),7)
    print(accuracy)

    

