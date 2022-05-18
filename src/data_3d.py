# -*- coding: UTF-8 -*-
import arcpy
import apiglio.src.geoop.points as apgeo_points


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

def skyline_table_to_polygon(in_table,out_dataset,path="in_memory"):
	point_coords=[]
	acc=-1
	break_point=-1
	last_value=400 # 大于最大水平角
	cursor=arcpy.da.UpdateCursor(in_table,["HORIZ_ANG","ZENITH_ANG"])
	for row in cursor:
		acc+=1
		point_coords.append(row)
		if row[0]>last_value+10:
			break_point=acc
			#循环条件的+10毫无意义，浮点型比较的特性，以后再管为啥吧
		last_value=row[0]
	point_coords_sorted=point_coords[break_point:]+point_coords[:break_point]
	del cursor
	point_coords_sorted.insert(0,[360.0,0.0])
	point_coords_sorted.append([0.0,0.0])
	points=[]
	for p in point_coords_sorted:
		points.append(arcpy.Point(*p))
	ploygon=arcpy.Polygon(arcpy.Array(points))
	arcpy.management.CreateFeatureclass(path,out_dataset,"POLYGON")
	cursor=arcpy.da.InsertCursor(path+'/'+out_dataset,["SHAPE@"])
	cursor.insertRow([ploygon])
	del cursor



















