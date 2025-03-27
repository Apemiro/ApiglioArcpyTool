# -*- coding: UTF-8 -*-
# map document tool
import arcpy
import os
import os.path
import math
from feature import to_list
from feature import to_dict

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
	

def __extent_scale(ext, factor):
	wInc = factor * (ext.XMax - ext.XMin)
	hInc = factor * (ext.YMax - ext.YMin)
	return arcpy.Extent( \
		ext.XMin - wInc, ext.YMin - hInc, \
		ext.XMax + wInc, ext.YMax + hInc, \
		ext.ZMin, ext.ZMax, \
		ext.MMin, ext.MMax \
	)

# 类似于数据驱动页面，将图层设置为透明，再设置选中图元的符号类型，此函数会依次缩放至图元、将其选中并导出
# 数据框长宽比大于1.05时，根据要素长宽比旋转数据框视图角度
def export_by_layer_selection(path, layer, identical_field=None, ext="png", resolution=None, scale_factor=0.0):
	fea = to_dict(layer.dataSource)
	fcount = len(fea)
	index_field = arcpy.Describe(layer.dataSource).fields[0].name
	mxd=cmxd()
	dfm=cmxd().activeDataFrame
	dfm_ratio = dfm.elementWidth / dfm.elementHeight
	dfm_rotation_origin = dfm.rotation
	if not os.path.exists(path):
		os.makedirs(path)
	for ii in range(fcount):
		filename = fea[ii].get(identical_field)
		if filename==None:
			filename = fea[ii][index_field]
		layer.setSelectionSet("NEW",[fea[ii][index_field]])
		extent_feature = fea[ii]["SHAPE@"].extent
		feature_ratio = extent_feature.width / extent_feature.height
		if feature_ratio>1.05 and dfm_ratio<1.05:
			dfm.rotation = -90
		elif feature_ratio<1.05 and dfm_ratio>1.05:
			dfm.rotation = -90
		else:
			dfm.rotation = 0
		extent_view = __extent_scale(extent_feature, scale_factor)
		#dfm.panToExtent(extent_view)
		dfm.extent = extent_view
		dfm.name = filename
		_export_ext_func_[ext.lower()](mxd,path+'/'+filename+"."+ext,resolution=resolution)
	dfm.rotation = dfm_rotation_origin
	
