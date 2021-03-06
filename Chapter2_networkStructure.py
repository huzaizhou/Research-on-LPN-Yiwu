import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from numpy import mean,array,vstack

#创建网络
def creat(year):
    y = str(year)
    G = nx.DiGraph()
    path = 'data/{}.csv'.format(y)
    edge = pd.read_csv(path,engine='python')
    G.add_edges_from(array(edge))
    return G

#最大连通子图
def lcc(year):
    G = creat(year)
    H = nx.Graph(G)
    largest_cc = max(nx.connected_components(H), key=len)
    return G.subgraph(largest_cc)

#平均度
def md(year):
    G = creat(year)
    print('平均度：',mean(list(dict(G.degree()).values())))

#最大连通子图规模的平均最短路径
def aspl(year):
    largest_cc = lcc(year)
    a = len(largest_cc)
    b = nx.average_shortest_path_length(largest_cc)
    print('最大联通片规模：',a,'\n','平均最短路径：',b)

#随机图的最大连通子图和平均最短路径
def rg(year):
    G = creat(year)
    H = nx.Graph(G)
    n = len(H)
    p = nx.density(H)
    randomGraph = nx.fast_gnp_random_graph(n,p)
    largest_cc = max(nx.connected_components(randomGraph), key=len)
    a = len(largest_cc)
    b = nx.average_shortest_path_length(randomGraph.subgraph(largest_cc))
    print('随机图最大联通片规模：',a,'\n','随机图平均最短路径：',b)

#节点度值统计表
def degstat(year):
    G = creat(year)
    odg = dict(G.out_degree())
    idg = dict(G.in_degree())
    path2 = 'data/'+str(year)+'Node2.csv'
    nodeinfo = pd.read_csv(path2,index_col=2,engine='python',encoding="gbk")
    index = list(odg)
    odgvalue = list(odg.values())
    idgvalue = list(idg.values())
    arr = vstack((array(odgvalue),array(idgvalue),array(nodeinfo['company']),array(nodeinfo['type']))).T
    degreeTable = pd.DataFrame(arr,columns=['outdegree','indegree','company','type'],index=index)
    degreeTable.to_csv('data/'+str(year)+'degree.csv',encoding='utf_8_sig')

#集聚系数及其分布
def cluster(year):
    G = creat(year)
    clusterings = list(nx.clustering(G).values())
    df = pd.DataFrame(clusterings,columns=['集聚系数'])
    df.to_csv('data/'+str(year)+'cluster.csv',encoding='utf_8_sig')
    a = array(clusterings)
    count0 = sum(a == 0)
    count1 = sum(a == 1)
    count2 = sum(a >= 0.5) - count1
    count3 = len(G) - count0 - count1 - count2
    print('集聚系数分布：',count0, count1, count2, count3)

#平均集聚系数
def averageClustering(year):
    G = creat(year)
    return nx.average_clustering(G)
#介数中心性
def btwn(year):
    G = creat(year)
    betweenness = list(nx.betweenness_centrality(G,normalized=False).values())
    df = pd.DataFrame(betweenness,columns=['介数'])
    df.to_csv('data/'+str(year)+'betweenness.csv',encoding='utf_8_sig')
    a = array(betweenness)
    print('介数为0的点数：',sum(a == 0))

#调用函数，得到结果
i = 2009
md(i)
aspl(i)
rg(i)
degstat(i)
averageClustering(i)
cluster(i)
btwn(i)

#网络绘图
G = creat(i)
nx.draw_networkx(G,node_size=5,pos = nx.spring_layout(G))
plt.axis('off')
fig = plt.gcf()
fig.set_size_inches(30,30)
fig.savefig("a.png",dpi=400)
plt.show()
