## 基于深度学习的安居客二手房房价预测

### 1. **项目简介**

本项目爬取了[安居客上的上海地区二手房信息](https://shanghai.anjuke.com/sale/?from=navigation)，进行了一系列
数据预处理工作，并利用处理后的数据建立了基于深度学习的二手房房价回归预测模型

### 2. **项目文件结构**

本项目源码文件结构与文件内容大致说明如下：

```

Top
│   README.md
│   data_org.py   定义了数据组织对象，负责加载数据    
│   dlmodel.py    定义了项目中使用的深度学习模型 
│   model_train.py  深度学习模型训练过程定义脚本
│   r2_plot.py      r2分数曲线绘制脚本   
│   crawer.py      爬虫   
│
└─── preprocess
│   │   preprocessing.ipynb  预处理过程文件
│   │   preprocess.py   预处理方法定义
│   │   depart.py      对文本分词，转化为向量，同时依据相关性获取add_param.py中所需的关键字
│   │   add_param.py   提取文本信息中的关键字作为新的参数
│   │
│
└─── data
    │   house_pos.csv   完成预处理后的标签类属性文件
    │   house_info.csv  爬取的原始数据文件
    │   vector.txt      文本信息词向量文件
    │



```

#### 3. 运行环境

+ 平台： windows 10 
+ python语言版本： 3.7.x
+ 代理：花生代理
  
