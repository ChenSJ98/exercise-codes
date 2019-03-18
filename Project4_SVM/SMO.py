from sklearn import svm
import numpy as np
import SVM
x,y=SVM.readData("train_data.txt")
x = np.array(x)
y = np.array(y)
clf = svm.SVC(gamma='scale')
print(len(x))
print(len(y))
clf.fit(x,y)
total = 0
N = len(x)
for i in range(N):
    xi = x[i]
    yi = y[i]
    ans = clf.predict(xi.reshape(-1,10))
    print(i,'--',ans-yi)
    if (ans == yi):
        total += 1
print("accuracy:",total)

    
    

#clf.fit(x,y)
#print(x)
#print(y)
x = [[0,0],[1,1]]
y = [0,1]
clf.fit(x,y)


print(clf.predict([[2.,2.],[3,3]]))
print(clf.predict([[-2.,-2.]]))
