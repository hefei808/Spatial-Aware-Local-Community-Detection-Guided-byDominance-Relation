import time
import math
import copy
import gc

class solution:  #定义对象
    def __init__ (self, nodes,neighbor):
        self.nodes = nodes
        self.M = 0
        self.S = 0
        self.I = 0
        self.O = 0
        self.Ix = 0
        self.N = neighbor
        # self.dict =
    def __eq__(self, other):
        return self.nodes==other.nodes
    def __hash__(self):
        return hash(self.nodes)

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

def Isoutarchive(W,archive):   #判断解W是否在archive里
    for i in archive:
        if(W.nodes==i.nodes):
            return False
    return True

def Isinarchive(W,archive):   #判断解W是否在archive里
    for i in archive:
        if(W.nodes==i.nodes):
            return True
    return False

def computeDistance(p1,p2):    #计算两点之间距离
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4

def Findneighbors(G,W):    #寻找解W对应的节点集在网络中的邻居节点
    N = set()
    for i in W.nodes:
        N.update(set(G.graph[i]))
    return N - W.nodes


def compute_ms(node,G,W):  #根据增量计算节点集P的模块度M和空间内聚度S
    x = 0
    In = set(G.graph[node])&W.nodes
    Out = set(G.graph[node])-In
    I = W.I+len(In)
    O = W.O+len(Out)-len(In)
    if(O==0):
        return -1,-1,-1,-1,-1
    M = round(I/O,16)
    loc = G.nodes[node]
    for node_s in W.nodes:
        loc1 = G.nodes[node_s]
        d1 = math.sqrt(((loc1[0] - loc[0]) *(loc1[0] - loc[0])) + ((loc1[1] - loc[1]) *(loc1[1] - loc[1])))
        x += d1
    Ix = W.Ix+x
    S = round(-((2 * Ix) / (len(W.nodes) * (len(W.nodes) + 1))),16)
    return M, S, I, O, Ix

def Issame(A,B):
    if(len(A)!=len(B)):
        return False
    else:
        for i in range(0,len(A)):
            if(A[i].nodes!=B[i].nodes):
                return False
        return True

def updateN(G, W, node,P):
    Out = set(G.graph[node]) - W.nodes #ratio值需要更新的节点
    d=dict(P.N)
    # del P.N[search(P.N,(node,d[node]))]
    P.N.remove((node,d[node]))
    for i in Out: #更新P.N
        if(i in d):
            # index=search(P.N,(i,d[i]))
            # del P.N[index]
            P.N.remove((i, d[i]))
            # print("删除", i)
        O = set(G.graph[i]) - P.nodes
        I = set(G.graph[i]) - O
        if (len(O) != 0):
            w = (i, len(I) / len(O))
            insort(P.N,w)
        else:
            w = (i, len(P.nodes))
            insort(P.N, w)
    return P.N

def insort(a,x,lo=0,hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x[1] > a[mid][1]:
            hi = mid
        else:
            lo = mid + 1
    a.insert(lo, x)

def Findsons(G,archive): #寻找当前档案的的的衍生解
    box =set().union(archive)
    CC=set()
    for W in archive:        #temp = {W}
        for node in range(len(W.N)):
            #end = time.perf_counter()
            if(node>len(W.N)/3):
                break
            else:
                tempc=frozenset([W.N[node][0]])|W.nodes
                tempN = copy.copy(W.N)
                P = solution(tempc,tempN)
                #P.nodes=frozenset([W.N[node][0]])|W.nodes  # W和其邻居创建衍生解P
                ############################################
                if P in box:
                    # print("重复了！！！！！！！")
                    continue
                else:
                    P.M, P.S, P.I, P.O, P.Ix = compute_ms(W.N[node][0], G, W)
                    if (P.M == -1 ):#and Isoutarchive(P, CC),没看出来这个的用处
                        CC.add(P)
                        continue
                    P.N= updateN(G, W, W.N[node][0], P)
                    box.add(P)  # 加入衍生解P
    box = list(box)
    return box,CC

def Findpreto(sons):    #寻找解集中的非支配解
    preto = []   #存放非支配解
    sort = sorted(sons,key=lambda x: (x.M,x.S),reverse=True)  #按照解的M值大小关系，对解降序排序
    # print("\n^_^衍生解更新，当前档案长度为：", len(sort))
    # for j in sort:
    #     print(j.nodes, "    M=", j.M, "     S=",  j.S)
    preto.append(sort[0])   #取第一个解作为非支配解
    maxS = sort[0].S
    for each in sort:     #筛选出剩下解当中的非支配解存入preto中
        if(each.S>maxS):
            preto.append(each)
            maxS = each.S
        elif(each.S==maxS and each.M == preto[len(preto)-1].M and Isoutarchive(each,preto)):
            preto.append(each)
        else:
            continue
    # print("\n^_^preto解更新，当前档案长度为：", len(preto))
    # for j in preto:
    #     print(j.nodes, "    M=", '%.4f' % j.M, "     S=", '%.4f' % j.S)
    return preto

def LocalCommunityDetectionForNodei(nodei, G,archive):
    W = solution(frozenset([nodei]),[]) #初始化W为对象solution
    #W.nodes = frozenset([nodei])
    W.M,W.I,W.Ix,W.S=0,0,0,-100000
    W.O=len(G.graph[nodei])
    for i in G.graph[nodei]:
        O = set(G.graph[i]) - W.nodes
        I = set(G.graph[i]) - O
        if (len(O) != 0):
            w = (i, len(I) / len(O))
            W.N.append(w)
            # W.dict.update(w)
        else:
            w = (i, len(W.nodes))
            W.N.append(w)
            # W.dict.update(w)
    # W.N = sorted(W.N.items(), key=lambda x:x[1],reverse=True)
    W.N.sort(key=lambda x:x[1],reverse=True)
    archive.append(W)  #档案记录第一个解
    HND = set()
    CC=set()
    while(True):
         son,cc = Findsons(G, archive)  # 当前档案的衍生解
         CC.update(cc)
         print("\n^_^非支配解更新，当前档案长度为：", len(archive),";     存档长度：",len(HND))
         for j in range(0, len(archive)):
              print(archive[j].nodes, "    M=", '%.4f'%archive[j].M, "     S=", '%.4f'%archive[j].S,"     d=", '%.4f'%(archive[j].Ix))  # 输出当前档案中所有解
         # print("其衍生解有", len(son), "个，如下：")
         # for j in range(0, len(son)):
         #     if(son[j] in archive):
         #         print("*",son[j].nodes,"*")
         #     else:
         #         print(son[j].nodes, "    M=", '%.4f'%son[j].M, "     S=", '%.4f'%son[j].S)  # 输出当前所有候选解
         # fina = Findpreto(son)  # 衍生解中的非支配解
         ND = list(set(Findpreto(list(set(son)|HND))))  # 衍生解中的非支配解
         HND=set(ND)&HND
         C = set()
         for a in ND:
             for b in archive:
                 if (b.nodes == a.nodes):
                     C.add(a)
         HND.update(C)
         archive = list(set(ND) - HND)
         if (len(archive)==0):  # 终止循环条件：更新前的档案和更新后的档案一样；否则，更新档案，继续循环
              break
    # archive = list(set(archive)|CC)
    # print(CC)
    archive=Findpreto(list(set(archive)|HND))
    # archive=ND
    print("最终档案长度为", len(archive))
    for j in range(0, len(archive)):
        print(archive[j].nodes, "    M=", '%.4f'%archive[j].M, "     S=", '%.8f'%archive[j].S,"     d=", '%.4f'%(archive[j].Ix))  # 输出当前档案中所有解
    return archive

if __name__ =="__main__":
    start = time.perf_counter()
    f1 = "dataset/kite-graph.txt"
    f2 = "dataset/kite-node.txt"
    G = GetNetwork(f1, f2)
    archive = []  # 档案：存放解
    nodei =3
    print(G.graph[nodei])
    print(len(G.graph[nodei]))
    if (G.graph[nodei] == []):
        print('该点为孤立节点，无社区！！')
    else:
        result = LocalCommunityDetectionForNodei(nodei, G, archive)  # 为节点nodei找社区
    end = time.perf_counter()  # 记录执行时间
    print(end - start, "秒")
