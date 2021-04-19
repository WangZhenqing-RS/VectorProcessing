# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 20:13:23 2021

@author: 126243
"""
import requests
from requests.adapters import HTTPAdapter 
import json

# 根据UID获取边界数据
def GetBoundary(uid):
    
    bmap_boundary_url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&uid=' + uid + '&c=340&ext_ver=new&tn=B_NORMAL_MAP&nn=0&auth=fw9wVDQUyKS7%3DQ5eWeb5A21KZOG0NadNuxHNBxBBLBHtxjhNwzWWvy1uVt1GgvPUDZYOYIZuEt2gz4yYxGccZcuVtPWv3GuxNt%3DkVJ0IUvhgMZSguxzBEHLNRTVtlEeLZNz1%40Db17dDFC8zv7u%40ZPuxtfvSulnDjnCENTHEHH%40NXBvzXX3M%40J2mmiJ4Y&ie=utf-8&l=19&b=(12679382.095,2565580.38;12679884.095,2565907.38)&t=1573133634785'

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(url=bmap_boundary_url, timeout=5, headers={"Connection": "close"})
    data = data.text
    data = json.loads(data)
    content = data['content']
    if not 'geo' in content:
        return None
    geo = content['geo']
    i = 0
    strsss = ''
    for jj in str(geo).split('|')[2].split('-')[1].split(','):
        jj = str(jj).strip(';')
        if i % 2 == 0:
            strsss = strsss + str(jj) + ','
        else:
            strsss = strsss + str(jj) + ';'
        i = i + 1
    return strsss.strip(";")