#计算企业节点结构特征
import pandas as pd
import numpy as np

excel = pd.ExcelFile('data/网络结构统计.xlsx')

def statistic(year):
    sheet = pd.read_excel(excel,year-2008,index_col=0)
    o = sheet[sheet['type'] == 'E']['outdegree']
    i = sheet[sheet['type'] == 'E']['indegree']
    c = sheet[sheet['type'] == 'E']['集聚系数']
    b = sheet[sheet['type'] == 'E']['介数']
    
    print(year,np.mean(o),np.mean(i),np.mean(c),np.mean(b))
    print(sum(list(sheet['type'] == 'E') & (sheet['集聚系数'] == 0)))
    print(sheet[(sheet['type'] == 'E') & (sheet['介数'] >= 0.03)]['介数'])

for i in range(2009,2018):
    statistic(i)
