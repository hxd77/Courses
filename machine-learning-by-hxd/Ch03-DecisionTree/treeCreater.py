"""
拟合函数中，X支持pd.DataFrame数据类型；y暂只支持pd.Series类型，其他数据类型未测试，
目前在西瓜数据集上和sklearn中自带的iris数据集上运行正常，以后若发现有其他bug，再修复。
"""

import numpy as np
import pandas as pd


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
