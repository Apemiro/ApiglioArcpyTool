# -*- coding: UTF-8 -*-
# 针对图层选择的操作

import arcpy
import arcpy.sa

def __active_df_sr():
	return arcpy.mapping.MapDocument(r"CURRENT").activeDataFrame.spatialReference.exportToString()

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



def getLayerDataFrame(layer_object):
	'''根据图层对象查找并返回其所属的数据框对象'''
	mxd = arcpy.mapping.MapDocument("Current")
	dfs = arcpy.mapping.ListDataFrames(mxd)
	for dfm in dfs:
		if layer_object in arcpy.mapping.ListLayers(mxd,"*",dfm):
			return dfm
	return None

def all_saw(layer):
	'''根据图层所在数据框的显示范围选择图层要素'''
	mxd = arcpy.mapping.MapDocument("Current")
	lyrs = arcpy.mapping.ListLayers(mxd, layer)
	if len(lyrs) != 1:
		raise Exception("存在重名图层，不能确定选择操作。")
	lyr = lyrs[0]
	dfm = getLayerDataFrame(lyr)
	dfm_ext = dfm.extent
	lyr.setSelectionSet("NEW",[])
	sr = dfm.spatialReference.exportToString()
	exts = []
	cursor = arcpy.da.SearchCursor(lyr.dataSource,["SHAPE@"],spatial_reference=sr)
	for row in cursor:
		exts.append(row[0].extent)
	sels = []
	for idx,pos in enumerate(exts):
		if dfm_ext.contains(pos):
			sels.append(idx)
	lyr.setSelectionSet("NEW",sels)
	arcpy.RefreshActiveView()
	arcpy.RefreshTOC()


