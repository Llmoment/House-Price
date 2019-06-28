import jieba
import csv
from gensim.models import word2vec

# 创建停用词列表
def stopwordslist():
    stfile = open('stop_words.txt',encoding='UTF-8')
    stopwords = [line.strip() for line in stfile.readlines()]
    stfile.close()
    return stopwords
#获取需要分词的语句
def get_sentence():
    csvfile = open('house_text.csv','r',encoding='UTF-8')
    reader = csv.reader(csvfile)
    core_info = []
    for house in reader:
        core_info.append(house[2])
    csvfile.close()
    return core_info
#对每一段单独分词
def depart_for_each():
    departfile = open('depart_each.txt','w',encoding='UTF-8')
    stopwords = stopwordslist()
    for sentence in get_sentence():
        sentence_depart = jieba.cut(sentence.strip())        
        outstr = ""
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\n':
                    outstr = outstr+' '+word
        departfile.write(outstr+"\n")    
    departfile.close()
def w2v():
    sentences=word2vec.Text8Corpus(u'depart_each.txt')
    model = word2vec.Word2Vec(sentences, min_count=0, size=30,window=5, iter=100)
    model.save("./model/w2v_model")
def count_len():
    f = open('depart_each.txt','r',encoding='UTF-8')
    tot = 0
    count = 0
    while True:
        line=f.readline()
        if not line:
            break
        line = line[1:-1]
        linelist = line.split(" ")
        count += 1
        tot += len(linelist)
    f.close()
    print(tot,count,tot/count)
def sentence2vec():
    model = word2vec.Word2Vec.load('./model/w2v_model')
    f = open('depart_each.txt','r',encoding='UTF-8')
    vecfile = open('vector.txt','w',encoding='UTF-8')
    dup = []
    for i in range(30):
        dup.append(0.0)
    while True:
        line=f.readline()
        if not line:
            break
        if line == "\n":
            continue
        line = line[1:-1]
        linelist = line.split(" ")
        ans = []
        length = len(linelist)
        for i in range(50):
            if i<length:
                try:
                    temp = model[str(linelist[i])].tolist()
                except KeyError:
                    ans.append(dup)
                else:
                    ans.append(temp)
            else:
                ans.append(dup)
        vecfile.write(str(ans)+"\n")
    f.close()
    vecfile.close()
def test1():
    f = open('depart_each.txt','r',encoding='UTF-8')
    i=0
    while i<8:
        line=f.readline()
        if line =="\n":
            continue
        i+=1
        print(line)
        if not line:
            break
def test2():
    f = open('vector.txt','r',encoding='UTF-8')
    line = f.readline()
    try1 = eval(line)
    print(try1[0])
def get_similiar():
     model = word2vec.Word2Vec.load('./model/w2v_model')
     sim = model.similar_by_word(u'中学', topn=50)
     print(sim)
if __name__ ==  '__main__':
    #depart_for_each()
    #w2v()
    #test()
    #count_len()
    sentence2vec()
    #test2()
    #get_similiar()
