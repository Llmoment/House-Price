import csv
def extract():
    f1 = open('house_3.csv','r',newline='',encoding='utf-8-sig')
    f2 = open('house_text.csv','r',newline='',encoding='utf-8-sig')
    f3 = open('house_add.csv','w',newline='',encoding='utf-8-sig')
    writer = csv.writer(f3)
    reader = csv.reader(f1)
    base = []
    for house in reader:
        base.append(house)
    reader = csv.reader(f2)
    add = [['医院','医疗','医保','三甲','保健院','医学院','门诊部','医学中心','卫生院'],
           ['地铁','交通','公交','号线','停车','轻轨','客运','主干道','车位'],
           ['学校','幼儿园','小学','中学','名校','小學','幼稚园','初中','教育']]
    count = 0
    for house in reader:
        addnum = [0,0,0]
        for i in range(3):
            for i1 in add[i]:
                if (i1 in house[1]) or (i1 in house[2]):
                    addnum[i] = 1
                    break
                elif i1 in house[3]:
                    addnum[i] = -1
                    break
        base[count] += addnum
        writer.writerow(base[count])     
        count += 1
    f1.close()
    f2.close()
    f3.close()
if __name__ == '__main__':
    extract()
