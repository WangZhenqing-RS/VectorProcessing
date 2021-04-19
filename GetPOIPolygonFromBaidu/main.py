# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:02:07 2021
ref: 
    https://blog.csdn.net/qq_34464926/article/details/103276834
    https://blog.csdn.net/w5688414/article/details/104632440
    https://blog.csdn.net/liyazhou0215/article/details/77161142
    https://www.cnblogs.com/qiernonstop/p/4005785.html
@author: 126243
"""

from WriteVectorFile import WriteVectorFile
from GetNameAndUid import GetNameAndUid
from GetBoundary import GetBoundary
from CoordinateConversion import bd09_to_wgs84_batch, bd09_metre_to_degree

query = "公园"
region = "北京"
ak = "kaVeiNCLULrnvcF3xDMLUOfiXkzrrKU7"

# 获取北京所有公园的 name 和 uid
names, uids = GetNameAndUid(query, region, ak)

for i in range(len(names)):
    try:
        # 通过uid获取边界坐标(百度米制)
        boundarys = GetBoundary(uids[i])
        # 百度米制坐标转百度经纬度坐标系
        boundarys_bd09 = bd09_metre_to_degree(boundarys, ak)
        # 百度经纬度坐标系转wgs84
        boundarys_wgs84 = bd09_to_wgs84_batch(boundarys_bd09)
        # 写shp需要的格式
        POLYGON = "POLYGON ((" + boundarys_wgs84 + "))"
        # 写shp
        WriteVectorFile("res//" + names[i] + ".shp",
                        names[i], 
                        POLYGON)
    except:
        pass