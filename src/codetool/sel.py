# -*- coding: UTF-8 -*-
# 针对图层选择的操作

import arcpy
import arcpy.sa

def __get_layer(name):
	mxd = arcpy.mapping.MapDocument("Current")
	lyrs = arcpy.mapping.ListLayers(mxd,"山")
	if len(lyrs)<1:
		return None
	else:
		return lyrs[0]

def getGCS_Point(layer):
	'''根据图层选择的唯一要素返回质心点经纬度坐标（Point），若选择不止一个要素则报错。'''
	lyr = __get_layer(layer)
	if lyr == None:
		raise Exception("未找到图层"+layer+"。")
	gsr = arcpy.Describe(lyr.name).spatialReference.GCS
	sels = lyr.getSelectionSet()
	if sels == None: raise Exception("未选择要素。")
	if len(sels)!=1: raise Exception("选择过多要素或未选择要素。")
	res=[]
	cur = arcpy.da.SearchCursor(lyr.name,["SHAPE@"],spatial_reference=gsr.exportToString())
	acc = 0
	for row in cur:
		res.append(row[0])
	del row, cur
	return res[0].trueCentroid

def getLatLong(layer):
	'''根据图层选择的唯一要素返回质心点经纬度坐标（list），若选择不止一个要素则报错。'''
	p = getGCS_Point(layer)
	return [p.X,p.Y]











