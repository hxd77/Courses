import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D

def _numerical_gradient_no_batch(f,x):
    h=1e-4 #0.0001
    grad = np.zeros_like(x)

    for idx in range(x.size):
        tmp_val=x[idx]
        x[idx]=tmp_val+h
        fxh1=f(x) #f(x+h)

        x[idx]=tmp_val-h
        fxh2=f(x) #f(x-h)
        grad[idx]=(fxh1-fxh2)/(2*h)

        x[idx]=tmp_val #还原值
    return grad

def numerical_gradient(f,X):
    if X.ndim==1:
        return _numerical_gradient_no_batch(f,X)
    else:
        grad=np.zeros_like(X)

        for idx,x in enumerate(X):
            grad[idx]=_numerical_gradient_no_batch(f,x)
        return grad
    

def function_2(x):
    if x.ndim==1: #ndim表示数组维度
        return np.sum(x**2)
    else:
        return np.sum(x**2,axis=1) #axis=1表示沿着行方向求和

def tangent_line(f,x):
    d=numerical_gradient(f,x)
    print(d)
    y=f(x)-d*x
    return lambda t:d*t+y

if __name__=='__main__':
    x0=np.arange(-2,2.5,0.25)
    x1=np.arange(-2,2.5,0.25)
    X,Y=np.meshgrid(x0,x1) #numpy里用来生成网格坐标的函数，生成覆盖整个平面的所有(x,y)组合，方便对每个网格点计算函数值
    #生成的X和Y都是两个大小相等的二维数组

    X=X.flatten() #展开成一维数组
    Y=Y.flatten()
    grad=numerical_gradient(function_2,np.array([X,Y]))

    grad_X=grad[0]
    # 创建一个大画布,里面放两个并排的子图
    plt.figure(figsize=(12, 5))

    #专门用来画向量场的函数X,Y是箭头起点的坐标，-grad[0],-grad[1]箭头方向分量,
    #因为梯度 ∇f 指向函数增长最快的方向,而我们想画的是下降最快的方向(指向最小值)。所以要取负梯度 -∇f。
    #这也就是梯度下降法的核心:"沿着负梯度方向走,就能下山。"画出来后你会看到所有箭头都指向原点(因为 f = x₀² + x₁² 的最小值在原点)。
    
    # ===== 左图:二维向量场 =====
    plt.subplot(1, 2, 1)   # 1 行 2 列,当前画第 1 个
    plt.quiver(X, Y, -grad[0], -grad[1], angles="xy", color="#666666")
    plt.xlim([-2, 2])
    plt.ylim([-2, 2])
    plt.xlabel('x0')
    plt.ylabel('x1')
    plt.title('2D gradient field of f(x0,x1)=x0²+x1²')
    plt.grid()

    # ===== 右图:只看 x0 方向 =====
    plt.subplot(1, 2, 2)   # 1 行 2 列,当前画第 2 个
    plt.quiver(X, Y, -grad_X, np.zeros_like(X),
               angles="xy",color="#666666")
    plt.xlim([-2, 2])
    plt.ylim([-1, 1])
    plt.xlabel('x0')
    plt.title('Only ∂f/∂x0 direction')
    plt.grid()

    plt.tight_layout()   # 自动调整子图间距,避免文字重叠
    plt.show()