#计算直接消耗系数矩阵和产业相似度矩阵
import pandas as pds
import numpy as np

excel = pds.ExcelFile("data/2012全国投入产出表.xlsx")
sheet = pds.read_excel(excel,sheetname=1,index_col=0)

table = np.zeros([100,100])
for i in list(sheet.index)[:139]:
    for j in list(sheet.columns)[:139]:
        row = i // 1000
        col = j // 1000
        table[row,col] += sheet[j][i] 

table2 = np.zeros([100,100])
for i in range(100):
    for j in range(100):
        if sum(table[:,j]) != 0:
            table2[i,j] = table[i,j] / sum(table[:,j]) 

table3 = np.zeros([100,100])
for i in range(100):
    ai = table2[:,i]
    for j in range(100):
        aj = table[:,j]
        x,y,z = 0,0,0
        for k in range(100):
            x += ai[k]*aj[k]
            y += ai[k]**2
            z += aj[k]**2
        w = x/((y*z)**(0.5))
        table3[i,j] = w

np.save("data/dcc.npy",table2)
np.save("data/iip.npy",table3)