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





#apiglio.src.codetool.feature.listdict_to_line([{"x1":110.2,"y1":34.4,"x2":111.23,"y2":36.32,"testf":"d3wd"}],"x1","y1","x2","y2")
#apiglio.src.codetool.feature.listdict_to_line(part_of,"subject_lng","subject_lat","object_lng","object_lat")
def listdict_to_line(list_of_dictionary,x1,y1,x2,y2,dataset="temp_listdict_line_export",path="in_memory"):
	example=list_of_dictionary[0]
	example_key=example.keys()
	try:
		example_key.index(x1)
		example_key.index(x2)
		example_key.index(y1)
		example_key.index(y2)
	except:
		raise Exception("one of x1,y1,x2,y2 field not found.")
	filtered_fields=list(set(example_key)-set([x1,y1,x2,y2]))
	arcpy.management.CreateFeatureclass(path,dataset,"POLYLINE")
	output_edges = path + "/" + dataset
	for field in filtered_fields:
		arcpy.management.AddField(output_edges, field, "TEXT",field_length=100)
	with arcpy.da.InsertCursor(path+"/"+dataset,["SHAPE@"]+filtered_fields) as cursor:
		for dict_element in list_of_dictionary:
			coord_x1 = dict_element[x1]
			coord_y1 = dict_element[y1]
			coord_x2 = dict_element[x2]
			coord_y2 = dict_element[y2]
			p1 = arcpy.Point(coord_x1,coord_y1)
			p2 = arcpy.Point(coord_x2,coord_y2)
			line = arcpy.Polyline(arcpy.Array([p1,p2]))
			rows = [line]
			for field in filtered_fields:
				rows.append(dict_element[field])
			cursor.insertRow(rows)




