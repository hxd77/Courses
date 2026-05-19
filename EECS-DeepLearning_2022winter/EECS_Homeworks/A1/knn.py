"""
Implements a K-Nearest Neighbor classifier in PyTorch.
"""
import torch
from typing import Dict, List


def hello():
    """
    This is a sample function that we will try to import and run to ensure that
    our environment is correctly set up on Google Colab.
    """
    print("Hello from knn.py!")


def compute_distances_two_loops(x_train: torch.Tensor, x_test: torch.Tensor):
    """
    计算训练集中每个元素与测试集中每个元素之间的欧氏距离平方。图像应展平并当作向量处理。

    该实现采用朴素的嵌套循环方式遍历训练数据与测试数据。

    输入数据可以具有任意维度——例如，本函数应能计算向量间的最近邻，
    此时输入形状为 (训练样本数, 测试样本数, D)；也应能计算图像间的最近邻，
    此时输入形状为 (训练样本数, 测试样本数, C, H, W)。
    更一般地，输入形状为 (训练样本数, 测试样本数, D1, D2, …, Dn)；
    在计算距离前，你需要将每个形状为 (D1, D2, …, Dn) 的元素展平为形状为 (D1 × D2 × … × Dn) 的向量。

    输入张量不应被修改。

    注意：你的实现不得使用`torch.norm`、`torch.dist`、`torch.cdist`，或它们的实例方法变体（`x.norm`、`x.dist`、`x.cdist`等）。
    不得使用`torch.nn`或`torch.nn.functional`模块中的任何函数。

    参数：
        x_train：形状为(num_train, D1, D2, ...)的张量
        x_test：形状为(num_test, D1, D2, ...)的张量

    返回值：
        dists：形状为(num_train, num_test)的张量，其中dists[i, j]为第i个训练样本与第j个测试样本之间的欧氏距离平方。其数据类型应与x_train一致。
    """
    # 将dists初始化为形状为(num_train, num_test)的张量，
    # 其数据类型和设备与x_train保持一致
    num_train = x_train.shape[0]
    num_test = x_test.shape[0]
    dists = x_train.new_zeros(num_train, num_test)
    ##########################################################################
    # TODO: Implement this function using a pair of nested loops over the    #
    # 训练数据与测试数据。
    # 你不得使用torch.norm（或其实例方法变体），
    # 也不得使用torch.nn或torch.nn.functional中的任何函数。                                                                           
    ##########################################################################
    # Replace "pass" statement with your code
    for i in range(num_train):
        for j in range(num_test): 
            dists[i,j]=((x_train[i]-x_test[j])**2).sum()**(1/2)
    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################
    return dists


def compute_distances_one_loop(x_train: torch.Tensor, x_test: torch.Tensor):
    """
    计算训练集中每个元素与测试集中每个元素之间的欧氏距离平方。图像应展平并当作向量处理。

    该实现仅对训练数据使用单层循环。

    与`compute_distances_two_loops`类似，该函数应能处理任意维度的输入。输入不应被修改。

    注意：你的实现不得使用`torch.norm`、`torch.dist`、`torch.cdist`，或它们的实例方法变体（`x.norm`、`x.dist`、`x.cdist`等）。不得使用`torch.nn`或`torch.nn.functional`模块中的任何函数。

    参数：
        x_train：形状为(num_train, D1, D2, ...)的张量
        x_test：形状为(num_test, D1, D2, ...)的张量

    返回值：
        dists：形状为(num_train, num_test)的张量，其中dists[i, j]为第i个训练样本与第j个测试样本之间的欧氏距离平方。其数据类型应与x_train一致。
    """
    # Initialize dists to be a tensor of shape (num_train, num_test) with the
    # same datatype and device as x_train
    num_train = x_train.shape[0]
    num_test = x_test.shape[0]
    dists = x_train.new_zeros(num_train, num_test)
    ##########################################################################
    # TODO: Implement this function using only a single loop over x_train.   #
    #                                                                        #
    # You may not use torch.norm (or its instance method variant), nor any   #
    # functions from torch.nn or torch.nn.functional.                        #
    ##########################################################################
    # Replace "pass" statement with your code
    # 为了处理任意维度的输入，我们首先将图像展平为向量。
    x_train_flat = x_train.view(num_train, -1) #将训练集展平为[num_train,D]
    x_test_flat = x_test.view(num_test, -1) #将测试集展平为[num_test,D]
    for i in range(num_train):
        # 利用广播机制计算第 i 个训练样本与所有测试样本的差值，然后平方。
        # 最后沿特征维度求和，得到欧氏距离的平方。
        dists[i] = torch.sum((x_train_flat[i] - x_test_flat)**2, dim=1)
        #x_train_flat[i]形状是[D],x_test_flat形状是[num_test,D]
        #相减时利用广播机制,[D]自动拓展为[num_test,D] dim=1表示沿维度1求和
        #dists[i][j] 就是训练样本 i 与测试样本 j 的 L2 距离平方。KNN 接下来会对每列找最小的 K 个值，用对应训练样本的标签来预测测试样本的类别。
    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################
    return dists


def compute_distances_no_loops(x_train: torch.Tensor, x_test: torch.Tensor):
    """
    计算训练集中每个元素与测试集中每个元素之间的欧氏距离平方。图像应展平并视为向量处理。

    该实现不得使用任何Python循环。为保证内存效率，同样不应创建任何大型中间张量；尤其不得创建元素数量为O(训练样本数×测试样本数)的中间张量。

    与`compute_distances_two_loops`类似，该方法应能处理任意维度的输入，且不得修改输入数据。

    注意：实现中不得使用`torch.norm`、`torch.dist`、`torch.cdist`及其实例方法变体（`x.norm`、`x.dist`、`x.cdist`等）。不得使用`torch.nn`或`torch.nn.functional`模块中的任何函数。

    参数：
        x_train：形状为(训练样本数, 通道数, 高度, 宽度)的张量
        x_test：形状为(测试样本数, 通道数, 高度, 宽度)的张量

    返回值：
        dists：形状为(训练样本数, 测试样本数)的张量，其中dists[i, j]表示第i个训练样本与第j个测试样本之间的欧氏距离平方。
    """
    # 将dists初始化为形状为(num_train, num_test)的张量，
    # 其数据类型和设备与x_train保持一致
    #x_train.shape=[50000,3,32,32]
    num_train = x_train.shape[0]
    num_test = x_test.shape[0]
    dists = x_train.new_zeros(num_train, num_test) #等价于torch.zeros(num_train,num_test,dtype=x_train_dtype,device=x_train.device)
    ##########################################################################
    # TODO: Implement this function without using any explicit loops and     #
    # without creating any intermediate tensors with O(num_train * num_test) #
    # elements.                                                              #
    #                                                                        #
    # You may not use torch.norm (or its instance method variant), nor any   #
    # functions from torch.nn or torch.nn.functional.                        #
    #                                                                        #
    # 提示：尝试通过两次广播求和与一次矩阵乘法来构建欧几里得距离                       #
    ##########################################################################
    # Replace "pass" statement with your code
    x_train_flat = x_train.view(num_train, -1)  # [num_train, 3*32*32]
    x_test_flat = x_test.view(num_test, -1)     # [num_test, 3*32*32]

    #AB2.shape=[num_train,num_test]
    AB2 = x_train_flat.mm(x_test_flat.T)*2 #A.mm(B.T)是矩阵乘法,[num_train,num_test] 第[i,j]位置是训练样本i和测试样本j的内积
    dists = ((x_train_flat**2).sum(dim = 1).reshape(-1,1) - AB2 + (x_test_flat**2).sum(dim = 1).reshape(1,-1))**(1/2)
    #因为x_train_flat**2.sum(dim=1)(shape=num_train,) reshape后shape=(num_train,1) (x_test_flat**2).sum(dim = 1).reshape(1,-1))**(1/2)(shape=num_test,),reshape后shape=(1,num_test)
    #(A**2).sum(dim=1).reshape(-1, 1)   # [num_train, 1]，每个训练样本的 ||a||²
    #(B**2).sum(dim=1).reshape(1, -1)   # [1, num_test]， 每个测试样本的 ||b||²
    #因为x_train_flat**2.sum(dim=1)的维度是(num_train,),reshape(-1,1)后shape=(num_train,1),
    #AB2.shape=(num_train,num_test)
    #x_test_flat**2.sum(dim=1)的维度是(num_test,),reshape(1,-1)后shape=(1,num_test)
    #理解: https://stackoverflow.com/questions/27948363/numpy-broadcast-to-perform-euclidean-distance-vectorized
 
    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################
    return dists #dists.shape=(num_train,num_test)


def predict_labels(dists: torch.Tensor, y_train: torch.Tensor, k: int = 1):
    """
<<<<<<< HEAD
    在已知所有训练样本与测试样本两两之间距离的前提下，通过对测试集来检查训练集中每个测试样本的`k`个最近邻进行**多数投票**，为每个测试样本预测标签。

    若出现票数相同的情况，该函数**应返回编号最小的标签**。例如，当`k=5`时，若某一测试样本的5个最近邻标签为`[1, 2, 1, 2, 3]`，则标签1和2各获得2票，出现平票，此时应返回更小的标签1。

    该函数不应修改任何输入数据。

    参数：
        - dists：形状为`(num_train, num_test)`的张量，其中`dists[i, j]`表示第`i`个训练样本与第`j`个测试样本之间的欧式距离平方。
        - y_train：形状为`(num_train,)`的张量，存储所有训练样本的标签。每个标签均为`[0, num_classes - 1]`范围内的整数。
        - k：用于分类的最近邻数量。

    返回值：
        - y_pred：形状为`(num_test,)`的int64类型张量，存储测试数据的预测标签，其中`y_pred[j]`为第`j`个测试样本的预测标签。每个标签均为`[0, num_classes - 1]`范围内的整数。
=======
    已知所有训练样本与测试样本两两之间的距离，通过在训练集中选取对测试样本来说的`k`个最近邻并进行**多数投票**，为每个测试样本预测标签。

    若出现票数相同的情况，该函数应返回**编号最小**的标签。例如，当`k=5`时，某一测试样本的5个最近邻标签为`[1, 2, 1, 2, 3]`，此时标签1和2各获得2票，出现平局，则应返回更小的标签1。

    该函数不应修改任何输入参数。

    参数：
        dists：形状为(num_train, num_test)的张量，其中dists[i, j]表示第i个训练点与第j个测试点之间的欧式距离平方。
        y_train：形状为(num_train,)的张量，给出所有训练样本的标签。每个标签均为范围在[0, num_classes - 1]内的整数。
        k：用于分类的最近邻数量。

    返回值：
        y_pred：形状为(num_test,)的int64类型张量，给出测试数据的预测标签，其中y_pred[j]为第j个测试样本的预测标签。每个标签均为范围在[0, num_classes - 1]内的整数。
>>>>>>> c7e7149e53b09b99151424fa9abab3788169dfc6
    """
    num_train, num_test = dists.shape
    y_pred = torch.zeros(num_test, dtype=torch.int64)
    ##########################################################################
    # TODO: Implement this function. You may use an explicit loop over the   #
    # test samples.                                                          #
    #                                                                        #
    # HINT: Look up the function torch.topk                                  #
    ##########################################################################
    # Replace "pass" statement with your code
<<<<<<< HEAD
    _,indices=torch.topk(dists,k,dim=0,largest=False) #input=dists,k表示取多少个,dim=0表示对维度0,largest=False表示取最小值
    #indices.shape=(k,num_test)
    for i in range(indices.shape[1]): #遍历每一个测试样本
        knn_label=y_train[indices[:,i]]
        votes=knn_label.bincount() #返回数组,按从小到大的数量排序，同时对应下标 
        y_pred[i]=torch.argmax(votes)
=======
    _,top_indices=torch.topk(dists,k,dim=0,largest=False) #dists是输入张量, k是要取的元素数量,Largest=False表示取最小的
    #top_indices.shape=(k,num_test)因为dim=0
    for i in range(top_indices.shape[1]): #遍历每一个num_test测试样本
        knn_label=y_train[top_indices[:,i]] #得到每一个num_test[i]对应的标签
        #top_indices[:,i]表示取第 i 列就得到第 i 个测试样本的 k 个最近邻在训练集中的下标，形状 (k,)。
        #torch.bincount(knn_labels) 输出一个数组，下标就是标签值，值是对应票数。例如标签为 [1,2,1,2,3] 时，结果是 [0, 2, 2, 1]。
        votes=torch.bincount(knn_label) #统计每个标签出现的次数，返回一个下标即为标签值的计数数组
        y_pred[i]=torch.argmax(votes) #argmax返回最大的下标值

    print(y_pred)
>>>>>>> c7e7149e53b09b99151424fa9abab3788169dfc6
    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################
    return y_pred


class KnnClassifier:

    def __init__(self, x_train: torch.Tensor, y_train: torch.Tensor):
        """
        使用指定的训练数据创建一个新的K近邻分类器。
        在初始化方法中，我们仅需存储传入的训练数据即可。

        参数：
            x_train：形状为(num_train, C, H, W)的张量，用于表示训练数据
            y_train：形状为(num_train, )的int64类型张量，用于表示训练标签
        """
        ######################################################################
        # TODO: Implement the initializer for this class. It should perform  #
        # no computation and simply memorize the training data in            #
        # `self.x_train` and `self.y_train`, accordingly.                    #
        ######################################################################
        # Replace "pass" statement with your code
        self.x_train=x_train
        self.y_train=y_train
        ######################################################################
        #                         END OF YOUR CODE                           #
        ######################################################################

    def predict(self, x_test: torch.Tensor, k: int = 1):
        """
        使用分类器进行预测。

        参数：
            x_test：形状为(num_test, C, H, W)的张量，用于提供测试样本。
            k：用于预测的近邻数量。

        返回值：
            y_test_pred：形状为(num_test,)的张量，用于给出测试样本的预测标签。
        """
        y_test_pred = None
        ######################################################################
        # TODO: Implement this method. You should use the functions you      #
        # wrote above for computing distances (use the no-loop variant) and  #
        # to predict output labels.                                          #
        ######################################################################
        # Replace "pass" statement with your code
        dists=compute_distances_no_loops(self.x_train,x_test)
        y_test_pred=predict_labels(dists,self.y_train,k)
        ######################################################################
        #                         END OF YOUR CODE                           #
        ######################################################################
        return y_test_pred

    def check_accuracy(
        self,
        x_test: torch.Tensor,
        y_test: torch.Tensor,
        k: int = 1,
        quiet: bool = False
    ):
        """
        用于在测试数据上检验该分类器准确率的实用方法。返回分类器在测试数据上的准确率，同时打印一条包含该准确率的提示信息。

        参数：
            x_test：形状为 (num_test,C,H,W) 的张量，代表测试样本。
            y_test：形状为 (num_test,) 的 int64 类型张量，代表测试标签。
            k：用于预测的近邻数量。
            quiet：若为 True，则不打印提示信息。

        返回值：
            accuracy：该分类器在测试数据上的准确率，以百分比形式表示。为取值范围在 [0, 100] 内的 Python 浮点型数值。
        """
        y_test_pred = self.predict(x_test, k=k) #测试集预测的标签
        num_samples = x_test.shape[0]  #测试样本数量
        num_correct = (y_test == y_test_pred).sum().item()
        accuracy = 100.0 * num_correct / num_samples
        msg = (
            f"Got {num_correct} / {num_samples} correct; "
            f"accuracy is {accuracy:.2f}%"
        )
        if not quiet:
            print(msg)
        return accuracy


def knn_cross_validate(
    x_train: torch.Tensor,
    y_train: torch.Tensor,
    num_folds: int = 5,
    k_choices: List[int] = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100],
):
    """
    交叉验证: 
    最常用的方法：$K$-折交叉验证 (K-Fold Cross-Validation)
    这是你代码中 torch.chunk 试图实现的方法。
    步骤如下：
    1. 分块：将原始数据集随机打乱，并平均分成 $K$ 份（通常 $K=5$ 或 $10$）。
    2. 循环：进行 $K$ 轮训练和评估。
        第 1 轮：用第 1 份做验证集，其余 $K-1$ 份做训练集。
        第 2 轮：用第 2 份做验证集，其余 $K-1$ 份做训练集。...以此类推。
        平均：最后将这 $K$ 次的评估结果（如准确率）取平均值，作为模型最终的性能指标。
    对`KnnClassifier`执行交叉验证。

    参数：
        x_train：形状为 (num_train, C, H, W) 的张量，包含全部训练数据。
        y_train：形状为 (num_train,) 的 int64 类型张量，为训练数据提供标签。
        num_folds：整数，指定要使用的折数。
        k_choices：整数列表，给出待尝试的 k 值。

    返回值：
        k_to_accuracies：字典，将 k 值映射为列表，其中
        k_to_accuracies[k][i] 表示使用 k 近邻的`KnnClassifier`在第 i th 折数据上的准确率。
    """

    # 首先，我们将训练数据划分为数量为num_folds的等份折数。
    x_train_folds = []
    y_train_folds = []
    ##########################################################################
    # TODO: 将训练数据与图像划分为多个折。划分完成后，                              #
    # x_train_folds 和 y_train_folds 应是长度为 num_folds 的列表，              #
    # 其中 y_train_folds[i] 为 x_train_folds[i] 中对应图像的标签向量。            #
    #                                                                        #
    # HINT: torch.chunk                                                      #
    ##########################################################################
    # Replace "pass" statement with your code
    x_train_folds=torch.chunk(x_train,num_folds,dim=0) #按第一维进行折叠 
    #x_train_folds.shape[0]=(1000,3,32,32) 有5个
    y_train_folds=torch.chunk(y_train,num_folds,dim=0)
    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################

    # 一个字典，用于存储在执行交叉验证时找到的不同k值对应的准确率。
    # 执行完交叉验证后，k_to_accuracies[k] 应当是一个长度为num_folds的列表，
    # 其中包含使用k个近邻的KnnClassifier时所得到的各类准确率。
    k_to_accuracies = {}

    ##########################################################################
    # TODO: 执行交叉验证以找到最优的k值。对于k_choices中的每个k值，
    # 运行k近邻算法num_folds次；
    # 在每种情况下，均使用除一个折之外的所有折作为训练数据，将最后一个折作为验证集。
    # 将所有折以及所有k值对应的准确率存储在k_to_accuracies中。                      #                                                                        #
    # HINT: torch.cat                                                        #
    ##########################################################################
    # Replace "pass" statement with your code
    for k in k_choices:
        list_of_acc=[]
        for num_fold in range(num_folds): 
            #x_train_folds_copy[0].shape=(1000,3,32,32)
            x_train_folds_copy=[x for x in x_train_folds] #为了不破坏原始分好的数据，用列表推导式拷贝了一份copy
            y_train_folds_copy=[y for y in y_train_folds]
            #y_train_folds_copy[0].shape=1000
            x_test=x_train_folds_copy[num_fold] #轮流把第0、第1、最后一折作为验证集
            #x_test.shape=(1000,3,32,32)
            y_test=y_train_folds_copy[num_fold]
            #y_test.shape=1000
            del x_train_folds_copy[num_fold] #因为num_fold份去做验证集了，所以要移除它
            del y_train_folds_copy[num_fold]
            x_train=torch.cat(x_train_folds_copy,dim=0) #把剩下的4份拼成训练集
            #x_train.shape=(4000,3,32,32)
            y_train=torch.cat(y_train_folds_copy,dim=0)
            classifier=KnnClassifier(x_train,y_train)
            list_of_acc.append(classifier.check_accuracy(x_test,y_test,k=k))
        k_to_accuracies[k]=list_of_acc

    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################

    return k_to_accuracies


def knn_get_best_k(k_to_accuracies: Dict[int, List]):
    """
    根据knn_cross_validate的交叉验证结果，为k选取最优值。
    若存在多个可选的k值，则应在所有可行结果中选择**最小的k**。

    参数：
        k_to_accuracies：将k值映射至列表的字典，其中
        k_to_accuracies[k][i]表示采用k个近邻的KnnClassifier模型
        在第i折数据上的准确率。

    返回：
        best_k：基于k_to_accuracies信息得出的最优k值
        （若存在多个最优值，则取其中最小的k）。
    """
    best_k = 0
    ##########################################################################
    # TODO: 利用存储在k_to_accuracies中的交叉验证结果来选择k的取值，并将结果存入`best_k`。
    # 你应选择在所有折数中平均准确率最高的k值。   #
    ##########################################################################
    # Replace "pass" statement with your code
    new_dict={}
    for k,accs in sorted(k_to_accuracies.items()):
        #new_dict={1: 0.864, 3: 0.904, 5: 0.884, ...}
        new_dict[k]=sum(accs)/len(accs) #把字典中k对应的值写成平均值
    max_value=max(new_dict.values()) #values()会把字典里所有的值平均分提取出来变成一个List,max找出最大值
    best_k = [k for k,v in new_dict.items() if v==max_value][0] #如果平均值刚好等于我们找的max_value就把k放入List,加[0]表示可能有很多个，取第一个

    ##########################################################################
    #                           END OF YOUR CODE                             #
    ##########################################################################
    return best_k
