# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:40:57 2021

@author: 126243
"""

import requests
import json

def GetNameAndUid(query,region,ak):
    url = "http://api.map.baidu.com/place/v2/search?query="+query+"&page_size=20&scope=1&region="+region+"&output=json&ak="+ak
    # 请求参数，页码
    params = {'page_num':0}  
    # 请求数据
    request = requests.get(url,params=params)  
    # 数据的总条数
    total = json.loads(request.text)['total']  
    # 每个页面大小是20，计算总页码
    total_page_num = (total+19) // 20  
    names = []  
    uids = []
    for i in range(total_page_num):
        params['page_num'] = i
        request = requests.get(url,params=params)
        for item in json.loads(request.text)['results']:
            name = item['name']
            uid = item.get('uid', '')
            names.append(name)
            uids.append(uid)
    return names, uids