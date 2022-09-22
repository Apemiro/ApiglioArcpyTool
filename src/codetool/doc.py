# -*- coding: UTF-8 -*-
# map document tool
import arcpy
import os
import os.path
import math
from feature import to_list


def cmxd():
	return arcpy.mapping.MapDocument("CURRENT")

def lyrs():
	return arcpy.mapping.ListLayers(cmxd(),"*")
	
def export_by_features(path,feature,field=None):
	fea=to_list(feature)
	fcount=len(fea)
	fields=set(map(lambda x:x.name,arcpy.Describe(feature).fields))
	if field in fields:
		filename=to_list(feature,field)
	else:
		filename=list(map(lambda x:str(x).zfill(int(math.ceil(math.log10(fcount+1)))),range(fcount)))
	mxd=cmxd()
	dfm=cmxd().activeDataFrame
	if not os.path.exists(path):
		os.makedirs(path)
	for ii in range(fcount):
		dfm.panToExtent(fea[ii].extent)
		arcpy.mapping.ExportToPNG(mxd,path+'/'+str(filename[ii])+".png")
	
	
