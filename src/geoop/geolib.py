# -*- coding: UTF-8 -*-
# 通过geometry计算geometry的方法

import arcpy
import numpy
import random

def line_segment(p1,p2):
	if p1.__class__ != arcpy.Point:
		raise Exception("参数p1不是arcpy.Point类型")
	if p2.__class__ != arcpy.Point:
		raise Exception("参数p2不是arcpy.Point类型")
	res = arcpy.Array([p1,p2])
	return(arcpy.Polyline(res))

def half_line(point,vector,length=None):
	if point.__class__ != arcpy.Point:
		raise Exception("参数point不是arcpy.Point类型")
	if vector.__class__ != list:
		raise Exception("参数vector不是list类型")
	if len(vector) != 2:
		raise Exception("参数vector长度不为2")
	vec_x = float(vector[0])
	vec_y = float(vector[1])
	if length<>None:
		ori_len = (vec_x**2 + vec_y**2)**0.5
		vec_x /= ori_len / length
		vec_y /= ori_len / length
	end_x = point.X + vec_x
	end_y = point.Y + vec_y
	end   = arcpy.Point(end_x,end_y)
	res   = arcpy.Array([point,end])
	return(arcpy.Polyline(res))





def __flatten(arr):
	res=[]
	index  = 0
	length = arr.__len__()
	while index < length:
		item = arr[index]
		methods = dir(item)
		if '__len__' in methods and '__getitem__' in methods:
			res += __flatten(item)
		else:
			res.append(arr[index])
		index+=1
	return(res)

def to_point(geo):
	if   geo.__class__ in [arcpy.Point]:
		return geo
	elif geo.__class__ in [arcpy.Polyline, arcpy.Polygon, arcpy.Multipatch, arcpy.Multipoint]:
		return __flatten(geo.getPart())
	elif geo.__class__ in [list, arcpy.Array, numpy.ndarray]:
		if not len(geo) in range(2,5):
			raise Exception("参数geo是坐标列表时必须是2~4维坐标")
		return arcpy.Point(*geo)
	else:
		raise Exception("参数geo不是有效类型")

def to_polyline(geo):
	if   geo.__class__ in [arcpy.Point]:
		raise Exception("参数geo不能是单个点")
	elif geo.__class__ in [arcpy.Polyline]:
		return geo
	elif geo.__class__ in [arcpy.Polygon, arcpy.Multipatch]:
		return arcpy.Polyline(geo.getPart())
	elif geo.__class__ in [arcpy.Multipoint]:
		return arcpy.Polyline(arcpy.Array([geo.getPart()]))
	elif geo.__class__ in [list, arcpy.Array, numpy.ndarray]:
		if len(geo)<2:
			raise Exception("参数geo是点列表时至少要包含两项")
		vertices = list(map(lambda x:to_point(x),geo))
		array = arcpy.Array(vertices)
		return arcpy.Polyline(arcpy.Array(array))
	else:
		raise Exception("参数geo不是有效类型")

def to_polygon(geo):
	if   geo.__class__ in [arcpy.Point]:
		raise Exception("参数geo不能是单个点")
	elif geo.__class__ in [arcpy.Polygon]:
		return geo
	elif geo.__class__ in [arcpy.Polyline, arcpy.Multipatch]:
		return arcpy.Polygon(geo.getPart())
	elif geo.__class__ in [arcpy.Multipoint]:
		return arcpy.Polygon(arcpy.Array([geo.getPart()]))
	elif geo.__class__ in [list, arcpy.Array, numpy.ndarray]:
		if len(geo)<2:
			raise Exception("参数geo是点列表时至少要包含两项")
		vertices = list(map(lambda x:to_point(x),geo))
		array = arcpy.Array(vertices)
		return arcpy.Polygon(arcpy.Array(array))
	else:
		raise Exception("参数geo不是有效类型")






def random_point(data_frame=None,hasZ=False,hasM=False):
	if data_frame == None:
		x_min = 0.0
		y_min = 0.0
		x_max = 1.0
		y_max = 1.0
	else:
		y_min = data_frame.extent.YMin
		x_min = data_frame.extent.XMin
		y_max = data_frame.extent.YMax
		x_max = data_frame.extent.XMax
	rand_x = random.random() * (x_max - x_min) + x_min
	rand_y = random.random() * (y_max - y_min) + y_min
	if hasM:
		return arcpy.Point(rand_x,rand_y,0,0)
	elif hasZ:
		return arcpy.Point(rand_x,rand_y,0)
	else:
		return arcpy.Point(rand_x,rand_y)
















