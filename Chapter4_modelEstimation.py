#搜寻模型——不同模型的设定和估计
import numpy as np
import statsmodels.api as sm
import pandas as pds

variables = np.load("data/variables.npy")
dependent = np.load("data/dependent.npy")

var1 = pds.DataFrame(variables,columns=['supplier_degree','buyer_degree','geo_dist','prod_dist','net_dist','i_geo_dist','i_prod_dist','i_net_dist','control'])
var1.insert(0,'intercept',1.0)

model1 = sm.Probit(dependent,var1[var1.columns[[0,1,2,9]]])
result1 = model1.fit()
print(result1.summary())

model2 = sm.Probit(dependent,var1[var1.columns[[0,1,2,3,4,5,9]]])
result2 = model2.fit()
print(result2.summary())

model3 = sm.Probit(dependent,var1[var1.columns[[0,1,2,3,4,5,6,7,9]]])
result3 = model3.fit()
print(result3.summary())

result1.save("data/result1")
result2.save("data/result2")
result3.save("data/result3")

#加载模型结果，查看边际效应和p值
from statsmodels.discrete.discrete_model import ProbitResults

result1 = ProbitResults.load("data/result1")
margeff = result1.get_margeff()

print(result1.summary())
print(result1.pvalues)
print(margeff.summary())
print(margeff.margeff)