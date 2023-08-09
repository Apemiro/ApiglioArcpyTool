# -*- coding: UTF-8 -*-
# map document tool
import arcpy
import os
import os.path
import math
from feature import to_list

_export_ext_func_ = {"png":arcpy.mapping.ExportToPNG,
					 "jpg":arcpy.mapping.ExportToJPEG,
					 "jpeg":arcpy.mapping.ExportToJPEG,
					 "tif":arcpy.mapping.ExportToTIFF,
					 "tiff":arcpy.mapping.ExportToTIFF,
					 "bmp":arcpy.mapping.ExportToBMP,
					 "pdf":arcpy.mapping.ExportToPDF,
					 "svg":arcpy.mapping.ExportToSVG,
					 "eps":arcpy.mapping.ExportToEPS,
					 "emf":arcpy.mapping.ExportToEMF,
					 "ai":arcpy.mapping.ExportToAI,
					}

def cmxd():
	return arcpy.mapping.MapDocument("CURRENT")

def lyrs():
	return arcpy.mapping.ListLayers(cmxd(),"*")
	
# 类似于数据驱动页面，后期增加新功能
def export_by_features(path,feature,field=None,ext="png",resolution=None):
	fea=to_list(feature)
	fcount=len(fea)
	fields=arcpy.Describe(feature).fields
	field_names=[x.name for x in fields]
	if field in field_names:
		fieldobj=fields[field_names.index(field)]
		filename=to_list(feature,field)
		if fieldobj.type==u'String':
			pass
		elif fieldobj.type in [u'Double', u'Single', u'Integer']:
			filename=[str(x) for x in filename]
		else:
			raise Exception('不支持的命名字段类型。')
	else:
		digit = str(int(math.ceil(math.log10(fcount+1))))
		fmt = "%0"+digit+"d"
		filename=[fmt%x for x in range(fcount)]
	mxd=cmxd()
	dfm=cmxd().activeDataFrame
	if not os.path.exists(path):
		os.makedirs(path)
	for ii in range(fcount):
		dfm.panToExtent(fea[ii].extent)
		_export_ext_func_[ext.lower()](mxd,path+'/'+filename[ii]+"."+ext,resolution=resolution)
	
	
