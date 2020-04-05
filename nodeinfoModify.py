#将统计年鉴数据补充进节点信息表
import pandas as pd
data = pd.ExcelFile('data/统计年鉴数据.xlsx')

def modify(year):
    path1 = "data/"+year+"nodeinfo.csv"
    path2 = "data/"+year+"nodeinfo2.csv"
    info = pd.read_csv(path1,index_col=0,engine='python')
    yeardata = pd.read_excel(data,year,index_col=0)
    
    for i in info.index:
        if info['area'][i] in ['稠城','稠江','江东','北苑','福田']:
            info['area'][i] = '城区'
        if info['type'][i] == '企业':
            info['type'][i] = 'E'
        elif info['type'][i] == '非企业':
            info['type'][i] = 'P'
        for j in ['总人口','财政总收入','人均财政收入','地区编号']:
            try:
                info[j][i] = yeardata[j][info['area'][i]]
            except:
                info[j] = 0
                info[j][i] = yeardata[j][info['area'][i]]
        if info['code'][i] % 100 == 0:
            print(info['code'][i])
    info.to_csv(path2,encoding='utf_8_sig')

modify(2009)
