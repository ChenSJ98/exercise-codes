import random
import numpy as np
import matplotlib.pyplot as plt
def readData(path):
    file=open(path)
    x = []
    y = []
    s = file.readlines()
    random.shuffle(s)
    for line in s:
        d = []
        l = line.split(',')

        for i in l[:-1]:
            d.append(float(i))
        # add constant normalization to eliminate b
        #d.append(1)

        x.append(d)
        y.append(float(l[-1][:-1]))
    
    return x,y
if __name__ == "__main__":
        
    x,y = readData("train_data.txt")

    _lambda = 0.001
    t = 0
    w = []
    for i in range(len(x[0])):
        w.append(0)
    w = np.array(w)
    _lambda = 0.05
    R = 0.5
    rs = []
    ys = []
    ls = []
    N = len(x)
    for i in range (1,1000):
        _lambda = i/400
        # R = i/400
        t = 0
        # for x in range(100):
            # _lambda += 0.01
        num = int(R*N)
        for i in range(20):
            for j in range(num):
                t += 1.0
                n_t = 1 / (t * _lambda)
                x_j = np.array(x[j])
                if y[j] * (np.dot(w, x_j)) < 1:
                    delta = n_t * (_lambda * w - y[j] * x_j)
                else:
                    delta = n_t * _lambda * w

                w = w - delta

        correct = 0.0
        for i in range(num,N):
            x_i = np.array(x[i])
            predict = np.sign(np.dot(x_i, w))
            ans = y[i]
            if predict == ans:
                correct += 1
        accuracy = round(correct /(N-num),7)
        ls.append(_lambda)
        ys.append(accuracy)
        rs.append(R)
        print(R,"  accuracy:", accuracy, "  l: ", round(_lambda,4), )
    
    
    plt.xlabel("lambda")
    plt.ylabel("accuracy")
    plt.plot(ls,ys)
    plt.show()
    plt.savefig("lambda-a.png")
    plt.clf()
    plt.xlabel("training data ratio")
    plt.ylabel("accuracy")
    # plt.plot(rs,ys)
    plt.show()
    plt.savefig("ratio-a.png")
    

