import torch 
import torch.nn as nn
import numpy as np


class MLSTM(nn.Module):
    def __init__(self):
        super(MLSTM, self).__init__()
        '''
        对于一般标称数据项，使用MLP生成特征向量；
        对于文本向量，使用LSTM生成特征向量
        '''
        #MLP生成长度为32的特征向量
        self.MLP = nn.Sequential(
            nn.Linear(20,128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64,32)
        )
        #LSTM生成长度为50的特征向量
        self.lstm = nn.LSTM(30,50,1,batch_first=True)
        #使用长度为82的特征向量进行回归，这里输出节点设为1
        self.regression = nn.Linear(82,1)
        self.train()

    def forward(self,x):
        #去除填充值
        label = x[:,0,0:20]
        wordvec = x[:,1:,:]
        feature_1 = self.MLP(label)
        feature_2,_ = self.lstm(wordvec)
        #采用LSTM输出序列的最后一项组为特征
        feature_2 = feature_2[:,-1,:]
        feature = torch.cat((feature_1,feature_2),1)
        price = self.regression(feature)
        return price
