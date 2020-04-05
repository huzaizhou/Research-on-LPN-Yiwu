#绘制模型1和模型2预测的2009年关系出现概率的分布图
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='C:/Windows/Fonts/simsun.ttc',size=14)

#模型1预测结果
data1 = np.loadtxt('data/p1m1_2009.txt')
data2 = np.loadtxt('data/p2m1_2009.txt')

fig,axes = plt.subplots(1,2,figsize=(10,3),dpi=200)
bins1 = np.arange(0,0.0082,0.0002)
ax1 = axes[0]
ax2 = axes[1]
ax1.hist(data1,bins=bins1,edgecolor='black')
#ax1.set_yscale('log')
ax2.hist(data2,bins=bins1,edgecolor='black')
#ax2.set_yscale('log')
ax1.set_title('（1）已有关系出现概率分布 ',pad=-200,fontproperties=font)
ax2.set_title('（2）潜在关系出现概率分布 ',pad=-200,fontproperties=font)

#模型2预测结果
data1 = np.loadtxt('data/p1m2_2009.txt')
data2 = np.loadtxt('data/p2m2_2009.txt')

fig,axes = plt.subplots(1,2,figsize=(10,3),dpi=200)
bins2 = np.arange(0,1.02,0.02)
ax1 = axes[0]
ax2 = axes[1]
ax1.hist(data1,bins=bins2,edgecolor='black')
#ax1.set_yscale('log')
ax2.hist(data2,bins=bins2,edgecolor='black')
ax2.set_yscale('log')
ax1.set_title('（1）已有关系出现概率分布 ',pad=-200,fontproperties=font)
ax2.set_title('（2）潜在关系出现概率分布 ',pad=-200,fontproperties=font)
