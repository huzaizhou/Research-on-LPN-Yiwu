#批发零售业度值统计
import pandas as pd
import numpy as np

degstat = pd.ExcelFile('data/网络结构统计.xlsx')
nodeinfo = pd.read_csv('data/AllNode.csv',index_col=1,engine='python',encoding='utf_8_sig')

dict = {}
for i in nodeinfo.index:
    if (nodeinfo['行业代码'][i] in[51,52]) and (nodeinfo['是否本地'][i] == '本地'):
        degreesum = 0
        for j in range(1,10):
            table = pd.read_excel(degstat,j,index_col=5)
            try:
                degree = table['outdegree'][i] + table['indegree'][i]
                degreesum += degree
            except:
                pass
        dict[i] = degreesum
    if nodeinfo['id'][i] % 100 == 0:
        print(nodeinfo['id'][i])

list = []
for key in dict:
    list.append([key,dict[key],dict[key]/18])
    
df = pd.DataFrame(list,columns=['company','degree','average'])
df.to_csv('data/批发零售业度值统计.csv',encoding='utf_8_sig')
