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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

