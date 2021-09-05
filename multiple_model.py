import multiprocessing
import math
import copy
import time
import AppSLDR

def Go(para):
    nodei = para[0]
    G = para[1]
    file = para[2]
    f = open(file+str(nodei),"w",encoding="utf-8")
    timef=open("node2/2timesyn_1/"+str(nodei),"w",encoding="utf-8")
    if (G.graph[nodei] == []):
        f.writelines("")
        timef.writelines("")
        print(nodei,"孤立节点！")
    else:
        a=time.perf_counter()
        result = AppSLDR.LocalCommunityDetectionForNodei(nodei, G,archive=[])
        b=time.perf_counter()
        timef.writelines(str(b-a))
        for j in range(0, len(result)):
            for nodes in result[j].nodes:
                f.writelines(str(nodes)+" ")
            f.writelines("\n")
        print(nodei,"成功！")
    f.close()
    timef.close()

if __name__ =="__main__":
    f1 = "dataset/syn_1-graph.txt"
    f2 = "dataset/syn_1-node.txt"
    G = AppSLDR.GetNetwork(f1, f2)
    savefile = "node/syn_1/"
    list1=[]
    for i in range(0,200):
        list1.append(1+20*i)
    nodelist = list1
    print(len(nodelist))
    plist = [[node,G,savefile] for node in nodelist]
    pool = multiprocessing.Pool(processes=3)  # 定义最大的进程数
    pool.map(Go,plist)  # p必须是一个可迭代变量。
    print("OK")
    pool.close()
    pool.join()