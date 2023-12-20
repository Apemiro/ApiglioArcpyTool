# -*- coding: UTF-8 -*-
# mapping tool
# 设置标注的方法
import arcpy
import copy
import os

local_path           = os.path.split(__file__)[0]
prototype_layer      = arcpy.mapping.Layer(local_path+"/prototype.lyr")
prototype_labelclass = prototype_layer.labelClasses[0]

def document():
	return arcpy.mapping.MapDocument(r"CURRENT")

def active_doc():
	return arcpy.mapping.MapDocument(r"CURRENT")

def active_df():
	return active_doc().activeDataFrame

def active_sr():
	return active_df().spatialReference

def active_sr_str():
	return active_df().spatialReference.exportToString()

def test():
	return local_path

def apply_symbology_layerfile(in_symbology_layer, wildcard=""):
	lyrs = arcpy.mapping.ListLayers(active_doc(),wildcard)
	print "找到%d个符合名称条件的图层"%(len(lyrs),)
	try:
		for lyr in lyrs:
			arcpy.management.ApplySymbologyFromLayer(lyr, in_symbology_layer)
	except:
		print "图层“%s”修改符号系统失败，批量修改中止。"%(lyr.name,)


def layer_solo_export(layer_or_layers,pathname):
	#统计图层原本的显影性，并全部隐藏，再打开所有组图层
	lyrs = arcpy.mapping.ListLayers(active_doc(),"")
	layer_visibility = []
	for lyr in lyrs:
		vis = lyr.visible
		layer_visibility.append(tuple([lyr, vis]))
		if vis: lyr.visible = False
	for lyr in lyrs:
		if lyr.isGroupLayer: lyr.visible = True
	#导出指定图层
	if isinstance(layer_or_layers, list):
		for lyr in layer_or_layers:
			lyr.visible = True
			filename = lyr.name
			arcpy.mapping.ExportToPNG(active_doc(),pathname+'/'+filename)
			lyr.visible = False
	else:
		layer_or_layers.visible = True
		filename = layer_or_layers.name
		arcpy.mapping.ExportToPNG(active_doc(),pathname+'/'+filename)
		layer_or_layers.visible = False
	#关闭所有组图层，而后恢复图层原本的显影性
	for lyr in lyrs:
		if lyr.isGroupLayer: lyr.visible = False
	for lyr, vis in layer_visibility:
		if vis: lyr.visible = True
	arcpy.RefreshTOC()
	arcpy.RefreshActiveView()


