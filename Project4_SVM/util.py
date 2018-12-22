import math
import copy
def normalize(data):
    pass
def readData(path):
    dictL2I = {}
    dictI2L = {}
    NClass = 0
    file=open(path)
    data = []
    for x in file.readlines():
        d = []
        l = x.split(' ')

        for i in l[:-1]:
            d.append(float(i))
        str = l[len(l)-1][:-1]


        if (str not in dictL2I.keys() and str != ''):
            NClass += 1
            dictL2I[str] = NClass
            dictI2L[NClass] = str
        if(str != ''):
            d.append(1)
            d.append(dictL2I[str])
            data.append(d)


    '''
    data = data[:-1]
    
    maxVal = copy.deepcopy(data[0][:-1])
    minVal = copy.deepcopy(data[0][:-1])
    for d in data:
        for i in range(len(maxVal)):
            if(maxVal[i]<d[i]):
                maxVal[i] = d[i]
            if(minVal[i]>d[i]):
                minVal[i] = d[i]
    dRange = []
    
    for i in range(len(maxVal)):
        dRange.append(maxVal[i]-minVal[i])

    for d in data:
        for i in range(len(d)-1):
            d[i] = (d[i]-minVal[i])/dRange[i]


    '''


    return data,NClass,dictL2I,dictI2L

