import sys, getopt
import numpy as np


def read_file(file_path, is_test_data):
    datalines = open(train_data, 'r').readlines()
    global x, y, row, col
    row = len(datalines)
    col = 10
    x = np.zeros((row, col))
    y = np.zeros(row)
    for i in range(row):
        data_line = datalines[i]
        vector = data_line.split()
        for j in range(col):
            x[i][j] = vector[j]
        # if not is_test_data:
        y[i] = vector[col]
    x = np.c_[x, np.ones(row)]

def pegasos(l = 1):
    print(l)
    global x, y, row, col
    w = np.zeros((col + 1))
    t = 0
    for it in range(20):
        for j in range(row):
            t = t + 1
            n = 1 / (t * l)
            if y[j] * np.dot(x[j], w) < 1:
                w = w - n * (l * w - y[j] * x[j].T)
            else:
                w = w - n * l * w
    return w


def predict(w):
    global test_data
    read_file(test_data, True)
    res = np.sign(np.dot(x, w))
    diff = res - y
    ratio = sum(diff == 0) / row
    print(res)
    print(ratio)


if __name__ == "__main__":
    x = None
    y = None
    row = 0
    col = 0
    l = 0.05
    test_data = sys.argv[1]
    train_data = "train_data.txt"
    '''
    try:
        opts, args = getopt.getopt(sys.argv[2:], "t:", [])
    except getopt.GetoptError:
        print("usage: python3 SVM.py <test_data> -t <time budget>")
    for opt, arg in opts:
        if opt == '-t':
            termination = arg
    '''
    read_file(train_data, False)
    w = pegasos(l)
    #predict(w)
    # print(x)
    # print(y)
    print(w)