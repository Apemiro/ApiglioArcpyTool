# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa

def raw2blk(filename_list):
	for filename in filename_list:
		b1=arcpy.Raster(filename+'/Band_3')
		b2=arcpy.Raster(filename+'/Band_2')
		r_out=b1*256+b2
		r_out.save('BLK_'+filename)

def height2shadow(filename_list):
	for filename in filename_list:
		r_in=arcpy.Raster(filename+'/Band_4')
		r_out=arcpy.sa.Hillshade(r_in, 180, 75, "SHADOWS", 0.35)
		r_out.save('HS_'+filename)

