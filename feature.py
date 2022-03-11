# -*- coding: UTF-8 -*-
import arcpy
import numpy
import random

#clear_feature("Test_Point2",["Shape@","Str"],lambda x:x[1]=="aaaaaaaaaa")
def clear_feature(feature_name,fields=["Shape@"],criterion=lambda x:True):
	with arcpy.da.UpdateCursor(feature_name,fields) as cursor:
		for row in cursor:
			if criterion(row):
				cursor.deleteRow()
			
	
def iterator(feature_name,method=None):
	if not callable(method):
		raise Exception("method参数需要是函数")
	tmp_feature="tmp_feature"
	with arcpy.da.UpdateCursor(feature_name,["FID"]) as cursor:
		for row in cursor:
			if type(row[0])==str:
				arcpy.FeatureClassToFeatureClass_conversion(feature_name,"in_memory",tmp_feature,'"FID" = '+"'"+(row[0])+"'")
			else:
				arcpy.FeatureClassToFeatureClass_conversion(feature_name,"in_memory",tmp_feature,'"FID" = '+str(row[0]))
			method(tmp_feature)
			arcpy.DeleteFeatures_management(tmp_feature)
	arcpy.DeleteFeatures_management(tmp_feature)
	
# def tmp_mtd(x):
	# target_layer_name=x+str(int(random.random()*100000))
	# arcpy.FeatureClassToFeatureClass_conversion(x,"in_memory",target_layer_name)
