import pandas as pd 
import numpy as np
import random
import os
from collections import Counter

LABEL_DATA_PATH = './house_label.csv'
TEXT_DATA_PATH = './house_text.csv'
DATA_PATH = './house_info.csv'
DATA_PATH_2 = './house_4.csv'

class Preprocessor:
    def __init__(self):
        if not os.path.exists(LABEL_DATA_PATH):
            self._split_file()
        self.label = pd.read_csv(DATA_PATH_2, encoding='utf_8_sig')
        #self.fill_all_unknown()
        
    
    def _split_file(self):
        """
        将原数据分为文字描述和基本标签信息，并去除重复的行
        """
        self.data = pd.read_csv(DATA_PATH, encoding='utf_8_sig')
        feature = ['所属小区', '所在位置', '建造年代', '房屋类型', '产权年限', '产权性质', '房屋户型', '建筑面积', '房屋朝向', '所在楼层', '配套电梯', '唯一住房', '房屋单价', '参考首付', '参考月供', '装修程度', '房本年限', '一手房源','核心卖点', '专家解读(特色)', '专家解读(不足)']
        temp=pd.DataFrame([feature],columns=feature)
        self.data = temp.append(self.data,ignore_index=True)
        self.data.to_csv('house_new2.csv', sep=',',encoding='utf_8_sig')
        self.data = self.data.drop(labels='Unnamed: 0', axis=1)
        self.data = self.data.drop_duplicates(keep='first')
        self.data.drop(0, axis=0, inplace=True)
        self.data.index=range(self.data.shape[0])
        #文字描述数据
        text = pd.DataFrame(self.data, columns=['核心卖点', '专家解读(特色)', '专家解读(不足)'])
        text.to_csv(TEXT_DATA_PATH, sep=',', encoding='utf_8_sig')
        #标签类数据
        label = pd.DataFrame(self.data, columns=['所属小区', '所在位置', '建造年代', '房屋类型', '产权年限', '产权性质', '房屋户型', '建筑面积', '房屋朝向', '所在楼层', '配套电梯', '唯一住房', '房屋单价', '参考首付', '参考月供', '装修程度', '房本年限', '一手房源'])
        label.to_csv(LABEL_DATA_PATH, sep=',',encoding='utf_8_sig')
        print("Finished file split.")
    
    def fill_all_unknown(self):
        lost_feature = ['建造年代','房屋类型','产权性质','配套电梯','唯一住房','房本年限']
        lost_feature_2 = ['产权年限']
        for item in lost_feature:
            self.label = self.fill_unknown(item, self.label, 'unknown')
        for item in lost_feature_2:
            self.label = self.fill_unknown(item, self.label, 0)
        self.label = self.label.drop(labels='Unnamed: 0', axis=1)
        self.label.to_csv('house_4.csv', sep=',',encoding='utf_8_sig')

    def fill_unknown(self, feature, data, flag):
        '''
        args:
            feature: 特征名
            data: 数据集
        return:
            对样本缺失值进行填补后的数据集
        '''
        distrib = Counter(data[feature].to_list())
        distrib.pop(flag)
        count = 0
        #计算某值出现概率
        for key in distrib.keys():
            count += distrib[key]
        for key in distrib.keys():
            distrib[key] = distrib[key] / float(count)

        for i in range(data.shape[0]):
            if data.loc[i, feature] == flag:
                #根据频率分布进行随机填补
                data.loc[i, feature] = self.ran_gen(distrib)
        return data

    def ran_gen(self, distrib):
        '''
        args:
            distrib: 数据集某属性的频率
        return:
            依据频率随机生成的属性值
        '''
        ran_num = random.uniform(0,1)
        procum = 0.0
        for key in distrib.keys():
            procum += distrib[key]
            if ran_num < procum:
                return key

    
    

Preprocessor()






