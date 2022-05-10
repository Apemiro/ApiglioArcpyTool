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

def _set_z_operation(point):
	res=point.clone
	res.Z=z
	return res

def set_z_points(geo,z_operation=lambda x:0):
	_set_z_operation=lambda x
	map_points(geo,operation=_set_z_operation)









































