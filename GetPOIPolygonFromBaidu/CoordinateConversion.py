# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 20:10:01 2021

@author: 126243
"""
import requests
from requests.adapters import HTTPAdapter 
import json
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323

# 从百度米制坐标系转换为百度经纬度坐标系
def bd09_metre_to_degree(coordinates, ak):
    
    req_url = 'http://api.map.baidu.com/geoconv/v1/?coords='+coordinates+'&from=6&to=5&ak=' + ak

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(req_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
    data = data.text
    data = json.loads(data)
    coords = ''
    if data['status'] == 0:
        result = data['result']
        if len(result) > 0:
            for res in result:
                lng = res['x']
                lat = res['y']
                coords = coords + ";" + str(lng) + "," + str(lat)
    return coords.strip(";")
 
def out_of_china(lng, lat):
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)
 
def _lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
 
 
def _lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
 
def bd09_to_gcj02(bd_lon, bd_lat):
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]
 
def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _lat(lng - 105.0, lat - 35.0)
    dlng = _lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]
 
def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)

def bd09_to_wgs84_batch(bd_lon_bd_lats):
    bd_lon_bd_lats_list = bd_lon_bd_lats.split(";")
    result = ""
    for bd_lon_bd_lat in bd_lon_bd_lats_list:
        lon_lat = bd_lon_bd_lat.split(",")
        lon = float(lon_lat[0])
        lat = float(lon_lat[1])
        lon_lat_wgs84 = bd09_to_wgs84(lon, lat)
        lon_wgs84 = lon_lat_wgs84[0]
        lat_wgs84 = lon_lat_wgs84[1]
        result += str(lon_wgs84) + " " + str(lat_wgs84) + ","
    result = result[:-1]
    return result