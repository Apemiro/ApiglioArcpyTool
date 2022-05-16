# -*- coding: UTF-8 -*-
# 编辑折点
import arcpy


def map_points(geo,operation=lambda x:x):
	if geo.__class__==arcpy.PointGeometry:
		ptr=geo.getPart()
		ptr=operation(ptr)
		return arcpy.PointGeometry(ptr,geo.spatialReference,ptr.Z<>None,ptr.M<>None)
	elif geo.__class__==arcpy.Polyline or geo.__class__==arcpy.Polygon:
		parts=geo.getPart()
		parts_new=arcpy.Array()
		has_z,has_m=False,False
		for part in parts:
			part_new=arcpy.Array()
			for ptr in part:
				ptr=operation(ptr)
				has_z|=ptr.Z<>None
				has_m|=ptr.M<>None
				part_new.append(ptr)
			parts_new.append(part_new)
		return geo.__class__(parts_new,geo.spatialReference,has_z,has_m)
	else:
		raise Exception("暂不支持或无效的arcpy.Geometry类")

#map_points中operation(geo,h)参数的柯里化过程
def _currying_geo_setZ_(h):
	def result_func(point):
		x=point.X
		y=point.Y
		m=point.M
		return arcpy.Point(x,y,h,m)
	return result_func
def _currying_geo_addZ_(h):
	def result_func(point):
		x=point.X
		y=point.Y
		z=point.Z
		m=point.M
		return arcpy.Point(x,y,z+h,m)
	return result_func

def set_z_points(geo,z_value):
	func=_currying_geo_setZ_(z_value)
	return map_points(geo,operation=func)
def add_z_points(geo,z_offset):
	func=_currying_geo_addZ_(z_offset)
	return map_points(geo,operation=func)







































