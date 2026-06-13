import sys,os
#添加项目根目录到Python路径
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet

#读入数据
(x_train,t_train),(x_test,t_test)=load_mnist(normalize=True,one_hot_label=True)
network=TwoLayerNet(input_size=784,hidden_size=50,output_size=10)

iters_num=1000
train_size=x_train.shape[0] #784
batch_size=100
learning_rate=0.1

train_loss_list=[]
train_acc_list=[]
test_acc_list=[]

iter_per_epoch=max(train_size/batch_size,1)

for i in range(iters_num):
    batch_mask=np.random.choice(train_size,batch_size) #随机在train_size中抽取batch个编号
    x_batch=x_train[batch_mask]
    t_batch=t_train[batch_mask]

    #梯度
    grad=network.numerical_gradient(x_batch,t_batch)

    #更新
    for key in ('W1','b1','W2','b2'):
        network.params[key]-=learning_rate*grad[key]

    loss=network.loss(x_batch,t_batch) 
    train_loss_list.append(loss)

    if i %iter_per_epoch==0: #表示一个epoch需要多少次mini-bach更新
        train_acc=network.accuracy(x_train,t_train)
        test_acc=network.accuracy(x_test,t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc,test acc |"+str(train_acc)+","+str(test_acc))



