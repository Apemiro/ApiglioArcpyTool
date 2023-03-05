# -*- coding: UTF-8 -*-
# 通过geometry计算geometry的方法

import arcpy

def line_segment(p1,p2):
	if p1.__class__ <> arcpy.Point:
		raise Exception("参数p1不是arcpy.Point类型")
	if p2.__class__ <> arcpy.Point:
		raise Exception("参数p2不是arcpy.Point类型")
	res = arcpy.Array([p1,p2])
	return(arcpy.Polyline(res))

def half_line(point,vector,length=None):
	if point.__class__ <> arcpy.Point:
		raise Exception("参数point不是arcpy.Point类型")
	if vector.__class__ <> list:
		raise Exception("参数vector不是list类型")
	if len(vector) <> 2:
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






def face2lines(face):
	if face.__class__ <> arcpy.Polygon:
		raise Exception("参数face不是arcpy.Polygon类型")
	parts = face.getPart()
	return list(map(lambda x:arcpy.Polyline(x),parts))

























