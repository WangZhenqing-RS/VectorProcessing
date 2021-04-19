# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:58:47 2021

@author: 126243
"""

try:
    from osgeo import gdal, ogr, osr
except ImportError:
    import gdal, ogr, osr

def WriteVectorFile(shp_path, name, polygon):
    
    # 解决中文路径
    gdal.SetConfigOption('GDAL_FILENAME_IS_UTF8', 'YES') 
    # 解决 SHAPE 文件的属性值
    gdal.SetConfigOption('SHAPE_ENCODING', 'GBK') 

    # 注册所有的驱动
    ogr.RegisterAll()

    # 创建ESRI的shp文件
    strDriverName = "ESRI Shapefile"
    oDriver =ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("驱动不可用!",)
        return

    # 创建数据源
    oDS = oDriver.CreateDataSource(shp_path)
    if oDS == None:
        print("创建文件失败!")
        return
    
    # 创建空间参考系，WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    
    # 创建图层，创建一个多边形图层
    papszLCO = []
    oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
        return

    # 下面创建属性表
    # 先创建一个叫FieldID的整型属性
    oFieldID =ogr.FieldDefn("FieldID", ogr.OFTInteger)
    oLayer.CreateField(oFieldID, 1)

    # 再创建一个叫FieldName的字符型属性，字符长度为100
    oFieldName =ogr.FieldDefn("FieldName", ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName, 1)

    oDefn = oLayer.GetLayerDefn()

    # 创建要素
    oFeatureTriangle = ogr.Feature(oDefn)
    oFeatureTriangle.SetField(0, 0)
    oFeatureTriangle.SetField(1, name)
#    geomTriangle =ogr.CreateGeometryFromWkt("POLYGON ((0 0,20 0,10 15,0 0))")
    geomTriangle =ogr.CreateGeometryFromWkt(polygon)
    oFeatureTriangle.SetGeometry(geomTriangle)
    oLayer.CreateFeature(oFeatureTriangle)

    oDS.Destroy()
    print("数据集创建完成!")