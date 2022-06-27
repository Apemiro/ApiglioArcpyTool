# -*- coding: UTF-8 -*-
# 根据图层返回集合列表

import arcpy


def to_list(dataset,field="SHAPE@"):
	res=[]
	cursor=arcpy.da.SearchCursor(dataset,[field])
	for row in cursor:
		res.append(row[0])
	del row,cursor
	return res

def to_set(dataset,field="SHAPE@"):
	res=set()
	cursor=arcpy.da.SearchCursor(dataset,[field])
	for row in cursor:
		res.add(row[0])
	del row,cursor
	return res

def shape_to_feature(geo,name,path="in_memory"):
	if geo.__class__==arcpy.PointGeometry:
		pass
	elif geo.__class__==arcpy.Point:
		pass
	elif geo.__class__==arcpy.Polyline:
		pass
	elif geo.__class__==arcpy.Polygon:
		pass
	else:
		raise Exception("无效的图形参数")
	if geo.firstPoint.Z<>None:
		zz="Enabled"
	else:
		zz="Disabled"
	if geo.firstPoint.M<>None:
		mm="Enabled"
	else:
		mm="Disabled"
	arcpy.management.CreateFeatureclass(path,name,geo.type.upper(),spatial_reference=geo.spatialReference,has_z=zz,has_m=mm)
	cursor=arcpy.da.InsertCursor(path+'/'+name,["SHAPE@"])
	cursor.insertRow([geo])
	del cursor

def to_file(list_of_geometry,dataset="temp_list_export",path="in_memory"):
	shape_type=list_of_geometry[0].type.upper()
	arcpy.management.CreateFeatureclass(path,dataset,shape_type)
	with arcpy.da.InsertCursor(path+"/"+dataset,["SHAPE@"]) as cursor:
		for shape in list_of_geometry:
			cursor.insertRow([shape])

#clear_feature("Test_Point2",["Shape@","Str"],lambda x:x[1]=="aaaaaaaaaa")
def clear_feature(feature_name,fields=["Shape@"],criterion=lambda x:True):
	with arcpy.da.UpdateCursor(feature_name,fields) as cursor:
		for row in cursor:
			if criterion(row):
				cursor.deleteRow()












