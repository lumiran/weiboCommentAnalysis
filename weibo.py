
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

# Please First turn to 'm.weibo.cn'
# Check Developer Tools to Find Your Cookies and Your User-Agent
myCookies = {'Cookie':YourCookies}
head = {'User-Agent': YourAgent}

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

# target url have the form of 'https://m.weibo.cn/api/comments/show?id=4363275507008634&page={}'
url = target_url

for i in range(1, getPageNum(url)+1):
    get_comment(url.format(str(i)))
    time.sleep(10*random.random()) # 防止爬得太快被封

# Use pandas to write a .csv file
df = pd.DataFrame({'ID': ids, '评论': comments})
df = df.drop_duplicates()
df.to_csv('Data.csv', index=False, encoding='gb18030')


        
        



