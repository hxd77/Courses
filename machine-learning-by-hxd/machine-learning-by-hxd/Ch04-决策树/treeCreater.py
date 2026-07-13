"""
拟合函数中，X支持pd.DataFrame数据类型；y暂只支持pd.Series类型，其他数据类型未测试，
目前在西瓜数据集上和sklearn中自带的iris数据集上运行正常，以后若发现有其他bug，再修复。
"""

import numpy as np
import pandas as pd
from sklearn.utils.multiclass import type_of_target


class Node(object):
    def __init__(self):
        self.feature_name=None
        self.feature_index=None
        self.subtree={}
        self.impurity=None
        self.is_continuous=None
        self.split_value=None
        self.is_leaf=False
        self.leaf_class=None
        self.leaf_num=None
        self.high=1


class DecisionTree(object):
    """
    没有针对缺失值的情况进行处理
    """
    def __init__(self,criterion='gini',pruning=None):
        """
        :param criterion: 划分方法选择,'gini','infogain','gainratio'三种
        :param pruning: 是否剪枝. 'pre_pruning', 'post_pruning'
        """

        assert criterion in ('gini','infogain','gainratio')
        assert pruning in (None,'pre_pruing','post_pruning')
        self.criterion=criterion
        self.pruning=pruning

    def fit(self,X_train,y_train,X_val=None,y_val=None):                                                                                                                                                                                                                                                                                                                                                               
        """
        生成决策树
        -------
        :param X:  只支持DataFrame类型数据，因为DataFrame中已有列名，省去一个列名的参数。不支持np.array等其他数据类型
        :param y:
        :return:
        """
        
        if self.pruning is not None and (X_val is None or y_val is None):
            raise Exception('you must input X_val and y_val if you are goint to pruning')
        
        #重置数据索引,
        X_train.reset_index(inplace=True,drop=True)
        y_train.reset_index(inplace=True,drop=True)

        if X_val is not None:
            X_val.reset_index(inplace=True,drop=True)
            y_val.reset_index(inplace=True,drop=True)
        self.columns=list(X_train.columns) 
        self.tree_=self.generate_tree(X_train,y_train)

        #预剪枝
        if self.pruning=='pre_pruning':
            self.pruning.pre_pruning(X_train,y_train,X_val,y_val,self.tree_)
        elif self.pruning=='post_pruning':
            self.pruning.post_pruning(X_train,y_train,X_val,y_val,self.tree_)
        return self

    def generate_tree(self,X,y):
        my_tree=Node()
        my_tree.leaf_num=0
        if y.unique()==1: #属于同一类别,说明当前节点下所有样本已经属于同一类，直接生成叶子节点
            my_tree.is_leaf=True
            my_tree.leaf_class=y.values[0]
            my_tree.high=0 #高度为0
            my_tree.leaf_num+=1  #
            return my_tree
        
        if X.empty: #特征用完了，用当前样本中最多的类别作为叶子节点类别
            my_tree.is_leaf=True
            my_tree.leaf_class=pd.value_counts(y).index[0] #选择出现最多的类别作为预测结果
            my_tree.high=0 #叶子节点高度为0
            my_tree.leaf_num+=1 #该节点本身是一个叶子
            return my_tree 
        
        best_feature_name,best_impurity=self.choose_best_feature_to_split(X,y)


    
    def choose_best_feature_to_split(self,X,y):
        assert self.criterion in ('gini','infogain','gainratio')
        if self.criterion=='gini': #gini指数
            return self.choose_best_feature_gini(X,y)
        elif self.criterion=='infogain': #信息增益
            return self.choose_best_feature_infogain(X,y)
        elif self.criterion=='gainratio': #增益率
            return self.choose_best_feature_gainratio(X,y)
    
    #遍历所有特征，计算每个特征切分数据后的gini指数，选gini指数最小的特征作为最佳划分特征
    def choose_best_feature_gini(self,X,y):
        features=X.columns
        best_feature_name=None
        best_gini=[float('inf')] #先将当前最优gini指数设置为无穷大
        for feature_name in features: #遍历每一个特征
            is_continuous=type_of_target(X[feature_name])=='continuous' #判断特征是否为连续数值
            gini_index=self.gini_index(X[feature_name],y,is_continuous)
            if gini_index[0]<best_gini[0]:
                best_feature_name=feature_name
                best_gini=gini_index
        return best_feature_name,best_gini

    def gini_index(self,feature,y,is_continuous=False):
        '''
        计算基尼指数， 对于连续值，选择基尼系统最小的点，作为分割点
        -------
        :param feature:
        :param y:
        :return:
        '''
        m=y.shape[0] #样本总数
        unique_value=pd.unique(feature) #特征中所有不重复取值
        if is_continuous: #连续特征情况
            unique_value.sort()  #排序,比如[20,22,25,28]
            split_point_set=[
                (unique_value[i]+unique_value[i+1])/2 for i in range(len(unique_value)-1)
            ]
            #计算相邻值的中点:[21.0, 23.5, 26.5]
            '''
            于是可以这么划分:
            温度 <= 21.0 和 > 21.0
            温度 <= 23.5 和 > 23.5
            温度 <= 26.5 和 > 26.5
            '''

            min_gini=float('inf')
            min_gini_point=None
            #遍历每个划分点
            for split_point_ in split_point_set:
                Dv1=y[feature<=split_point_]
                Dv2=y[feature>split_point_]
                #分别计算两个子集的gini指数，并按样本数加权:
                gini_index=(Dv1.shape[0]/m*self.gini(Dv1)+Dv2.shape[0]/m*self.gini(Dv2))
                if gini_index<min_gini:
                    min_gini=gini_index
                    min_gini_point=split_point_
            
            return [min_gini,min_gini_point]
        #离散特征情况
        else:
            gini_index=0
            #代码逐个值取出对应的标签集合
            '''
            比如unique_value = ['晴', '雨', '阴']
            y = ['是', '是', '是', '否', '否']
            value='晴',Dv=['否','否']
            value = '雨'Dv = ['是', '是']
            '''
            for value in unique_value:
                Dv=y[feature==value]
                m_dv=Dv.shape[0] #每个类别占的比例,比如这里Dv=2
                gini=self.gini(Dv)
                gini_index+=m_dv/m*gini 
            return [gini_index]
        

    def gini(self,y):
        p=pd.value_counts(y)/y.shape[0] #每个类别所占比例
        gini=1-np.sum(p**2)
        return gini
    
    #按照信息增益来选择划分
    def choose_best_feature_infogain(self,X,y):
        '''
        以返回值中best_info_gain 的长度来判断当前特征是否为连续值，若长度为 1 则为离散值，若长度为 2 ， 则为连续值
        :param X: 当前所有特征的数据 pd.DaraFrame格式
        :param y: 标签值
        :return:  以信息增益来选择的最佳划分属性，第一个返回值为属性名称，
        '''
        features=X.columns
        best_feature_name=None
        best_info_gain=[float('-inf')]
        entD=self.entropy(y)
        for feature_name in features:
            is_continuous=type_of_target(X[feature_name])=='continuous'
            info_gain=self.info_gain(X[feature_name],y,entD,is_continuous) #返回[gain]
            if info_gain[0]>best_info_gain[0]:
                best_feature_name=feature_name
                best_info_gain=info_gain
        return best_feature_name,best_info_gain

    def info_gain(self,feature,y,entD,is_continuous=False):
        '''
        计算信息增益
        ------
        :param feature: 当前特征下所有样本值
        :param y:       对应标签值
        :return:        当前特征的信息增益, list类型，若当前特征为离散值则只有一个元素为信息增益，若为连续值，则第一个元素为信息增益，第二个元素为切分点
        '''
        m=y.shape[0]
        unique_value=pd.unique(feature) #比如这里feature是{青绿，乌黑，浅白}
        if is_continuous: #连续值
            unique_value.sort() #排序，用于建立分割点
            split_point_set=[(unique_value[i]+unique_value[i+1])/2 for i in range(len(unique_value)-1)]
            min_ent=float('inf') 
            min_ent_point=None
            for split_point_ in split_point_set:
                Dv1=y[feature<=split_point_]
                Dv2=y[feature>split_point_]
                feature_ent_=Dv1.shape[0]/m *self.entropy(Dv1)+Dv2.shape[0]/m*self.entropy(Dv2)

                if feature_ent_<min_ent:
                    min_ent=feature_ent_
                    min_ent_point=split_point_
            gain=entD-min_ent

            return [gain,min_ent_point]
        else:
            feature_ent=0
            for value in unique_value: 
                Dv=y[feature==value] #当前特征中取值为value的样本，即D^{v}
                feature_ent+=Dv.shape[0]/m*self.entropy(Dv)
            gain=entD-feature_ent #式子4.2
            return [gain]

    #信息熵函数
    def entropy(self,y):
        p=pd.value_counts(y)/y.shape[0] #计算各类样本所占比率
        ent=np.sum(-p*np.log2(p))
        return ent


    #从增益率选择特征进行划分
    def choose_best_feature_gainratio(self,X,y):
        '''
        以返回值中best_gain_ratio 的长度来判断当前特征是否为连续值，若长度为 1 则为离散值，若长度为 2 ， 则为连续值
        :param X: 当前所有特征的数据 pd.DaraFrame格式
        :param y: 标签值
        :return:  以信息增益率来选择的最佳划分属性，第一个返回值为属性名称，第二个为最佳划分属性对应的信息增益率
        '''
        features=X.columns;
        best_feature_name=None
        best_gain_ratio=[float['-inf']]
        entD=self.entropy(y)

        for feature_name in features:
            is_continuous=type_of_target(X[feature_name])=='contiunous'
            info_gain_ratio=self.info_gainRatio(X[feature_name],y,entD,is_continuous)

    def info_gainRatio(self,feature,y,entD,is_continuous=False):
        '''
        计算信息增益率 参数和info_gain方法中参数一致
        ------
        :param feature:
        :param y:
        :param entD:
        :return:
        '''
        if is_continuous:
            # 对于连续值，以最大化信息增益选择划分点之后，计算信息增益率，注意，在选择划分点之后，需要对信息增益进行修正，要减去log_2(N-1)/|D|，N是当前特征的取值个数，D是总数据量。
            # 修正原因是因为：当离散属性和连续属性并存时，C4.5算法倾向于选择连续特征做最佳树分裂点
            # 信息增益修正中，N的值，网上有些资料认为是“可能分裂点的个数”，也有的是“当前特征的取值个数”，这里采用“当前特征的取值个数”。
            # 这样 (N-1)的值，就是去重后的“分裂点的个数” , 即在info_gain函数中，split_point_set的长度，个人感觉这样更加合理。有时间再看看原论文吧。
            gain,split_point=self.info_gain(feature,y,entD,is_continuous)
            #计算左右两本样本比例
            '''
            | 温度 | 是否出去 |
            |---:|---|
            | 20 | 否 |
            | 22 | 否 |
            | 25 | 是 |
            | 28 | 是 |
            假设:
            温度 <= 23.5
            温度 > 23.5
            <= 23.5：2 个样本，占 2/4 = 0.5
            > 23.5：2 个样本，占 2/4 = 0.5
            '''
            p1=np.sum(feature<=split_point)/feature.shape[0] #小于或等于划分点样本
            p2=1-p1

            #计算这个二分划分的IV
            IV=-(p1*np.log2(p1)+p2*np.log2(p2))
            #修正信息增益，再除以IV,额外减去一个惩罚项
            gain_ratio=(gain-np.log2(feature.nunique())/len(y))/IV
            return [gain_ratio,split_point]
        else:
            p=pd.value_counts(feature)/feature.shape[0] #当前特征下各取值所占比率
            IV=np.sum(-p*np.log2(p))
            gain_ratio=self.info_gain(feature,y,entD,is_continuous)[0]/IV
            return [gain_ratio]
        


        
    
