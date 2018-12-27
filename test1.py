import numpy as np
path = "train_data.txt"
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

w = np.array([-0.41492488, 0.14412138,  0.50754006, -0.10200898, -0.42848712, -0.12348216,0.02234066, -0.368893,    0.61568262,  0.34883719, -0.40404798])
print(w)
correct = 0.0
N = len(data)
for i in range(N):
    # index = random.randint(0, len(data) - 1)
    d = data[i]

    x_i = np.array(d[:-1])
    y_i = d[-1]
    predict = np.sign(np.dot(x_i, w))
    ans = float(dictI2L[y_i])
    # print(predict, "--", ans)
    if predict == ans:
        correct += 1
print("gy accuracy:", correct / N)