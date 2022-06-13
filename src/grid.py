# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa

import os.path
import sys
sys.path.append(os.path.split(__file__)[0]+"/..")
import codetool.df as adf



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
	#return [x,y]
	return str(int(y)).zfill(f_digit)+str(int(x)).zfill(f_digit)
	
	
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

def __build_fine_grid_polygon(x,y,width,height,sr):
	p1=arcpy.Point(x,y)
	p2=arcpy.Point(x+width,y)
	p3=arcpy.Point(x+width,y+height)
	p4=arcpy.Point(x,y+height)
	arr = arcpy.Array([p1,p2,p3,p4])
	return arcpy.Polygon(arr,sr)

def build_fine_grid(width,height,pathname="in_memory",data_name="fine_grid"):
	ddf=adf.active_df()
	ext=ddf.extent
	if not adf.is_gcs:
		raise Exception("仅支持地理坐标系")
	if ext.width>0.5 or ext.height>0.5:
		raise Exception("格网过大")
	ll=ext.lowerLeft.X
	rr=ext.upperRight.X
	tt=ext.upperRight.Y
	bb=ext.lowerLeft.Y
	x1=ll-(ll%width)
	x2=rr-(rr%width)
	y1=bb-(bb%height)
	y2=tt-(tt%height)
	sr=adf.active_sr_str()
	arcpy.management.CreateFeatureclass(pathname, data_name, "POLYGON",spatial_reference=sr)
	arcpy.management.AddField(pathname+"/"+data_name,"M_ID","TEXT",field_length=3)
	arcpy.management.AddField(pathname+"/"+data_name,"F_ID","TEXT",field_length=6)
	arcpy.management.AddField(pathname+"/"+data_name,"Full_ID","TEXT",field_length=9)
	cursor = arcpy.da.InsertCursor(pathname+"/"+data_name, ["SHAPE@","M_ID","F_ID","Full_ID"])
	i=x1
	res=[]
	while i<=x2+width:
		j=y1
		while j<=y2+height:
			shape=__build_fine_grid_polygon(i,j,width,height,sr)
			res.append(shape)
			m_id=latlong2MID(i,j)
			f_id=latlong2FID(i,j)
			cursor.insertRow([shape,m_id,f_id,m_id+f_id])
			j+=height
		i+=width
	#return res

def build_related_grid(xy,data_name,offset=250):
	arcpy.management.CreateFeatureclass("in_memory", data_name, "POLYGON")
	x=xy[0]
	y=xy[1]
	
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
	
	
	
	
	
	
	
	
	
	
	
	

