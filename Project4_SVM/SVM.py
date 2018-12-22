import random

import util
import numpy as np

data, NClass, dictL2I, dictI2L = util.readData("train_data.txt")
# for d in data:
#   print(d)

_lambda = 0.001
t = 0
w = []
for i in range(len(data[0]) - 1):
    w.append(0)
w = np.array(w)
_lambda = 0.0
for x in range(100):
    _lambda += 0.01
    for i in range(20):
        for j in range(len(data)):
            t += 1.0
            n_t = 1 / (t * _lambda)
            x_j = np.array(data[j][:-1])
            y_j = float(dictI2L[data[j][-1]])
            if y_j * (np.dot(w, x_j)) < 1:
                delta = n_t * (_lambda * w - y_j * x_j)
            else:
                delta = n_t * _lambda * w

            w = w - delta

    #print("w:", w)
    N = len(data)

    correct = 0.0
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
    print("  accuracy:", round(correct / N,7), "  l: ", round(_lambda,4), )


# print("hello")
