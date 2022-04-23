# -*- coding: UTF-8 -*-
# data frame tool
import arcpy

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
	
def center(data_frame_name):
	return __get_extent(data_frame_name)[0]
	
def width(data_frame_name):
	return __get_extent(data_frame_name)[1]
	
def height(data_frame_name):
	return __get_extent(data_frame_name)[2]
	
def left(data_frame_name):
	return __get_extent(data_frame_name)[3]
	
def right(data_frame_name):
	return __get_extent(data_frame_name)[4]
	
def lower(data_frame_name):
	return __get_extent(data_frame_name)[5]
	
def upper(data_frame_name):
	return __get_extent(data_frame_name)[6]
	
