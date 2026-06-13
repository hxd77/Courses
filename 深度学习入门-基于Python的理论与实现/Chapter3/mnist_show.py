import sys,os
sys.path.append(os.pardir) #把父目录加入到sys.path(Python的搜索模块路径集中)，从而可以导入父目录下的任务目录
import numpy as np
from dataset.mnist import load_mnist
from PIL import Image

def img_show(img):
    pil_img=Image.fromarray(np.uint8(img)) #将Numpy数组数据转换成PIL数据对象
    pil_img.show()

if __name__ == "__main__":
    (x_train,t_train),(x_test,t_test)=load_mnist(flatten=True,normalize=False)
    #flatten=True表示一维展开,normalize=False表示输入图像保持原来的0-255
    #print(x_train.shape) (60000,784)
    #print(t_train) (60000)
    img=x_train[0]
    label=t_train[0]
    print(label) #5

    print(img.shape) #784
    img=img.reshape(28,28) #把图像的形状变为原来的尺寸
    print(img.shape) #(28,28)

    img_show(img)
