import torch 
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torch.autograd as autograd
import numpy as np
from dlmodel import MLSTM
from data_org import *
from sklearn.metrics import r2_score


#定义超参数
BATCH_SIZE = 80
LR = 0.0005
EPOCH = 25
DATA_PATH = "house_pos.csv"

dataorg = DataOrganizer(DATA_PATH)
# 组织数据集
x_train,x_test,y_train,y_test = dataorg.load_data()
print(x_train.shape)
print(y_train.shape)
x_train = torch.from_numpy(x_train).float()
x_test = torch.from_numpy(x_test).float()
y_train = torch.from_numpy(y_train).float()
y_test = torch.from_numpy(y_test).float()

train_dataset = data.TensorDataset(x_train,y_train)
test_dataset = data.TensorDataset(x_test,y_test)

#按照batch_size分割训练集
train_loader = data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = data.DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

r2_list = []
r2_list_test = []

model = MLSTM()

if torch.cuda.is_available():
    model.cuda()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LR)


for epoch in range(EPOCH):
    model.train()
    print("\n")
    print('*' * 10)
    print("epoch {}".format(epoch + 1))
    print('*' * 10)

    running_loss = 0.0
    running_r2 = 0.0
    plt_r2 = 0.0
    #定义训练过程
    for i, data in enumerate(train_loader, 1):
        entrys, price = data
        
        if torch.cuda.is_available():
            entrys = entrys.cuda()
            price = price.cuda()
        
        out = model(entrys)
        out = out.squeeze()
        loss = criterion(out, price)
        out_cpu = out.cpu().detach().numpy()
        price_cpu = price.cpu().numpy()
        #计算r2分数
        r2score = r2_score(price_cpu, out_cpu)
        running_r2 += r2score
        plt_r2 += r2score
        running_loss += loss.item()

        if i % 20 == 0:
            r2_list.append(plt_r2/20)
            plt_r2 = 0.0

        if  i % 50 == 0:
            print("Batch r2: {:.6f}".format(running_r2/i))
            print("Batch loss: {:.6f}".format(running_loss /i))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    #模型评价
    model.eval()
    eval_loss = 0.
    eval_r2 = 0.
    for i, data in enumerate(test_loader, 1):
        entrys, price = data
        if torch.cuda.is_available():
            entrys = entrys.cuda()
            price = price.cuda()

        out = model(entrys)
        out = out.squeeze()
        loss = criterion(out, price)
        out_cpu = out.cpu().detach().numpy()
        price_cpu = price.cpu().numpy()
        r2score = r2_score(price_cpu, out_cpu)
        eval_r2 += r2score
        eval_loss += loss.item()

    print("evaling module:")
    print('*'*10)
    print("eval r2: {:.6f}".format(eval_r2*BATCH_SIZE/len(test_dataset)))
    print("The eval loss is: {:.6f}".format((eval_loss * BATCH_SIZE)/len(test_dataset)))
    r2_list_test.append(eval_r2*BATCH_SIZE/len(test_dataset))

np.savetxt("r2_score.txt", r2_list)
np.savetxt("r2_score_test.txt", r2_list_test)





