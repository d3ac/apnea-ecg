import pandas as pd
import os
import numpy as np

def solvedata(ans, data, flag):
    for i in range(len(data)):
        temp = data.iloc[i] # 横着读取数据
        temp = temp.dropna()
        tempans = [flag,]
        for j in temp:
            if type(j) != type('a'): # 乱码不要
                tempans.append(j)
        if len(tempans) >=11 and len(tempans)<=61:
            ans.append(tempans)
    return ans

def SolveData(name):
    ans = []
    try:
        data0 = pd.read_excel(name+'_0'+'.xlsx')
        ans = solvedata(ans, data0, 0)
    except:
        print(name+'_0'+'.xlsx'+' don\'t exist')
    try:
        data1 = pd.read_excel(name+'_1'+'.xlsx')
        ans = solvedata(ans, data1, 1)
    except:
        print(name+'_1'+'.xlsx'+' don\'t exist')
    ans = pd.DataFrame(ans)
    return ans

def del_last(name):
    Len = len(name)
    ans = ''
    for i in range(Len-2):
        ans += name[i]
    return ans

def step4(path='OSA RRi', SavePath='processed'):
    # path 是处理文件夹
    # processed 是输出文件夹
    # path = 'OSA RRi'
    # SavePath = 'processed'
    book = {}

    if not os.path.exists(SavePath):
        os.makedirs(SavePath)

    for filename in os.listdir(path):
        split_name = os.path.splitext(filename)
        split_name = del_last(split_name[0])
        if split_name in book:
            continue
        book[split_name] = True
        name = os.path.join(path, split_name)
        ans = SolveData(name)
        Name = os.path.join(SavePath, split_name+'.xlsx')
        ans.to_excel(Name, header=None, index=False) # 输出不要index 和 header
    print('step4 done')