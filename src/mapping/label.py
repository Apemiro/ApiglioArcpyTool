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















