# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:30:59 2022

@author: DELL
"""

from osgeo import ogr, gdal


def get_tif_meta(tif_path):
    dataset = gdal.Open(tif_path)
    # 栅格矩阵的列数
    width = dataset.RasterXSize 
    # 栅格矩阵的行数
    height = dataset.RasterYSize 
    # 获取仿射矩阵信息
    geotrans = dataset.GetGeoTransform()
    # 获取投影信息
    proj = dataset.GetProjection()
    return width, height, geotrans, proj

def shp2tif(shp_path, refer_tif_path, target_tif_path, attribute_field="class", nodata_value=0):

    width, height, geotrans, proj = get_tif_meta(refer_tif_path)
    # 读取shp文件
    shp_file = ogr.Open(shp_path)
    # 获取图层文件对象
    shp_layer = shp_file.GetLayer()
    # 创建栅格
    target_ds = gdal.GetDriverByName('GTiff').Create(
        utf8_path = target_tif_path,    # 栅格地址
        xsize = width,                  # 栅格宽
        ysize = height,                 # 栅格高
        bands = 1,                      # 栅格波段数
        eType = gdal.GDT_Byte           # 栅格数据类型
        )
    # 将参考栅格的仿射变换信息设置为结果栅格仿射变换信息
    target_ds.SetGeoTransform(geotrans)
    # 设置投影坐标信息
    target_ds.SetProjection(proj)
    band = target_ds.GetRasterBand(1)
    # 设置背景nodata数值
    band.SetNoDataValue(nodata_value)
    band.FlushCache()
    
    # 栅格化函数
    gdal.RasterizeLayer(
        dataset = target_ds,                        # 输出的栅格数据集
        bands = [1],                                # 输出波段
        layer = shp_layer,                          # 输入待转换的矢量图层
        options=[f"ATTRIBUTE={attribute_field}"]    # 指定字段值为栅格值
        )
    
    del target_ds


shp_path = "demo.shp"
refer_tif_path = "refer.tif"
target_tif_path = "target.tif"
attribute_field = "class"
nodata_value = 0
shp2tif(shp_path, refer_tif_path, target_tif_path, attribute_field, nodata_value)
