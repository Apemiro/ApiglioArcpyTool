# -*- coding: UTF-8 -*-
import arcpy

#python的风格让我无语
'''
def __shape_to_3d(geo,z):
	if type(geo) == arcpy.geometries.PointGeometry:
		ptr=geo.firstPoint
		ptr.Z=z
		return(arcpy.geometries.PointGeometry(ptr))
	elif type(geo) == arcpy.geometries.Polyline:
		arr=geo.getPart()[0]
		for i in arr:
			i.Z=z
		return(arcpy.Polyline(arcpy.Array(arr)))
	elif type(geo) == arcpy.geometries.Polygon:
		arr=geo.getPart()
		for i in arr:
			for j in i:
				j.Z=z
		return(arcpy.Polygon(arcpy.Array(arr)))
	else:
		raise Exception("错误的文件几何类型。")
'''

def CopyTo3D(dataset,field_name,key=lambda x:x):
	dst_dataset="temp_3d_"+dataset
	shape_type=arcpy.Describe(dataset).shapeType
	prj_info=arcpy.Describe(dataset).spatialReference.exportToString()
	arcpy.CreateFeatureclass_management("in_memory", dst_dataset, geometry_type=shape_type,has_z="ENABLED",spatial_reference=prj_info)
	fields_list=arcpy.Describe("archi_outside").fields
	fields_list_str=[]
	idx=0
	acc=0
	for field in fields_list[2:]:
		fields_list_str.append(field.name)
		arcpy.AddField_management(dst_dataset,field.name,field.type,field.precision,field.scale,field.length,field.aliasName,field.isNullable,field.required,field.domain)
		if field.name==field_name:
			idx=acc
		acc+=1
	if idx==0:
		raise Exception("找不到字段"+field_name+"。")
	cursor=arcpy.da.SearchCursor(dataset,["SHAPE@"]+fields_list_str)
	dst_cursor=arcpy.da.InsertCursor(dst_dataset,["SHAPE@"]+fields_list_str)
	tmp_lst=[]
	for row in cursor:
		shp=row[0]
		z=key(row[idx+1])
		shp=__shape_to_3d(shp,z)
		tmp_lst.append(z)
		other_values=row[1:]
		dst_cursor.insertRow([shp]+list(other_values))
	del row,cursor,dst_cursor
	return(tmp_lst)
	
	


























