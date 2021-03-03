#集聚系数分布图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import mpl,text

simsun = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc', size=12)
roman = FontProperties(fname=r'C:\Windows\Fonts\times.ttf', size=12)
mpl.rcParams['font.sans-serif'] = ['SimSun']
fontcn = {'family': 'SimSun','size': 10}
fonten = {'family':'Times New Roman','size': 10}

excel = pd.ExcelFile('data/网络结构统计.xlsx')

def btw(year):
    sheet = pd.read_excel(excel,year-2008)
    btws = sheet[sheet['type'] == 'E']['介数']
    return btws

fig,axes = plt.subplots(3,3,figsize=(18,10))
list = [[2009,2010,2011],[2012,2013,2014],[2015,2016,2017]]
for i in range(3):
    for j in range(3):
        year = list[i][j]
        btws = btw(year)
        ax = axes[i,j]
        bins = np.arange(0.0,0.0305,0.0005)
        ax.hist(btws,bins=bins,edgecolor='black')
        ax.set_xticks([0.000,0.005,0.010,0.015,0.020,0.025,0.030])
        ax.text(0.010,0.13,'（',fontproperties=simsun)
        ax.text(0.0113,0.13,str(year-2008),fontproperties=roman)
        ax.text(0.012,0.13,'）',fontproperties=simsun)
        ax.text(0.0134,0.13,str(year),fontproperties=roman)
        ax.text(0.016,0.13,'年',fontproperties=simsun)
        ax.set_yscale('log')
        plt.tick_params(labelsize=30)
plt.subplots_adjust(hspace=0.3)
plt.show()
