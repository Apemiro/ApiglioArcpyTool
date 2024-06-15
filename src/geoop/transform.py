# -*- coding: UTF-8 -*-
# 平移、缩放、旋转等连续性变换

import arcpy


#issubclass(arcpy.geometries.PointGeometry,arcpy.geometries.Geometry)


def translation(geo,offset):
	if not issubclass(geo.__class__,arcpy.Geometry):
		raise Exception("geo必须是arcpy.Geometry类")
	x_offset=offset[0]
	y_offset=offset[1]
	if type(geo) == arcpy.geometries.PointGeometry:
		ptr=geo.firstPoint
		ptr.X+=x_offset
		ptr.Y+=y_offset
		return(arcpy.geometries.PointGeometry(ptr))
	elif type(geo) == arcpy.geometries.Polyline:
		arr=geo.getPart()[0]
		for i in arr:
			i.X+=x_offset
			i.Y+=y_offset
		return(arcpy.Polyline(arcpy.Array(arr)))
	elif type(geo) == arcpy.geometries.Polygon:
		arr=geo.getPart()
		for i in arr:
			for j in i:
				j.X+=x_offset
				j.Y+=y_offset
		return(arcpy.Polygon(arcpy.Array(arr)))
	else:
		print(type(geo))
		raise Exception("错误的文件几何类型")

def scaling(geo,offset,origin=[0,0]):
	x_times=offset[0]
	y_times=offset[1]
	x_origin=origin[0]
	y_origin=origin[1]
	if type(geo) == arcpy.geometries.PointGeometry:
		ptr=geo.firstPoint
		ptr.X-=x_origin
		ptr.Y-=y_origin
		ptr.X*=x_times
		ptr.Y*=y_times
		ptr.X+=x_origin
		ptr.Y+=y_origin
		return(arcpy.geometries.PointGeometry(ptr))
	elif type(geo) == arcpy.geometries.Polyline:
		arr=geo.getPart()[0]
		for i in arr:
			i.X-=x_origin
			i.Y-=y_origin
			i.X*=x_times
			i.Y*=y_times
			i.X+=x_origin
			i.Y+=y_origin
		return(arcpy.Polyline(arcpy.Array(arr)))
	elif type(geo) == arcpy.geometries.Polygon:
		arr=geo.getPart()
		new_parts = []
		for i in arr:
			new_vertices = []
			for j in i:
				v=j
				v.X -= x_origin
				v.Y -= y_origin
				v.X *= x_times
				v.Y *= y_times
				v.X += x_origin
				v.Y += y_origin
				new_vertices.append(v)
			new_parts.append(new_vertices)
		return(arcpy.Polygon(arcpy.Array(new_parts)))
	else:
		print(type(geo))
		raise Exception("错误的文件几何类型")




































