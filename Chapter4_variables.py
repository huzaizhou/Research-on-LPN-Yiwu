#搜寻模型——生成变量
import pandas as pds
import networkx as nx
import numpy as np
from industryconvert import convert

edge09 = pds.read_csv("data/2009.csv",engine="python")
node09 = pds.read_csv("data/2009nodeinfo2.csv",engine="python",index_col=0)
edge10 = pds.read_csv("data/2010.csv",engine="python")
node10 = pds.read_csv("data/2010nodeinfo2.csv",engine="python",index_col=2)

dcc = np.load("data/dcc.npy")
iip = np.load("data/iip.npy")

net = nx.DiGraph()#09年网络
for i in edge09.index:
    start = edge09['heads'][i]
    end = edge09['tails'][i]
    net.add_edge(start,end)

codeDict = {}#企业代码映射，10年企业代码：09年企业代码
degreeDict = {}#度值映射，10年企业代码：09年企业度值
for i in range(1,3043):
    name = node10["company"][i]
    if name in node09.index:
        c = node09["code"][name]
        codeDict[i] = c
        degreeDict[i] = net.degree(c)
    else:
        degreeDict[i] = 0

#10年网络邻接矩阵（因变量）
adjMatrix = np.zeros([3042,3042])
for i in range(10048):
    adjMatrix[edge10["tails"][i]-1,edge10["heads"][i]-1] = 1

#直接距离计算
gd = np.zeros([3042,3042])#地理距离矩阵
pd = np.zeros([3042,3042])#产品距离矩阵
nd = np.zeros([3042,3042])#网络距离矩阵

for supplier in range(1,3043):
    for buyer in range(supplier+1,3043):
        #地理距离计算
        if node10["area"][supplier] == node10["area"][buyer]:
            gd[supplier-1,buyer-1] = 1
        #产品距离计算
        supplierIndus = convert(node10["industry"][supplier])
        buyerIndus = convert(node10["industry"][buyer])
        pd[supplier-1,buyer-1] = dcc[supplierIndus,buyerIndus]#直接消耗系数
        
        #网络距离计算
        if (supplier in codeDict) and (buyer in codeDict):
            osc = codeDict[supplier]
            obc = codeDict[buyer]
            if nx.has_path(net,osc,obc):
                nd[supplier-1,buyer-1] = 1 / nx.shortest_path_length(net,osc,obc)        
    print(supplier)

#间接距离计算
igd = np.zeros([3042,3042])#间接地理距离矩阵
ipd = np.zeros([3042,3042])#间接产品距离矩阵

for supplier in range(1,3043):
    if supplier in codeDict:
        osc = codeDict[supplier]
        #卖方的生意伙伴
        partners = set()
        partners = set(net.successors(osc)) | set(net.predecessors(osc))
        for buyer in range(1,3043):
            if supplier != buyer:
                if buyer in codeDict:
                    obc = codeDict[buyer]
                    partners = partners - set([obc])
                l = len(partners)
                if l > 0:
                    #间接距离
                    sigd, sipd, sind= 0,0,0
                    for p in partners:
                        #间接地理距离
                        if node09["area"][node09.index[p-1]] == node10["area"][buyer]:
                            sigd += 1
                        #间接产品距离
                        buyerIndus = convert(node10["industry"][buyer])
                        partnerIndus = convert(node09["industry"][node09.index[p-1]])
                        sipd += iip[partnerIndus,buyerIndus]
                    
                    igd[supplier-1,buyer-1] = sigd / l
                    ipd[supplier-1,buyer-1] = sipd / l
    print(supplier)

#控制变量
eco = pds.ExcelFile("data/统计年鉴数据.xlsx")
eco09 = pds.read_excel(eco,sheetname=0,index_col=0)

#生成变量矩阵
variables = np.zeros([9250722,9])
dependent = np.zeros([9250722,1])

idx = 0
for supplier in range(1,3043):
    for buyer in range(1,3043):
        if supplier != buyer:
            dependent[idx,0] = adjMatrix[supplier-1,buyer-1]
            variables[idx,0] = degreeDict[supplier]
            variables[idx,1] = degreeDict[buyer]
            variables[idx,5] = igd[supplier-1,buyer-1]
            variables[idx,6] = ipd[supplier-1,buyer-1]
            variables[idx,8] = eco09["人均财政收入"][node10["area"][buyer]] / 1000
            if buyer > supplier:
                variables[idx,2] = gd[supplier-1,buyer-1]
                variables[idx,3] = pd[supplier-1,buyer-1]
                variables[idx,4] = nd[supplier-1,buyer-1]
            else:
                variables[idx,2] = gd[buyer-1,supplier-1]
                variables[idx,3] = pd[buyer-1,supplier-1]
                variables[idx,4] = nd[buyer-1,supplier-1]
            idx += 1
    if supplier % 100 == 0:
        print(supplier)

#保存变量
np.save("data/variables.npy",variables)
np.save("data/dependent.npy",dependent)