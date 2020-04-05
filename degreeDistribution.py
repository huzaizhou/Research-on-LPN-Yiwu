#绘制度分布散点直方图
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
from matplotlib.font_manager import FontProperties

list = [[2009,2010,2011],[2012,2013,2014],[2015,2016,2017]]
excel = pd.ExcelFile('data\网络结构统计.xlsx')

def deg(year):
    sheet = pd.read_excel(excel,year-2008,index_col=0)
    t = 'E' 
    o = sheet[(sheet['type'] == t) & (sheet['outdegree'] + sheet['indegree'] <= 200)]['outdegree']
    i = sheet[(sheet['type'] == t) & (sheet['outdegree'] + sheet['indegree'] <= 200)]['indegree']
    return o,i

def scatterHist(x,y,year,axScatter):
    axScatter.scatter(x, y)
    axScatter.set_aspect(1.)
    
    plt.xticks([0,20,40,60,80,100],fontsize='large')
    plt.yticks([0,20,40,60,80,100],fontsize='large')
    
    axScatter.set_xlabel('outdegree',fontsize='large',fontproperties=roman)
    axScatter.set_ylabel('indegree',fontsize='large',fontproperties=roman)
    
    divider = make_axes_locatable(axScatter)
    axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
    axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)
    
    axHistx.xaxis.set_tick_params(labelbottom=False)
    axHisty.yaxis.set_tick_params(labelleft=False)
    b = 102
    bins = np.arange(0, b, 2)
    axHistx.hist(x, bins=bins, edgecolor='black')
    axHistx.set_yscale('log')
    axHisty.hist(y, bins=bins, orientation='horizontal', edgecolor='black')
    axHisty.set_xscale('log')
    
    axHisty.set_title('({})  \n{}  '.format(str(year-2008),year), pad=40, fontproperties=roman)

simsun = FontProperties(fname='C:/Windows/Fonts/simsun.ttc',size=14)
roman = FontProperties(fname=r'C:\Windows\Fonts\times.ttf', size=16)

fig = plt.figure(figsize=(18,18))
for m in range(3):
    for n in range(3):
        year = list[m][n]
        x,y = deg(year)
        ax = fig.add_subplot(3,3,3*m+n+1)
        scatterHist(x,y,year,ax)
fig.savefig('度分布.png',dpi=400)
plt.show()
        