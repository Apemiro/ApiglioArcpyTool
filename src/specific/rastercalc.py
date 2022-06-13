# -*- coding: UTF-8 -*-
# skyline tool

import arcpy
# import numpy
import os
import re
# import os.path
# import sys
# sys.path.append(os.path.split(__file__)[0]+"/..")
# import codetool.df
# import map_feature



def load_rgb_from_dir(path):
	filenames=os.listdir(path)
	bands=[[],[],[]]
	for filename in filenames:
		tmp=path+"/"+filename
		bands[0].append(arcpy.Raster(tmp+"/band_1"))
		bands[1].append(arcpy.Raster(tmp+"/band_2"))
		bands[2].append(arcpy.Raster(tmp+"/band_3"))
	return bands

def load_band_from_dir(path,regexpr):
	filenames=os.listdir(path)
	bands=[]
	for filename in filter(lambda x:re.search(regexpr,x)!=None,filenames):
		tmp=path+"/"+filename
		bands.append(arcpy.Raster(tmp))
		#print(tmp)
	return bands

def generalize(ras):
	v2=ras.maximum
	v1=ras.minimum
	res=ras-float(v1)
	res/=float(v2-v1)
	return res

def mean(ras_list):
	count=len(ras_list)
	res=ras_list[0]+0
	for ras in ras_list[1:]:
		res+=ras
	res/=float(count)
	return res

def sum(ras_list):
	res=ras_list[0]+0
	for ras in ras_list[1:]:
		res+=ras
	return res

def mean_deviation(ras_list,save_name):
	generalized_list=map(generalize,ras_list)
	aver=mean(generalized_list)
	res=generalized_list[0]-aver
	res=abs(res)
	for ras in generalized_list[1:]:
		tmp=ras-aver
		tmp=abs(tmp)
		res+=tmp
	res.save(save_name)



