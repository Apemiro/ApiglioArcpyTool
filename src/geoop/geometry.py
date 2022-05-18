# -*- coding: UTF-8 -*-

import arcpy

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














