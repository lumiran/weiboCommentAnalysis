
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:23:46 2019

@author: Lumi
"""

import requests
import re
import time
import pandas as pd
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

# 把id替换成你想爬的地址id
myCookies = {'Cookie':'ALF=1558415943; _T_WM=3fc719221000d1560fdfe7b3cc168a84; WEIBOCN_FROM=1110006030; SCF=As-MR5f1DBTkTnFqOJmhDp8PXyHsKx_GQarBCRmU6tSIbdcmr_jdIFf5ah9YIJZFCwVQh4ytD3eb4wo2zHKi20Q.; SUB=_2A25xuf2kDeRhGeNH4lQQ9C3MyTSIHXVTRYPsrDV6PUJbktBeLVn8kW1NSklrTU3ZiEhKmwl6FtxFxRSHS_jBCgG6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF5nX9uBup1wwxihe2z03Qz5JpX5K-hUgL.Fo-41KqpShe7eon2dJLoIf2LxKMLB.zLB.qLxKML1h2LB-qLxKBLBonL12BLxK-L1h2L1-eLxK.LBKeL1--LxK.LBKeL1--LxK.LBKeL1--LxKnLBo-LBoMLxKqL1-BLBK-t; SUHB=0IIV7YPA4m94MO; SSOLoginState=1555926516; MLOGIN=1; XSRF-TOKEN=5623e0; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174'}
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

comments, ids, names = [], [], []
tags = re.compile('</?\w+[^>]*>')
def get_comment(url):
    html = requests.get(url, headers=head,cookies = myCookies)
    j = html.json()
    comment_data = j['data']['data']
    for data in comment_data:
        if len(data) == 7:
            comment = tags.sub('', data['text'])
            weibo_id = data['id']
            name = data['user']['screen_name']
            print('昵称:{},评论:{}'.format(name,comment))
            comments.append(comment)
            ids.append(weibo_id)
            names.append(name)
        
def getPageNum(url):
    '''
    找到这个评论总共多少条，要爬多少页。
    返回页码数。
    '''
    url_temp = url.format(str(1))
    html = requests.get(url_temp, headers=head,cookies = myCookies)
    info = html.json()

    print(info['msg'])
    print('Total comment number:',info['data']['total_number'])
    return info['data']['max']

url = 'https://m.weibo.cn/api/comments/show?id=4363275507008634&page={}'

for i in range(1, getPageNum(url)+1):
    get_comment(url.format(str(i)))
    time.sleep(50*random.random()) # 防止爬得太快被封

# 这里我用pandas写入csv文件，需要设置encoding，不然会出现乱码
df = pd.DataFrame({'ID': ids, '评论': comments})
df = df.drop_duplicates()
df.to_csv('观察者网.csv', index=False, encoding='gb18030')

len(comments)
kgKey = '卡攻'
tgKey = ['婷攻','停']
wenKey = '文'
xsKey = '学生'
hgKey = ['互','护工']

kgSum,tgSum,hgSum = [],[],[]
kgwk,tgwk,hgwk = [],[],[]
kgxs,tgxs,hgxs = [],[],[]
for i in range(len(comments)):
    
    kgSum.append(kgKey in comments[i])
    kgwk.append((wenKey in comments[i]) and (kgKey in comments[i]))
    kgxs.append((xsKey in comments[i]) and (kgKey in comments[i]))
    
    tgSum.append((tgKey[0] in comments[i]) or (tgKey[1] in comments[i]))
    tgwk.append(((tgKey[0] in comments[i]) or (tgKey[1] in comments[i])) and (wenKey[0] in comments[i]))
    tgxs.append(((tgKey[0] in comments[i]) or (tgKey[1] in comments[i])) and (xsKey in comments[i]))
    
    if tgSum[i] or kgSum[i]:
        hgSum.append(False)
    else:
        hgSum.append((hgKey[0] in comments[i]) or (hgKey[1] in comments[i]))
        hgwk.append(hgSum[i] and (wenKey[0] in comments[i]))
        hgxs.append(hgSum[i] and (xsKey[0] in comments[i]))
    
plt.bar(range(3),[sum(kgSum),sum(tgSum),sum(hgSum)])   
plt.bar(range(3),[sum(kgwk),sum(tgwk),sum(hgwk)]) 
plt.show() 

plt.bar(range(3),[sum(kgSum),sum(tgSum),sum(hgSum)],label = 'Employee')   
plt.bar(range(3),[sum(kgxs),sum(tgxs),sum(hgxs)],label = 'Student') 
plt.legend()
plt.show() 











print('    |    卡攻      |     婷攻     |     互攻     |')
wkSum = sum(kgwk)+sum(tgwk)+sum(hgwk)
AllSum = sum(kgSum)+sum(tgSum)+sum(hgSum)
xsSum = sum(kgxs)+sum(tgxs)+sum(hgxs)
print('文科| {:12} | {:12} | {:12} |{:5}({:4.1f}%)|'.format(sum(kgwk),sum(tgwk),sum(hgwk),wkSum,wkSum/AllSum*100))
print('非文| {:12} | {:12} | {:12} |{:5}({:4.1f}%)|'.format(sum(kgSum)-sum(kgwk),sum(tgSum)-sum(tgwk),sum(hgSum)-sum(hgwk),AllSum-wkSum,(AllSum-wkSum)/AllSum*100))
print('_______________________________________________')
print('学生| {:12} | {:12} | {:12} |{:5}({:4.1f}%)|'.format(sum(kgxs),sum(tgxs),sum(hgxs),xsSum,xsSum/AllSum*100))
print('工作| {:12} | {:12} | {:12} |{:5}({:4.1f}%)|'.format(sum(kgSum)-sum(kgxs),sum(tgSum)-sum(tgxs),sum(hgSum)-sum(hgxs),AllSum-xsSum,(AllSum-xsSum)/AllSum*100))

print('总数| {:5}({:4.1f}%) | {:5}({:4.1f}%) | {:5}({:4.1f}%)| {:12}|'.format(sum(kgSum),sum(kgSum)/AllSum*100,sum(tgSum),sum(tgSum)/AllSum*100,sum(hgSum),sum(hgSum)/AllSum*100,AllSum))




print('评论抽奖：',names[round(random.random()*AllSum)])



for i in range(len(comments)):
    if tgxs[i]:
        print(comments[i])
    
    
    if not tgSum[i] and not hgSum[i] and not kgSum[i]:
        print(comments[i])
        print(names[i])
        
        



