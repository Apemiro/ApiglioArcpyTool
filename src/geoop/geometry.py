# -*- coding: UTF-8 -*-

import arcpy
import math

def polygon(coords):
	points=[]
	for p in coords:
		points.append(arcpy.Point(*p))
	arr=arcpy.Array(points)
	return arcpy.Polygon(arr)

def polygon_cell(top,left,right,bottom):
	points=[]
	points.append(arcpy.Point(left,top))
	points.append(arcpy.Point(right,top))
	points.append(arcpy.Point(right,bottom))
	points.append(arcpy.Point(left,bottom))
	arr=arcpy.Array(points)
	return arcpy.Polygon(arr)

def polygon_cell_center(center,width,height):
	x=center[0]
	y=center[1]
	hw=width/2
	hh=height/2
	points=[]
	points.append(arcpy.Point(x-hw,y+hh))
	points.append(arcpy.Point(x+hw,y+hh))
	points.append(arcpy.Point(x+hw,y-hh))
	points.append(arcpy.Point(x-hw,y-hh))
	arr=arcpy.Array(points)
	return arcpy.Polygon(arr)

def polyline(coords,closed=False):
	points=[]
	if closed and coords[0]<>coords[-1]:
		coords.append(coords[0])
	for p in coords:
		points.append(arcpy.Point(*p))
	arr=arcpy.Array(points)
	return arcpy.Polyline(arr)

def __point_angle_offset(point,radian_angle,length):
	ori_x = point.X
	ori_y = point.Y
	default_Z = None if point.Z==None else 0
	default_M = None if point.M==None else 0
	new_x = ori_x+length*math.cos(radian_angle)
	new_y = ori_y+length*math.sin(radian_angle)
	return arcpy.Point(new_x,new_y,default_Z,default_M)

def sector(point,orie_deg_1,orie_deg_2,radius,segment=96):
	ori_x = point.X
	ori_y = point.Y
	deg_1 = orie_deg_1%360
	deg_2 = orie_deg_2%360
	while deg_2>deg_1: deg_2-=360
	while deg_2<deg_1: deg_2+=360
	rad_1 = math.pi*deg_1/180.0
	rad_2 = math.pi*deg_2/180.0
	seg_n = int(segment*(deg_2-deg_1)/360.0)
	if seg_n<1: seg_n=1
	delta_rad = (rad_2 - rad_1) / seg_n
	points = [point]
	for idx in range(seg_n):
		angle = rad_1+delta_rad*idx
		points.append(__point_angle_offset(point,angle,radius))
	points.append(__point_angle_offset(point,rad_2,radius))
	return arcpy.Polygon(arcpy.Array(points))
	

def polyline_offset_point(polyline, x, y):
	'''	根据给定的polyline计算生成偏移点Arcpy.Point， x为起始点到终点的距离行进距离， y为垂直于行进方向的偏移， 左侧为正方向。'''
	pass

def add_face(coords,dataset="TempFace",path="in_memory"):
	geo=ploygon(coords)
	if geo.firstPoint.Z<>None:
		zz="Enabled"
	else:
		zz="Disabled"
	if geo.firstPoint.M<>None:
		mm="Enabled"
	else:
		mm="Disabled"
	arcpy.management.CreateFeatureclass(path,dataset,"POLYGON",has_z=zz,has_m=mm)
	cursor=arcpy.da.InsertCursor(path+'/'+dataset,["SHAPE@"])
	cursor.insertRow([geo])
	del cursor
	return geo

def add_line(coords,dataset="TempLine",path="in_memory",closed=False):
	geo=ployline(coords,closed)
	if geo.firstPoint.Z<>None:
		zz="Enabled"
	else:
		zz="Disabled"
	if geo.firstPoint.M<>None:
		mm="Enabled"
	else:
		mm="Disabled"
	arcpy.management.CreateFeatureclass(path,dataset,"POLYLINE",has_z=zz,has_m=mm)
	cursor=arcpy.da.InsertCursor(path+'/'+dataset,["SHAPE@"])
	cursor.insertRow([geo])
	del cursor
	return geo














