import os
import sys
class solution:  #定义对象
    def __init__ (self):
        self.nodes = []
        self.M = 0
        self.S = -10000
class Graph():
    def __init__(self):
        self.nodes = {}
        self.graph = {}
def GetNetwork(f1,f2):
    G = Graph()
    with open(f2) as f:
        lines = f.readlines()
        for line in lines:
            curLine = line.strip().split(" ")
            G.nodes.update({int(curLine[0]):[float(curLine[1]),float(curLine[2])]})
    with open(f1) as ef:
        elines = ef.readlines()
        for line in elines:
            cureline = line.strip().split(" ")
            if(len(cureline)>1):
                temp = []
                for i in range(1,len(cureline)):
                    temp.append(int(cureline[i]))
                G.graph.update({int(cureline[0]):temp})
            else:
                G.graph.update({int(cureline[0]):[]})
    return G
def computeMS(G,W):
    I = 0
    O = 0
    Ix = 0
    Ox = 0
    num = 0
    numo = 0
    S = -1000000
    for node in W:
        O += len(set(G.graph[node]) - W)
        I += len(set(G.graph[node]) & W)
    I = I / 2
    if (O != 0):
        M = I / O
    else:
        print(W)
        sys.exit(0)

    for i in W:
        p1 = G.nodes[i]
        for node_i in G.graph[i]:
            if node_i in W:
                p2 = G.nodes[node_i]
                d = (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5
                Ix = Ix + d
                num += 1
            else:
                p2 = G.nodes[node_i]
                d = (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5
                Ox = Ox + d
                numo += 1
    if Ox != 0 and num != 0 and Ix != 0 and numo!=0:
        S = -(Ix / num) / (Ox / numo)
    return M, S

def Findpreto(sons):    #寻找解集中的非支配解
    preto = []   #存放非支配解
    # a=[]
    sort = sorted(sons,key=lambda x: (x.M,x.S),reverse=True)  #按照解的M值大小关系，对解降序排序
    preto.append(sort[0])   #取第一个解作为非支配解
    maxS = sort[0].S
    for each in sort:     #筛选出剩下解当中的非支配解存入preto中
        if(each.S>maxS):
            preto.append(each)
            maxS = each.S
        elif(each.S==maxS and each.M == preto[len(preto)-1].M):
            preto.append(each)
        else:
            continue
    # for i in range(int(len(preto)*1/3),int(len(preto)*2/3)+1):
    #     a.append(preto[i])
    return preto

if __name__=="__main__":
    f1 = "dataset/syn_1-graph.txt"
    f2 = "dataset/syn_1-node.txt"
    G = GetNetwork(f1, f2)
    dict = {}
    for root, dirs, files in os.walk("results/base/2bkite/"):
        for file in files:
            print(file)
            f = open("results/base/2bkite/" + file, "r")
            lines = f.readlines()
            print(len(lines))
            if(len(lines)==0):
                f.close()
                dict.update({int(file): "null"})
                continue
            else:
                line=lines[int(len(lines)/2)]
                metric = line.strip().split(" ")
                a = solution()
                for j in metric:  # 将字符串类型转为整型
                    a.nodes.append(int(j))

                #     if(a.M*1/(-a.S)/(a.M-1/a.S)>b.M*1/(-b.S)/(b.M-1/b.S)):
                #     # if (a.M > b.M):
                #     # if(a.S>b.S):
                #         b=a
                #     else:
                #         continue
                # print(b.nodes)
                # dict.update({int(file): b.nodes})
                dict.update({int(file): a.nodes})
            f.close()
    fw = open("dict/2bkite.txt", "w")
    fw.write(str(dict))
    fw.close()
    ###读文本文件中的字典
    # fr = open("dict/kitedict.txt", 'r+')
    # dic = eval(fr.read())  # 读取的str转换为字典
    # fr.close()
    print(len(dict),dict)