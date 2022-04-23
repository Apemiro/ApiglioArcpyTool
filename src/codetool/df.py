# -*- coding: UTF-8 -*-
# data frame tool
import arcpy
import math

def __get_extent(data_frame_name):
	mxd = arcpy.mapping.MapDocument(r"CURRENT")
	data_frames = arcpy.mapping.ListDataFrames(mxd, data_frame_name)
	if data_frames==[]:
		raise Exception("找不到符合条件的数据框")
	else:
		data_frame = data_frames[0]
	ll=data_frame.extent.lowerLeft
	ur=data_frame.extent.upperRight
	lower=ll.Y
	left=ll.X
	upper=ur.Y
	right=ur.X
	center=[left+(right-left)/2.0,lower+(upper-lower)/2.0]
	# [center, width, height, x0, x1, y0, y1]
	return [center,right-left,upper-lower,left,right,lower,upper]
	
def center(data_frame_name="*"):
	return __get_extent(data_frame_name)[0]
	
def width(data_frame_name="*"):
	return __get_extent(data_frame_name)[1]
	
def height(data_frame_name="*"):
	return __get_extent(data_frame_name)[2]
	
def left(data_frame_name="*"):
	return __get_extent(data_frame_name)[3]
	
def right(data_frame_name="*"):
	return __get_extent(data_frame_name)[4]
	
def lower(data_frame_name="*"):
	return __get_extent(data_frame_name)[5]
	
def upper(data_frame_name="*"):
	return __get_extent(data_frame_name)[6]
	
def createViewBox(data_frame_name="*",in_memory_feature="TempViewBox"):
	arcpy.CreateFeatureclass_management("in_memory", in_memory_feature, "POLYGON")
	res=__get_extent(data_frame_name)
	p1=arcpy.Point(res[3],res[5])
	p2=arcpy.Point(res[3],res[6])
	p3=arcpy.Point(res[4],res[6])
	p4=arcpy.Point(res[4],res[5])
	arr = arcpy.Array([p1,p2,p3,p4])
	polygon = arcpy.Polygon(arr)
	cursor = arcpy.da.InsertCursor(in_memory_feature, ["SHAPE@"])
	cursor.insertRow([polygon])

def createViewCircle(segment=24,data_frame_name="*",in_memory_feature="TempViewCircle"):
	arcpy.CreateFeatureclass_management("in_memory", in_memory_feature, "POLYGON")
	res=__get_extent(data_frame_name)
	diam=res[1]
	if res[2]<diam:
		diam=res[2]
	radius=diam/2.0
	x0=res[0][0]
	y0=res[0][1]
	points=[]
	for i in range(0,segment):
		angle=2*i*math.pi/segment
		x=x0+radius*math.cos(angle)
		y=y0+radius*math.sin(angle)
		points.append(arcpy.Point(x,y))
	arr = arcpy.Array(points)
	polygon = arcpy.Polygon(arr)
	cursor = arcpy.da.InsertCursor(in_memory_feature, ["SHAPE@"])
	cursor.insertRow([polygon])

































