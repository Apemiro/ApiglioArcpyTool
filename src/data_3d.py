# -*- coding: UTF-8 -*-
import arcpy
import sys
import os.path
sys.path.append(os.path.split(__file__)[0])
import geoop.points as apgeo_points
#import geoop.geometry as apgeo_geometry


def CopyTo3D(dataset,dst_dataset,field_name,key=lambda x:x):
	#dst_dataset="temp_3d_"+dataset
	shape_type=arcpy.Describe(dataset).shapeType
	prj_info=arcpy.Describe(dataset).spatialReference.exportToString()
	arcpy.management.CreateFeatureclass("in_memory", dst_dataset, geometry_type=shape_type,has_z="ENABLED",spatial_reference=prj_info)
	fields_list=arcpy.Describe(dataset).fields
	fields_list_str=[]
	idx=-1
	acc=0
	for field in fields_list[2:]:
		fields_list_str.append(field.name)
		arcpy.management.AddField(dst_dataset,field.name,field.type,field.precision,field.scale,field.length,field.aliasName,field.isNullable,field.required,field.domain)
		if field.name==field_name:
			idx=acc
		acc+=1
	if idx<0:
		raise Exception("找不到字段"+field_name+"。")
	cursor=arcpy.da.SearchCursor(dataset,["SHAPE@"]+fields_list_str)
	dst_cursor=arcpy.da.InsertCursor(dst_dataset,["SHAPE@"]+fields_list_str)
	tmp_lst=[]
	for row in cursor:
		shp=row[0]
		z=key(row[idx+1])
		shp=apgeo_points.set_z_points(shp,z)
		tmp_lst.append(z)
		other_values=row[1:]
		dst_cursor.insertRow([shp]+list(other_values))
	del row,cursor,dst_cursor
	return(tmp_lst)










































