#模型精确度——AUC
import numpy as np

def auc(model):
    data1 = np.loadtxt('data/关系出现概率预测值/2009/p1m'+str(model)+'_2009.txt')
    data2 = np.loadtxt('data/关系出现概率预测值/2009/p2m'+str(model)+'_2009.txt')
    
    #AUC值计算
    score = 0
    idx = 0
    for i in data1:
        idx += 1
        h = np.random.choice(data2,size=100000)
        for j in h:
            if i > j:
                score += 1
            if i == j:
                score += 0.5
        print(idx)
    print(score/806100000)
    
#选择模型
auc(1)