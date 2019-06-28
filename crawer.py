# -*- coding: utf-8 -*-  
import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import random
import os
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
def case(var):
    return {
        '所属小区：':0,
        '所在位置：':1,
        '建造年代：':2,
        '房屋类型：':3,
        '产权年限：':4,
        '产权性质：':5,
        '房屋户型：':6,
        '建筑面积：':7,
        '房屋朝向：':8,
        '所在楼层：':9,
        '配套电梯：':10,
        '唯一住房：':11,
        '房屋单价：':12,
        '参考首付：':13,
        '参考月供：':14,
        '装修程度：':15,
        '房本年限：':16,
        '一手房源：':17,
        '核心卖点：':18,
        '专家解读(特色)：':19,
        '专家解读(不足)：':20,
        }.get(var,21)
def get_information():
    dicts = open('urls2.txt','r',encoding='utf-8').read().split('\n')[:-1]
    f = open('final_info1.csv','a',newline='',encoding='utf-8')
    writer=csv.writer(f,dialect='excel')
  #  writer.writerow(('所属小区','所在位置','建造年代','房屋类型','产权年限','产权性质','房屋户型',
   #                 '建筑面积','房屋朝向','所在楼层','配套电梯','唯一住房','房屋单价','参考首付',
    #                '参考月供','装修程度','房本年限','一手房源','核心卖点','专家解读(特色)',
     #                '专家解读(不足)'))
    total = len(dicts)
    i = 24554
    while (i<total):
        url = dicts[i]
        try:
            response = requests.get(url,header)
        except:
            pass
        else:
            print(i)
            soup = BeautifulSoup(response.text, 'html.parser')
            result_li = soup.find_all('li', {'class': 'houseInfo-detail-item'})
            is_alive = soup.find_all('div', {'class':'error-page clearfix'})
            if not len(is_alive):
                if len(result_li)!=0:
                    info = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    #获取房屋信息
                    for result in result_li:
                        label = result.find('div', {'class': 'houseInfo-label text-overflow'}).get_text()
                        content = result.find('div', {'class': 'houseInfo-content'}).get_text()
                        info[case(label)] = content
                    #获取核心卖点
                    temp = soup.find_all('div',{'class':'houseInfo-item-desc'})
                    if len(temp):
                        info[18] = temp[0].get_text()
                    #获取专家解读
                    temp = soup.find_all('dl',{'class':'info-character good-character'})
                    if len(temp):
                        info[19] = temp[0].get_text()
                    temp = soup.find_all('dl',{'class':'info-character bad-character'})
                    if len(temp):
                        info[20] = temp[0].get_text()
                    writer.writerow(info)   
                    i += 1
            else:
                print(is_alive[0].div.span)
                if '抱歉' in str(is_alive[0].div.span):
                    i+= 1
                else:
                    os.system("hsdl -d")
                    os.system("hsdl -c -L \"全国随机\"")
                    time.sleep(5)
    f.close()
def get_all_places():
    all_places = open('places.txt','w')
    region = ['pudong','minhang','baoshan','xuhui','songjiang','jiading','jingan','putuo','yangpu','hongkou','changning','huangpu','qingpu','fengxian','jinshan','chongming','shanghaizhoubian']
    for reg in region:
        time.sleep(1)
        url = 'https://shanghai.anjuke.com/sale/'+str(reg)+'/'
        response = requests.get(url,header)
        soup = BeautifulSoup(response.text, 'html.parser')
        result_li = soup.find_all('div', {'class': 'sub-items'})
        page_url = str(result_li[0])
        soup = BeautifulSoup(page_url, 'html.parser')
        result_href = soup.find_all('a')
        for place in result_href:
            all_places.write(place.attrs['href'][:-127])
            print(place.attrs['href'][:-127])
            all_places.write('\n')
    all_places.close()

def get_all_dicts():
    all_dicts = open('dicts.txt','w')
    all_places = open('places.txt','r').read().split('\n')[:-1]
    for place in all_places:
        for index in range(1,51):
            all_dicts.write(place+'p'+str(index)+'/')
            all_dicts.write('\n')

def get_all_urls():
    all_urls = open('urls3.txt','a',encoding='utf-8')
    dicts = open('dicts.txt','r').read().split('\n')[:-1]
    i = 0
    while(i<len(dicts)):
        p = 50 - i%50
        url = dicts[i]

        try:
            response = requests.get(url,header)
        except:
            time.sleep(3)
        else:
            # 通过BeautifulSoup进行解析出每个房源详细列表并进行打印
            soup = BeautifulSoup(response.text, 'html.parser')
            result_li = soup.find_all('li', {'class': 'list-item'})
            is_alive = soup.find_all('div',{'class':'tab-wrap'})
            if len(is_alive):
                print(i)
                if len(result_li)!=0:
                    for result in result_li:
                        # 由于BeautifulSoup传入的必须为字符串，所以进行转换
                        page_url = str(result)
                        soup = BeautifulSoup(page_url, 'html.parser')
                        # 由于通过class解析的为一个列表，所以只需要第一个参数
                        result_href = soup.find_all('a', {'class': 'houseListTitle'})[0]
                        # 先不做分析，等一会进行详细页面函数完成后进行调用
                        all_urls.write(result_href.attrs['href'])
                        all_urls.write('\n')
                    i += 1
                    p -= 1
                else:
                    i += p
                    p = 50
            else:
                print('time = ',time.time()-bbb)
                print('next i =',i)
                print('next url =',url)
                time.sleep(3)
if __name__ == '__main__':
    #get_all_places()
    #get_all_dicts()
    #get_all_urls()
    get_information()
