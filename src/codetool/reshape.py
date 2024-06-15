# -*- coding: UTF-8 -*-

import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import feature as af
import geoop.transform as atrans
import math
import arcpy

'''目前这里用dict_to_file的做法对shapefile都不是很友好，dict_to_file还要再改进才好'''

def scaling(input_feature, output_feature, scale_base, scale_field=None):
	inp_list = af.to_dict(input_feature)
	out_list = []
	for fea in inp_list:
		shape = fea["SHAPE@"]
		multi = scale_base
		if scale_field != None:
			multi *= fea[scale_field]
		centroid = shape.centroid
		new_shape = atrans.scaling(shape,[multi]*2,[centroid.X,centroid.Y])
		fea["SHAPE@"]=new_shape
		out_list.append(fea)
	path, dataset = os.path.split(output_feature)
	af.dict_to_file(out_list,dataset,path)

def dir_deg2rad(x):
	return x*math.pi/180.0

def direction(input_feature, output_feature, direction_radian_field, distance_field, direction_projection=dir_deg2rad, distance_projection=lambda x:x, two_direction=False):
	inp_list = af.to_dict(input_feature)
	out_list = []
	for fea in inp_list:
		shape = fea["SHAPE@"]
		direc = fea[direction_radian_field]
		dista = fea[distance_field]
		p1 = shape.centroid
		p1x = p1.X
		p1y = p1.Y
		dx = distance_projection(dista)*math.cos(direction_projection(direc))
		dy = distance_projection(dista)*math.sin(direction_projection(direc))
		p2 = arcpy.Point(p1x+dx, p1y+dy)
		p0 = arcpy.Point(p1x-dx, p1y-dy)
		if two_direction:
			new_shape = arcpy.Polyline(arcpy.Array([p0,p1,p2]))
		else:
			new_shape = arcpy.Polyline(arcpy.Array([p1,p2]))
		fea["SHAPE@"]=new_shape
		out_list.append(fea)
	path, dataset = os.path.split(output_feature)
	af.dict_to_file(out_list,dataset,path)









