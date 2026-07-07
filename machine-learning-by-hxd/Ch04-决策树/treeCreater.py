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
        if self.criterion=='gini':
            return self.choose_best_feature_gini(X,y)
        elif self.criterion=='infogain': #信息增益
            return self.choose_best_feature_infogain(X,y)
        elif self.criterion=='gainratio':
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
            
            #离散特征
            else:
                gini_index=0
                for value in unique_value:
                    Dv=y[feature==value]

    def gini(self,y):
        p=pd.value_counts(y)/y.shape[0] #每个类别所占比例
        gini=1-np.sum(p**2)
        return gini
        


