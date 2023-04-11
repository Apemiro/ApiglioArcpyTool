# -*- coding: UTF-8 -*-
# data frame tool
import arcpy
import math

isAddOutputsToMap=arcpy.env.addOutputsToMap

def BeginUpdate():
	isAddOutputsToMap=arcpy.env.addOutputsToMap
	arcpy.env.addOutputsToMap=False
	print("禁用导出自动加载为图层")
def EndUpdate():
	arcpy.env.addOutputsToMap=isAddOutputsToMap
	print("启用导出自动加载为图层")

def document():
	return arcpy.mapping.MapDocument(r"CURRENT")

def active_doc():
	return arcpy.mapping.MapDocument(r"CURRENT")

def active_df():
	return active_doc().activeDataFrame

def active_sr():
	return active_df().spatialReference

def active_sr_str():
	return active_df().spatialReference.exportToString()

def data_frame(data_frame_name=""):
	if data_frame_name=="":
		return active_df()
	mxd = document()
	data_frames = arcpy.mapping.ListDataFrames(mxd, data_frame_name)
	if data_frames==[]:
		raise Exception("找不到符合条件的数据框")
	else:
		return(data_frames[0])

def check_data_frame_sr_valid(data_frame_name=""):
	ddf=data_frame(data_frame_name)
	sr_str=ddf.spatialReference.exportToString()[:6]
	if sr_str==u"PROJCS" or sr_str==u"GEOGCS":
		return True
	else:
		return False

def str_data_frame_sr(data_frame_name=""):
	ddf=data_frame(data_frame_name)
	return ddf.spatialReference.exportToString()
	
def is_gcs(data_frame_name=""):
	ddf=data_frame(data_frame_name)
	sr_str=ddf.spatialReference.exportToString()[:6]
	if sr_str==u"GEOGCS":
		return True
	else:
		return False

def is_pcs(data_frame_name=""):
	ddf=data_frame(data_frame_name)
	sr_str=ddf.spatialReference.exportToString()[:6]
	if sr_str==u"PROJCS":
		return True
	else:
		return False

def __get_extent(data_frame_name=""):
	dfm=data_frame(data_frame_name)
	ll=dfm.extent.lowerLeft
	ur=dfm.extent.upperRight
	lower=ll.Y
	left=ll.X
	upper=ur.Y
	right=ur.X
	center=[left+(right-left)/2.0,lower+(upper-lower)/2.0]
	# [center, width, height, x0, x1, y0, y1]
	return [center,right-left,upper-lower,left,right,lower,upper]
	
def center(data_frame_name=""):
	return __get_extent(data_frame_name)[0]
	
def width(data_frame_name=""):
	return __get_extent(data_frame_name)[1]
	
def height(data_frame_name=""):
	return __get_extent(data_frame_name)[2]
	
def left(data_frame_name=""):
	return __get_extent(data_frame_name)[3]
	
def right(data_frame_name=""):
	return __get_extent(data_frame_name)[4]
	
def lower(data_frame_name=""):
	return __get_extent(data_frame_name)[5]
	
def upper(data_frame_name=""):
	return __get_extent(data_frame_name)[6]
	
def createViewBox(data_frame_name="",in_memory_feature="TempViewBox"):
	#if not check_data_frame_sr_valid(data_frame_name):
	#	raise Exception("未知坐标系不能生成目标要素。")
	#sr=str_data_frame_sr
	arcpy.management.CreateFeatureclass("in_memory", in_memory_feature, "POLYGON")
	#arcpy.management.DefineProjection(in_memory_feature,sr)
	res=__get_extent(data_frame_name)
	p1=arcpy.Point(res[3],res[5])
	p2=arcpy.Point(res[3],res[6])
	p3=arcpy.Point(res[4],res[6])
	p4=arcpy.Point(res[4],res[5])
	arr = arcpy.Array([p1,p2,p3,p4])
	polygon = arcpy.Polygon(arr)
	cursor = arcpy.da.InsertCursor(in_memory_feature, ["SHAPE@"])
	cursor.insertRow([polygon])

def createViewCircle(segment=24,data_frame_name="",in_memory_feature="TempViewCircle"):
	#if not check_data_frame_sr_valid(data_frame_name):
	#	raise Exception("未知坐标系不能生成目标要素。")
	#sr=str_data_frame_sr
	arcpy.management.CreateFeatureclass("in_memory", in_memory_feature, "POLYGON")
	#arcpy.management.DefineProjection(in_memory_feature,sr)
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

def createViewCenter(data_frame_name="",in_memory_feature="TempViewPoint",has_z=False,has_m=False):
	#if not check_data_frame_sr_valid(data_frame_name):
	#	raise Exception("未知坐标系不能生成目标要素。")
	zz="Disabled"
	mm="Disabled"
	if has_z: zz="Enabled"
	if has_m: mm="Enabled"
	#sr=str_data_frame_sr
	res=__get_extent(data_frame_name)
	arcpy.management.CreateFeatureclass("in_memory", in_memory_feature, "POINT")
	#arcpy.management.DefineProjection(in_memory_feature,sr)
	pts = arcpy.Point(res[0][0],res[0][1],0,0)
	cursor = arcpy.da.InsertCursor(in_memory_feature, ["SHAPE@"])
	cursor.insertRow([pts])

def list_layer(wildcard="*",data_frame_name=""):
	mxd=document()
	ddf=data_frame(data_frame_name)
	return arcpy.mapping.listLayers(mxd,wildcard,ddf)

def add_layer(filename,data_frame_name="",position="TOP"):
	ddf=data_frame(data_frame_name)
	nl=arcpy.mapping.Layer(filename)
	arcpy.mapping.AddLayer(ddf,nl,position)

def del_layer(layername):
	raise Exception("unimplemented")

def pan2S(step=1.0):
	dfm = active_df()
	print(dfm.extent)
	ll = dfm.extent.lowerLeft
	ur = dfm.extent.upperRight
	dist = (ur.Y - ll.Y) * step
	ext = arcpy.Extent(ll.X, ll.Y + dist, ur.X, ur.Y + dist)
	print(ext)
	dfm.panToExtent(ext)

def pan2N(step=1.0):
	dfm = active_df()
	print(dfm.extent)
	ll = dfm.extent.lowerLeft
	ur = dfm.extent.upperRight
	dist = (ur.Y - ll.Y) * step
	ext = arcpy.Extent(ll.X, ll.Y - dist, ur.X, ur.Y - dist)
	print(ext)
	dfm.panToExtent(ext)

def pan2E(step=1.0):
	dfm = active_df()
	print(dfm.extent)
	ll = dfm.extent.lowerLeft
	ur = dfm.extent.upperRight
	dist = (ur.X - ll.X) * step
	ext = arcpy.Extent(ll.X + dist, ll.Y, ur.X + dist, ur.Y)
	print(ext)
	dfm.panToExtent(ext)

def pan2W(step=1.0):
	dfm = active_df()
	print(dfm.extent)
	ll = dfm.extent.lowerLeft
	ur = dfm.extent.upperRight
	dist = (ur.X - ll.X) * step
	ext = arcpy.Extent(ll.X - dist, ll.Y, ur.X - dist, ur.Y)
	print(ext)
	dfm.panToExtent(ext)
























