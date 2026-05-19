import torch

# Type hints.
from typing import List, Tuple
from torch import Tensor


def hello():
    """
    这是一个示例函数, 我们将尝试导入并运行它,以确保我们的环境在Google Colab上正确设置。
    """
    print('Hello from pytorch101.py!')


def create_sample_tensor() -> Tensor:
    """
    返回一个形状为(3, 2)的torch张量,该张量除了元素(0, 1)被设为10、元素(1, 0)被设为100外,其余元素均为0。

    返回值:
    - 如上所述，形状为 (3, 2) 的张量。
    """
    
    ##########################################################################
    #                     TODO: Implement this function                      #
    ##########################################################################
    # Replace "pass" statement with your code
    x=torch.zeros(3,2)
    x[0,1]=10
    x[1,0]=100
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
    return x


def mutate_tensor(
    x: Tensor, indices: List[Tuple[int, int]], values: List[float]
) -> Tensor:
    """
    根据索引和值对张量x进行修改。具体来说,
    indices是一个由整数索引组成的列表[(i0, j0), (i1, j1), ...],
    values是一个由值组成的列表[v0, v1, ...]。此函数应通过以下设置来修改x: 

    x[i0, j0] = v0
    x[i1, j1] = v1

    依此类推.

    如果相同的索引对在indices中多次出现,你应该将x设置为最后一次出现的那个.

    参数:
        x: 形状为 (H, W) 的张量
        indices: 包含 N 个元组的列表 [(i0, j0), (i1, j1), ..., ]
        values: 包含 N 个值的列表 [v0, v1, ...]

    Returns:
        The input tensor x
    """
    ##########################################################################
    #                     TODO: Implement this function                      #
    ##########################################################################
    # Replace "pass" statement with your code
    for i in enumerate(indices): #i=(序号,元素值)=(0,(0,0)),(1,(1,0)),(2,(1,1))
        x[i[1][0],i[1][1]]=values[i[0]]
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return x


def count_tensor_elements(x: Tensor) -> int:
    """
    计算张量x中的标量元素数量.

    例如,形状为(10,)的张量有10个元素;形状为(3, 4)的张量有12个元素;形状为(2, 3, 4)的张量有24个元素,等等.

    不得使用torch.numel或x.numel函数.输入张量不应被修改.

    参数:
        x:任意形状的张量

    返回：
        num_elements:一个整数,表示x中的标量元素数量
    """
    num_elements = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    #   You CANNOT use the built-in functions torch.numel(x) or x.numel().   #
    ##########################################################################
    # Replace "pass" statement with your code
    num_elements=x.shape[0]*x.shape[1] #shape[0]表示张量,shape[1]表示一个张量的大小
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return num_elements


def create_tensor_of_pi(M: int, N: int) -> Tensor:
    """
    返回一个形状为(M, N)完全填充值3.14的张量

    参数:
        M, N: 用于指定要创建的张量形状的正整数

    返回:
        x:一个形状为(M, N)、填充值为3.14的张量
    """
    x = None
    ##########################################################################
    #         TODO: Implement this function. It should take one line.        #
    ##########################################################################
    # Replace "pass" statement with your code
    x=torch.full((M,N),3.14)
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return x


def multiples_of_ten(start: int, stop: int) -> Tensor:
    """
    返回一个数据类型为torch.float64的张量,该张量包含从start到stop(包括start和stop)
    之间所有10的倍(按顺序排列).如果在这个范围内没有10的倍数,则返回一个形状为(0,)的空张量。

    参数:
        start:要创建的范围的起始值。
        stop:要创建的范围的结束值(stop >= start).

    返回:
        x:float64类型的张量,包含start到stop之间10的倍数.
    """
    assert start <= stop
    x = None     
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    multiples=[x for x in range(start,stop) if x%10==0]
    #print(multiples)
    x =torch.tensor(multiples,dtype=torch.float64)
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return x


def slice_indexing_practice(x: Tensor) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """
    给定一个二维张量x,提取并返回若干子张量,以练习切片索引.
    每个张量都应使用单次切片索引操作创建。

    输入张量不应被修改。

    参数:
    x: 形状为(M，N)的张量——M行、N列,其中M≥3且N≥5.

    返回: 一个元组,包含:
        - last_row: 形状为(N,) 的张量,给出x的最后一行. 它应该是一个一维张量.
        - third_col：形状为（M，1）的张量，给出x的第三列。它应该是一个二维张量。
        - first_two_rows_three_cols：形状为（2，3）的张量，给出x的前两行和前三列中的数据。
        - even_rows_odd_cols：二维张量，包含x中偶数行和奇数列的元素。
    """
    assert x.shape[0] >= 3
    assert x.shape[1] >= 5
    last_row = None
    third_col = None
    first_two_rows_three_cols = None
    even_rows_odd_cols = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    last_row=x[-1]
    third_col=x[:,2:3]
    first_two_rows_three_cols=x[:2,:3]
    even_rows_odd_cols=x[::2,1::2]
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    out = (
        last_row,
        third_col,
        first_two_rows_three_cols,
        even_rows_odd_cols,
    )
    return out


def slice_assignment_practice(x: Tensor) -> Tensor:
    """
    给定一个形状为（M, N）且M >= 4、N >= 6的二维张量，修改其前4行和前6列，使它们等于：

    [0 1 2 2 2 2]
    [0 1 2 2 2 2]
    [3 4 3 4 5 5]
    [3 4 3 4 5 5]

    注意：输入张量的形状不限于（4, 6）。

    你的实现必须遵循以下要求：
    - 你需要在原地修改张量x并返回它
    - 你只能修改前4行和前6列；所有其他元素应保持不变
    - 你只能使用切片赋值操作来修改张量，即将一个整数赋给张量的一个切片
    - 必须使用不超过6次切片操作来达到预期结果

    参数：
        x：一个形状为（M, N）且M >= 4、N >= 6的张量

    返回：
        x
    """
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    x[:2,:1]=0
    x[:2,1:2]=1
    x[:2,2:6]=2
    x[2:4,:4:2]=3
    x[2:4,1:4:2]=4
    x[2:4,4:6]=5
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return x


def shuffle_cols(x: Tensor) -> Tensor:
    """
    按照如下描述对输入张量的列进行重新排序。

    你的实现应该使用一次整数数组索引操作来构造输出张量。输入张量不应被修改。

    参数：
        x：一个形状为（M，N）的张量，其中N ≥ 3

    返回：
        一个形状为（M，4）的张量y，其中：
        - y的前两列是x的第一列的副本
        - y的第三列与x的第三列相同
        - y的第四列与x的第二列相同
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    y=x[:,[0,0,2,1]]
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def reverse_rows(x: Tensor) -> Tensor:
    """
    反转输入张量的行。

    你的实现应该使用一次整数数组索引操作来构造输出张量。输入张量不应被修改。

    你的实现不得使用torch.flip。

    参数：
        x：形状为(M, N)的张量

    返回：
        y：形状为(M, N)的张量，与x相同，但行被反转——y的第一行应等于x的最后一行，
            y的第二行应等于x的倒数第二行，依此类推。
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    y=x[range(x.shape[0])[::-1]]

    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def take_one_elem_per_col(x: Tensor) -> Tensor:
    """
    按照如下描述，通过从输入张量的每一列中选取一个元素来构造一个新的张量。

    输入张量不应被修改，且您只能通过一次索引操作来访问输入张量的数据。

    参数：
        x：一个形状为（M, N）的张量，其中 M >= 4 且 N >= 3。

    返回：
        一个形状为（3,）的张量 y，满足：
        - y 的第一个元素是 x 第一列的第二个元素
        - y 的第二个元素是 x 第二列的第一个元素
        - y 的第三个元素是 x 第三列的第四个元素
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    y=x[[1,0,3],range(x.shape[1])]
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def make_one_hot(x: List[int]) -> Tensor:
    """
    根据一个Python整数列表构建一个独热向量张量。

    你的实现不应使用任何Python循环（包括推导式）。

    参数：
        x：一个包含N个整数的列表

    返回：
        y：形状为（N，C）的张量，其中C = 1 + max(x)，即比x中的最大值大1。y的第n行是x[n]的独热向量表示；
        换句话说，如果x[n] = c，那么y[n, c] = 1；
        y的所有其他元素均为0。y的数据类型应为torch.float32。
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    y=torch.zeros((len(x),max(x)+1))
    y[range(len(x)),x]=1
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def sum_positive_entries(x: Tensor) -> Tensor:
    """
    返回输入张量x中所有正值的总和。

    例如，给定输入张量
    
    x = [[ -1   2   0 ],
         [  0   5  -3 ],
         [  8  -9   0 ]]
    
    此函数应返回sum_positive_entries(x) = 2 + 5 + 8 = 15
    
    你的输出应该是一个Python整数，而不是PyTorch标量。
    
    你的实现不应修改输入张量，且不应使用任何显式的Python循环（包括推导式）。你应该仅通过一次比较操作和一次索引操作来访问输入张量的数据。
    
    参数：
        x：任意形状的张量，数据类型为torch.int64
    
    返回：
        pos_sum：Python整数，表示x中所有正值的总和
    """
    pos_sum = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    mask=x>0 
    pos_sum=x[mask].sum()
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return pos_sum


def reshape_practice(x: Tensor) -> Tensor:
    """
    给定一个形状为(24,)的输入张量，返回一个形状为(3, 8)的重塑张量y，使得

    y = [[x[0], x[1], x[2],  x[3],  x[12], x[13], x[14], x[15]],
         [x[4], x[5], x[6],  x[7],  x[16], x[17], x[18], x[19]],
         [x[8], x[9], x[10], x[11], x[20], x[21], x[22], x[23]]]

    你必须通过对x执行一系列重塑操作（view、t、transpose、permute、contiguous、reshape等）来构造y。输入张量不应被修改。

    参数：
        x：形状为(24,)的张量

    返回：
        y：x的重塑版本，形状为(3, 8)，如上述描述
    """
    y = None
    ##########################################################################
    # 1. view(2, 3, 4): 将 24 拆解为 (前/后12个, 行数, 每一块的列数)
    #    此时 index 布局为:
    #    [[[0,1,2,3], [4,5,6,7], [8,9,10,11]],  <-- 前12个
    #     [[12,13,14,15], [16,17,18,19], [20,21,22,23]]] <-- 后12个
    #
    # 2. permute(1, 0, 2): 交换前两个维度，让形状变为 (3, 2, 4)
    #    这样每一行对应的两组数据 ([0,1,2,3] 和 [12,13,14,15]) 就紧挨在一起了
    #
    # 3. reshape(3, 8): 将最后两维 (2, 4) 合并为 8
    ##########################################################################
    y = x.view(2, 3, 4).permute(1, 0, 2).reshape(3, 8)                     #
    ##########################################################################
    # Replace "pass" statement with your code
    # print(x.view(2,3,4).permute(1,0,2))#(3,2,4) 
    y=x.view(2,3,4).permute(1,0,2).reshape(3,8)
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def zero_row_min(x: Tensor) -> Tensor:
    """
    返回输入张量x的一个副本，其中每一行的最小值已被设置为0。

    例如，如果x是：
    x = torch.tensor([
        [10, 20, 30],
        [2, 5, 1]
    ])

    那么y = zero_row_min(x)应该是：
    torch.tensor([
        [0, 20, 30],
        [2, 5, 0]
    ])

    你的实现应该使用归约和索引操作。你不应该使用任何Python循环（包括推导式）。输入张量不应被修改。

    参数：
        x：形状为（M，N）的张量

    返回：
        y：形状为（M，N）的张量，是x的一个副本，只是每行的最小值被替换为0。
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    #   1.克隆原张量，避免原地修改
    y=x.clone()

    #   2.找到每一行最小值的列索引
    #   dim=1表示在行方向上搜索,返回每一行最小值所在位置
    row_min_idxs=torch.argmin(x,dim=1)

    #   3.准备行索引: [0,1,2,...M-1]
    rows=range(y.shape[0])
    #   4.使用高级索引将对应位置设为0
    #y[rows,min_indices]会选中(0,min_idx0),(1,min_idx1)...
    y[rows,row_min_idxs]=0

    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def batched_matrix_multiply(
    x: Tensor, y: Tensor, use_loop: bool = True
) -> Tensor:
    """
   在形状为（B, N, M）的张量x和形状为（B, M, P）的张量y之间执行批量矩阵乘法。

    根据use_loop的值，这会调用batched_matrix_multiply_loop或batched_matrix_multiply_noloop来执行实际计算。
    你无需在此处实现任何内容。

    参数：
        x：形状为（B, N, M）的张量
        y：形状为（B, M, P）的张量
        use_loop：是否使用显式的Python循环

    返回：
        z：形状为（B, N, P）的张量，其中形状为（N, P）的z[i]是形状为（N, M）的x[i]和形状为（M, P）的y[i]进行矩阵乘法的结果。
        输出z应与x具有相同的数据类型。 
    """
    if use_loop:
        return batched_matrix_multiply_loop(x, y)
    else:
        return batched_matrix_multiply_noloop(x, y)


def batched_matrix_multiply_loop(x: Tensor, y: Tensor) -> Tensor:
    """
    在形状为（B, N, M）的张量x和形状为（B, M, P）的张量之间执行批量矩阵乘法。

    此实现应使用一个显式的批处理维度B循环来计算输出。

    参数：
        x：形状为（B, N, M）的张量
        y：形状为（B, M, P）的张量

    返回：
        z：形状为（B, N, P）的张量，其中形状为（N, P）的z[i]是形状为（N, M）的x[i]与形状为（M, P）的y[i]进行矩阵乘法的结果。
        输出z应与x具有相同的数据类型。
    """
    z = None 
    ###########################################################################
    #                      TODO: Implement this function                      #
    ###########################################################################
    # Replace "pass" statement with your code
    #z是一个(B,N,P)的张量
    z=torch.zeros((x.shape[0],x.shape[1],y.shape[2]),dtype=x.dtype)
    for i in range(x.shape[0]):
        z[i]=x[i].mm(y[i]) #mm是计算矩阵与矩阵的乘积
        #x[i]是一个(N,M)的张量，y[i]是一个(M,P)的张量
    ###########################################################################
    #                           END OF YOUR CODE                              #
    ###########################################################################
    return z


def batched_matrix_multiply_noloop(x: Tensor, y: Tensor) -> Tensor:
    """
    在形状为（B, N, M）的张量x和形状为（B, M, P）的张量之间执行批量矩阵乘法。

    此实现不应使用任何显式的Python循环（包括推导式）。

    提示：torch.bmm 

    参数：
        x：形状为（B, N, M）的张量
        y：形状为（B, M, P）的张量

    返回：
        z：形状为（B, N, P）的张量，其中形状为（N, P）的z[i]是形状为（N, M）的x[i]与形状为（M, P）的y[i]进行矩阵乘法的结果。
        输出z应与x具有相同的数据类型。
    """
    z = None
    ###########################################################################
    #                      TODO: Implement this function                      #
    ###########################################################################
    # Replace "pass" statement with your code
    pass
    z = torch.bmm(x, y) #bmm就是一个批量执行矩阵乘法的内置函数，输入三维张量
    #假设输入1:(B,N,M),输入2:(B,M,P)结果是(B,N,P)
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
    return z


def normalize_columns(x: Tensor) -> Tensor:
    """
    对矩阵x的列进行标准化处理，方法是减去每列的均值并除以每列的标准差。你需要返回一个新的张量，输入的张量不应被修改。

    更具体地说，给定一个形状为（M, N）的输入张量x，生成一个形状为（M, N）的输出张量y，其中y[i, j] =（x[i, j] - mu_j）/ sigma_j，这里的mu_j是列x[:, j]的均值。

    你的实现不应使用任何显式的Python循环（包括推导式）；只能使用张量的基本算术运算（+、-、*、/、**、sqrt）、求和归约函数以及用于促进广播的重塑操作。不应使用torch.mean、torch.std及其实例方法变体x.mean、x.std。

    参数：
        x：形状为（M, N）的张量。

    返回：
        y：如上所述的形状为（M, N）的张量。它应与输入x具有相同的数据类型。
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    y=torch.clone(x)
    mean=y.sum(dim=0)/y.shape[0] #按列求平均值
    std=(((y-mean)**2).sum(dim=0)/(y.shape[0]-1))**0.5 #广播机制让y-mean自动每一行做减法
    y=(y-mean)/std
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def mm_on_cpu(x: Tensor, w: Tensor) -> Tensor:
    """
    在CPU上执行矩阵乘法。

    你无需为该函数实现任何逻辑。

    参数：
        x：形状为(A, B)的张量，位于CPU上
        w：形状为(B, C)的张量，位于CPU上

    返回：
        y：上述定义的形状为(A, C)的张量，不得位于GPU上。
    """
    y = x.mm(w)
    return y


def mm_on_gpu(x: Tensor, w: Tensor) -> Tensor:
    """
    在图形处理器（GPU）上执行矩阵乘法运算。

    具体而言，给定两个输入张量，该函数应执行以下操作：
    (1) 将每个输入张量迁移至GPU；
    (2) 在GPU上对张量执行矩阵乘法运算；
    (3) 将运算结果迁移回中央处理器（CPU）

    将张量迁移至GPU时，请使用`your_tensor.cuda()`操作

    参数：
        x：形状为(A, B)的张量，位于CPU上
        w：形状为(B, C)的张量，位于CPU上

    返回值：
        y：符合上述描述、形状为(A, C)的张量，该张量不应存储在GPU上
    """
    y = None
    ##########################################################################
    #                      TODO: Implement this function                     #
    ##########################################################################
    # Replace "pass" statement with your code
    x=x.cuda()
    w=w.cuda()
    y=x.mm(w).cpu()
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def challenge_mean_tensors(xs: List[Tensor], ls: Tensor) -> Tensor:
    """
    计算给定张量列表中每个张量的均值。

    具体而言，输入为包含N个张量的列表（1 ≤ N ≤ 10000）。列表中的第i个张量长度为Ki（1 ≤ Ki ≤ 10000）。返回一个形状为(N,)的张量，其第i个元素为输入列表中第i个张量的均值。
    可假定所有张量均位于同一设备（CPU或GPU）。
    
    你的实现不得使用任何显式的Python循环（包括推导式）。
    
    参数：
        xs：包含N个一维张量的列表。
        ls：`xs`中各张量的长度。一个int64类型的张量，长度与`xs`相同，其中`ls[i]`表示`xs[i]`的长度。
    
    返回：
        y：形状为(N,)的张量，其中`y[i]`为`xs[i]`的均值。
    """

    y = None
    ##########################################################################
    # TODO: Implement this function without using `for` loops and store the  #
    # mean values as a tensor in `y`.                                        #
    ##########################################################################
    # Replace "pass" statement with your code
    pass
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return y


def challenge_get_uniques(x: torch.Tensor) -> Tuple[Tensor, Tensor]:
    """
    Get unique values and first occurrence from an input tensor.

    Specifically, the input is 1-dimensional int64 Tensor with length N. This
    tensor contains K unique values (not necessarily consecutive). Your
    implementation must return two tensors:
    1. uniques: int64 Tensor of shape (K, ) - giving K uniques from input.
    2. indices: int64 Tensor of shape (K, ) - giving indices of the first
       occurring unique values.

    Concretely, this should hold True: x[indices[i]] = uniques[i] 

    Your implementation should not use any explicit Python loops (including
    comprehensions), and should not require more than O(N) memory. Creating
    new tensors larger than input tensor is not allowed. If you wish to
    create new tensors like input tensor, use `input.clone()`.

    You may use `torch.unique`, but you will receive half credit for that.

    Args:
        x: Tensor of shape (N, ) with K <= N unique values.

    Returns:
        uniques and indices: Se description above.
    """

    uniques, indices = None, None
    ##########################################################################
    # TODO: Implement this function without using `for` loops and within     #
    # O(N) memory.                                                           #
    ##########################################################################
    # Replace "pass" statement with your code
    pass
    ##########################################################################
    #                            END OF YOUR CODE                            #
    ##########################################################################
    return uniques, indices
