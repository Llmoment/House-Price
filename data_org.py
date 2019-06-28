import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#DATA_PATH = "./filled_data.csv"
DATA_PATH = "house_pos.csv"

class DataOrganizer():
    def __init__(self, path):
        self.data = pd.read_csv(path, encoding='utf_8_sig')
        self.data = self.data.values
    
    def load_data(self):
        self.price = self.data[:,19]
        self.label = np.delete(self.data,[0,11,19],axis=1)
        zero_matrix = np.zeros(shape=(self.label.shape[0], 10))
        self.label = np.hstack((self.label,zero_matrix))
        self.dataset = np.zeros(shape=(self.label.shape[0],51,30))

        vecfile = open('vector.txt','r',encoding='UTF-8')
        for i in range(self.label.shape[0]-1000):
            try:
                line = eval(vecfile.readline())
                wordvec = np.array(line)
                brock = np.vstack((self.label[i],wordvec))
                self.dataset[i] = brock
            except:
                print("errot in ",i)
        
        x_train, x_test, y_train, y_test = train_test_split(self.dataset, self.price, test_size=0.15, random_state=0)

        return x_train,x_test,y_train,y_test
    
    def load_data_test(self):
        self.dataset = np.random.random((200,51,30))
        self.price = np.random.random((200))
        x_train, x_test, y_train, y_test = train_test_split(self.dataset, self.price, test_size=0.15, random_state=0)

        return x_train,x_test,y_train,y_test





        