# -*- coding: UTF-8 -*-
import arcpy
import numpy
import random
import math
import os.path
import sys

sys.path.append(os.path.split(__file__)[0])
import codetool.df


#clear_feature("Test_Point2",["Shape@","Str"],lambda x:x[1]=="aaaaaaaaaa")
def clear_feature(feature_name,fields=["Shape@"],criterion=lambda x:True):
	with arcpy.da.UpdateCursor(feature_name,fields) as cursor:
		for row in cursor:
			if criterion(row):
				cursor.deleteRow()


#method参数的定义如下：
#def method(path_name,in_name,out_name)
#	#...
#	#return(out_name)
def iterator(in_dataset,out_dataset="Iterator_Result",method=None,temp_name="TMP"):
	merge_list=[]
	if not callable(method):
		raise Exception("method参数需要是函数")
	paths=list(os.path.split(temp_name))
	if paths[0]=="":
		paths[0]="in_memory"
	toto=int(arcpy.management.GetCount(in_dataset).getOutput(0))
	#shapetype=arcpy.Describe(in_dataset).shapetype
	codetool.df.BeginUpdate()
	try:
		acc=0
		digit=int(math.ceil(math.log10(toto+1)))
		with arcpy.da.UpdateCursor(in_dataset,["FID"]) as cursor:
			for row in cursor:
				acc+=1
				ds_import=paths[1]+str(acc).zfill(digit)+".shp"
				ds_export=paths[1]+str(acc).zfill(digit)+"_out.shp"
				merge_list.append(paths[0]+'/'+ds_export)
				arcpy.conversion.FeatureClassToFeatureClass(in_dataset,paths[0],ds_import,'"FID" = '+str(row[0]))
				method(paths[0],ds_import,ds_export)
				arcpy.management.Delete(paths[0]+'/'+ds_import)
				#print("%d/%d"%(acc,toto))
	except:
		pass
	finally:
		codetool.df.EndUpdate()
	print("merging...")
	arcpy.management.Merge(merge_list,paths[0]+'/'+out_dataset+'.shp')
	for filename in merge_list:
		arcpy.management.Delete(filename)
	print("done.")
	
def visibility_mtd(pathn,inpn,outn):
	#arcpy.FeatureClassToFeatureClass_conversion(inpn,pathn,target_layer_name)
	visibl_tif=inpn+"Img"
	arcpy.CreateRasterDataset_management(pathn,visibl_tif,pixel_type="8_BIT_UNSIGNED")
	arcpy.Visibility_3d(_DEM_TIFF_,inpn,visibl_tif,"#","FREQUENCY","ZERO","1","FLAT_EARTH",".13","#","#","#","#","#","#","#","#","#")
	#视高还解决不了
	visibl_fac=inpn+"F"
	arcpy.RasterToPolygon_conversion(visibl_tif,visibl_fac)
	clear_feature(visibl_fac,["Shape@","gridcode"],lambda x:x[1]==0)
	visibl_fac_mul=visibl_fac+"M"
	arcpy.Dissolve_management(visibl_fac,visibl_fac_mul,"#","#","MULTI_PART","DISSOLVE_LINES")
	#arcpy.DeleteFeatures_management(visibl_tif)
	arcpy.DeleteFeatures_management(visibl_fac)
	arcpy.Delete_management(visibl_tif)
	arcpy.Delete_management(visibl_fac)
	arcpy.AddField_management(visibl_fac_mul,"ITERA_ID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","")
	arcpy.CalculateField_management(visibl_fac_mul,"ITERA_ID",outn,"VB","#")
	return(visibl_fac_mul)

#批量生成Nodes数据集中每一个点在DEM_TIFF中的视域范围
#内存没删干净，后续处理
def Visibility_Iterator(dem_data,Nodes,out_data,tmp_name="TMP"):
	global _DEM_TIFF_
	_DEM_TIFF_= dem_data
	iterator(Nodes,out_data,visibility_mtd,tmp_name)

def __iter__nothing(pathn,inpn,outn):
	#print(pathn+'/'+inpn,pathn,outn)
	arcpy.conversion.FeatureClassToFeatureClass(pathn+'/'+inpn,pathn,outn)

def iter_nothing(in_dataset,out_dataset,run_path):
	iterator(in_dataset,out_dataset,__iter__nothing,run_path)