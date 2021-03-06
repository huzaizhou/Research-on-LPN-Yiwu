#将2009年对公交易原始数据转换为节点列表
import pandas as pd

info = pd.read_csv("data/AllNode.csv",index_col=1,encoding='gb18030')

def convert(year):
    path1 = "data/OriginalData"+year+".csv"
    path2 = "data/"+year+".csv"
    path3 = "data/"+year+"Node.csv"
    detail = pd.read_csv(path1)
    
    edgeList1 = []
    edgeList2 = []
    for i in detail.index:
        start = detail['户名'][i]
        end = detail['对方户名'][i]
        if (start in info.index) and (end in info.index):
            if (info['是否本地'][start] == '本地') and (info['是否本地'][end] == '本地'):
                u = info['单位编号'][start]
                v = info['单位编号'][end]
                if (u != v) and ([u,v] not in edgeList1):
                    edgeList1.append([u,v])
                    edgeList2.append([start,end])
    
    allcompany = []
    for m in edgeList2:
        for n in m:
            if n not in allcompany:
                allcompany.append(n)
    
    indexdict = {}
    for m in allcompany:
        id_before = info['单位编号'][m]
        id_new = allcompany.index(m)+1
        l2 = [id_before,id_new]
        indexdict[m] = l2
    
    edgeList3 = []
    for a in edgeList2:
        edgeList3.append([indexdict[a[0]][1],indexdict[a[1]][1]])
    
    edge_csv = open(path2,"w")
    edge_csv.write("heads,tails\n")
    for i in edgeList3:
        edge_csv.write(str(i[0])+","+str(i[1])+"\n")
    edge_csv.close()
    
    nodeinfo = open(path3,"w")
    nodeinfo.write("company,adjusted,code,industry,type,area\n")
    for k in allcompany:
        adjusted = info['调整后户名'][k]
        code = indexdict[k][1]
        industry = info['行业代码'][k]
        types = info['企业/非企业'][k]
        area = info['街道/镇'][k]
        nodeinfo.write(str(k)+','+adjusted+','+str(code)+','+str(industry)+','+types+','+area+"\n")
    nodeinfo.close()

convert("2009")





