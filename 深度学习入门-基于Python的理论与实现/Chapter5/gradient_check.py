import sys,os
# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet

#读入数据
(x_train,t_train),(x_test,t_test)=load_mnist(normalize=True,one_hot_label=True)

network=TwoLayerNet(input_size=784,hidden_size=50,output_size=10)

x_batch=x_train[:3] #3*784
t_batch=t_train[:3] #3*10

grad_numerical=network.numerical_gradient(x_batch,t_batch)
grad_backprop=network.gradient(x_batch,t_batch)

#求各个权重的绝对误差的平均值
for key in grad_numerical.keys():
    diff=np.average(np.abs(grad_backprop[key]-grad_numerical[key]))
    print(key+":"+str(diff))
