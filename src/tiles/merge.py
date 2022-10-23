# -*- coding: UTF-8 -*-
import arcpy
import sys
import os.path
import math


global_n = 85.05
global_s = -85.05
x0_width = 360.0
x0_height = global_n - global_s

# https://zhuanlan.zhihu.com/p/363654824
def wmts_tile_name_to_extent(filename):
	#filename 形如LL\col\row.png
	sp = os.path.split(filename.replace("/","\\"))
	sp1=sp[0].split("\\")
	sp2=sp[1].split(".")
	level = int(sp1[0])
	col = int(sp1[1])
	row = int(sp2[0])
	lng1 = 360.0*col/2**level-180.0
	lat1 = math.atan(math.sinh(math.pi-2*math.pi*row/2**level))*180/math.pi
	lng2 = 360.0*(col+1)/2**level-180.0
	lat2 = math.atan(math.sinh(math.pi-2*math.pi*(row+1)/2**level))*180/math.pi
	return [lng1,lat1,lng2,lat2]
	





def load_from_path(path,extent=None):
	if extent==None:
		extent=arcpy.Extent(,,,,)
	filenames=[]
	for folder,what,files in os.walk(path):
		for filename in files:
			filenames.append(folder+"/"+filename)
	for filename in filenames:
		

		
# tfw file
# x' = Ax + Cy + E
# y' = Bx + Dy + F




























