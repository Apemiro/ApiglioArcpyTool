# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa




def latlong2MID(lng,lat):
	lng_w=114.5
	lng_e=123.0
	lat_s=34.0
	lat_n=38.5
	
	first_char='@'
	first_num=0
	
	m_digit=2
	f_digit=3
	width_m=10*60 # seconds
	width_f=3     # seconds
	
	x=int((lng-lng_w)*3600/width_m)
	y=int((lat-lat_s)*3600/width_m)
	return chr(ord(first_char)+x)+str(y).zfill(m_digit)
	

def latlong2FID(lng,lat):
	lng_w=114.5
	lng_e=123.0
	lat_s=34.0
	lat_n=38.5
	
	first_char='@'
	first_num=0
	
	m_digit=2
	f_digit=3
	width_m=10*60 # seconds
	width_f=3     # seconds
	
	x=((lng-lng_w)*3600 % width_m / f_digit)
	y=((lat-lat_s)*3600 % width_m / f_digit)
	return [x,y]
	return str(y).zfill(f_digit)+str(x).zfill(f_digit)
	
	
def current_data_center(data_frame_name):
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
	return [left+(right-left)/2.0,lower+(upper-lower)/2.0]
	
	
def build_related_grid(x,y,data_name,offset=250):
	arcpy.CreateFeatureclass_management("in_memory", data_name, "POLYGON")
	
	x0=x-offset
	x1=x+offset
	y0=y-offset
	y1=y+offset
	
	p1=arcpy.Point(x0,y0)
	p2=arcpy.Point(x1,y0)
	p3=arcpy.Point(x1,y1)
	p4=arcpy.Point(x0,y1)
	arr = arcpy.Array([p1,p2,p3,p4])
	polygon = arcpy.Polygon(arr)
	cursor = arcpy.da.InsertCursor(data_name, ["SHAPE@"])
	cursor.insertRow([polygon])
	
	
	
	
	
	
	
	
	
	
	
	

