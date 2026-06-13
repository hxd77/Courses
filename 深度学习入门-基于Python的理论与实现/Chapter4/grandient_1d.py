import numpy as np
import matplotlib.pylab as plt

def numerical_diff(f,x):
    h=1e-4
    return (f(x+h)-f(x-h))/(2*h) #中间差分

def function_1(x):
    return 0.01*x**2+0.1*x

def tangent_line(f,x): #求切线函数，在曲线f的x点处,求出这一点的切线方程,并以函数形式返回
    d=numerical_diff(f,x) #计算差分,切线斜率
    print(d)
    y=f(x)-d*x #计算截距
    print(y)
    return lambda t:d*t+y #输入t返回d*t+y，返回切线方程

x=np.arange(0.0,20.0,0.1)
y=function_1(x)
plt.xlabel("x")
plt.ylabel("f(x)")

tf=tangent_line(function_1,5) #计算在t处的斜率
y2=tf(x)

plt.plot(x,y)
plt.plot(x,y2)
plt.show()