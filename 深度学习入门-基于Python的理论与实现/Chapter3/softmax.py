import numpy as np
import matplotlib.pylab as plt


def softmax(a):
    exp_a=np.exp(a)
    sum_exp_a=np.sum(exp_a)
    y=exp_a/sum_exp_a
    return y
#恒等函数
def identity_function(x):
    return x

X = np.arange(-0.1, 1.0, 0.1)
y1 = softmax(X)
y2=identity_function(X)
plt.plot(X, y1)
plt.plot(X,y2,'k--')
plt.ylim(-0.1, 1.1)
plt.show()
