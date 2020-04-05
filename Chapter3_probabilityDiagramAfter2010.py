#绘制模型2预测的2010年-2017nian 关系出现概率的分布图
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='C:/Windows/Fonts/simsun.ttc',size=14)

fig,axes = plt.subplots(4,2,figsize=(10,10),dpi=100)
year = [[2010,2011],[2012,2013],[2014,2015],[2016,2017]]
bins = np.arange(0,1.02,0.02)
for i in range(4):
    for j in range(2):
        y = year[i][j]
        data = np.loadtxt('data/p1m2_'+str(y)+'.txt')
        ax = axes[i,j]
        ax.hist(data,bins=bins,edgecolor='black')
        ax.set_yticks([1000,2000,3000,4000,5000])
        ax.set_title('（{}）{}年 '.format(y-2009,y),pad=-136,fontproperties=font)
        ax.text(0,4000,'平均值：{:.3f}'.format(data.mean()),fontproperties=font)
        ax.text(0,3000,'未准确预测：{}（{:.1%}）'.format(sum(data<0.1),sum(data<0.1)/sum(data<1)),fontproperties=font)
        ax.annotate('',xy=(0.05,800),xytext=(0.18,2700),arrowprops=dict(facecolor='black',width=1,headwidth=7,headlength=10))
        plt.subplots_adjust(hspace=0.4)
        #print(sum(data<0.1)/sum(data<1),data.mean())
