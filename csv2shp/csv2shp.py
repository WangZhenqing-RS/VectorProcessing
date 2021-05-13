# -*- coding: utf-8 -*-
"""
Created on Wed May 12 11:08:14 2021

ref:
    https://www.it610.com/article/1282732411003617280.htm
@author: 126243
"""

import osgeo.ogr as ogr
import osgeo.osr as osr
from osgeo import gdal
import pandas as pd

def csv2shp(csv_path, shp_path, layerName):
    # 解决中文字符问题
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO") 
    gdal.SetConfigOption("SHAPE_ENCODING","") 
    
    # 设置空间参考,4326代表WGS84
    SpatialReference  = osr.SpatialReference()
    SpatialReference .ImportFromEPSG(4326)
    
    # 新建DataSource,Layer
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(shp_path)
    layer = data_source.CreateLayer(layerName, SpatialReference, ogr.wkbPoint)
    
    # 读取csv文件
    csv_df = pd.read_csv(csv_path)
    # csv所有列名,即shp的字段名
    filed_names = list(csv_df)
    
    # layer添加上述字段
    for filed_name in filed_names:
        print(str(csv_df[filed_name].dtypes))
        if("int" in str(csv_df[filed_name].dtypes)):
            field = ogr.FieldDefn(filed_name, ogr.OFTInteger)
            field.SetWidth(10)
        elif("float" in str(csv_df[filed_name].dtypes)):
            field = ogr.FieldDefn(filed_name, ogr.OFTReal)
            field.SetWidth(10)
            field.SetPrecision(5)
        else:
            field = ogr.FieldDefn(filed_name, ogr.OFTString)
            field.SetWidth(10)
        layer.CreateField(field)

    # 从layer中读取相应的feature类型，并创建feature
    featureDefn = layer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    
    # 设定几何形状
    point = ogr.Geometry(ogr.wkbPoint)
    
    # 循环输入字段属性值
    for i in range(len(csv_df)):
        for j in range(len(filed_names)):
            if("int" in str(csv_df[filed_names[j]].dtypes)):
                feature.SetField(filed_names[j], int(csv_df.iloc[i, j]))
            elif("float" in str(csv_df[filed_names[j]].dtypes)):
                feature.SetField(filed_names[j], float(csv_df.iloc[i, j]))
            else:
                feature.SetField(filed_names[j], str(csv_df.iloc[i, j]))

        # 设置几何信息部分
        # 利用经纬度创建点,X为经度,Y为纬度(我的数据第5列是经度,第6列是纬度)
        point.AddPoint(float(csv_df.iloc[i, 5]), float(csv_df.iloc[i, 6]))
        feature.SetGeometry(point)
        
        # 将feature写入layer
        layer.CreateFeature(feature)
    
    # 从内存中清除 ds，将数据写入磁盘中
    data_source.Destroy()
    
csv_path = r"typhoonrisk_35_data_2013_25_1323_Fitow.csv"
shp_path = r"typhoonrisk_35_data_2013_25_1323_Fitow.shp"
csv2shp(csv_path, shp_path, "Fitow")