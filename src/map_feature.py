# -*- coding: UTF-8 -*-
import arcpy
import numpy
import random
import math
import os.path
import sys

sys.path.append(os.path.split(__file__)[0])
import codetool.df

#method参数的定义如下：
#def method(path_name,in_name,out_name)
#	#...
#	#return(out_name)
def iterator(in_dataset,out_dataset="Iterator_Result",method=None,temp_name="in_memory/TMP",out_format=".shp"):
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
				ds_export=paths[1]+str(acc).zfill(digit)+"_out"+out_format
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
	arcpy.management.Merge(merge_list,paths[0]+'/'+out_dataset+out_format)
	for filename in merge_list:
		arcpy.management.Delete(filename)
	print("done.")

#method_list
#def method_list(path_name,in_name_list,out_name)
#	#...
#	#return(out_name)
def iterator_list(in_dataset_list,out_dataset="Iterator_List_Result",method_list=None,temp_name="in_memory/TMP",out_format=".shp"):
	merge_list=[]
	if not callable(method_list):
		raise Exception("method参数需要是函数")
	paths=list(os.path.split(temp_name))
	if paths[0]=="":
		paths[0]="in_memory"
	print("path= "+paths[0])
	feature_count=None
	dataset_count=len(in_dataset_list)
	for in_dataset in in_dataset_list:
		toto=int(arcpy.management.GetCount(in_dataset).getOutput(0))
		if feature_count==None:
			feature_count=toto
		elif feature_count<>toto:
			raise Exception("in_dataset_list中各要素集中的要素数量不相同。")
	codetool.df.BeginUpdate()
	try:
		acc=0
		digit=int(math.ceil(math.log10(feature_count+1)))
		digit_list=int(math.ceil(math.log10(dataset_count+1)))
		#==这一部分真的有必要吗?
		'''
		fid_values=[]
		for in_dataset in in_dataset_list:
			fid_values.append([])
			with arcpy.da.UpdateCursor(in_dataset,["FID"]) as cursor:
				for row in cursor:
					fid_values[-1].append(row[0])
		fid_values=list(map(list,zip(*fid_values)))
		for compare in fid_values:
			if len(list(set(compare)))<>1:
				raise Exception("FID值不相同。")
		'''
		#========以上部分
		with arcpy.da.UpdateCursor(in_dataset_list[0],["FID"]) as cursor:
			for row in cursor:
				acc+=1
				ds_import_list=[]
				for ds_import_index in range(dataset_count):
					ds_import_list.append(paths[1]+str(acc).zfill(digit)+"_"+str(ds_import_index).zfill(digit_list)+".shp")
				ds_export=paths[1]+str(acc).zfill(digit)+"_out"+out_format
				merge_list.append(paths[0]+'/'+ds_export)
				for indx in range(dataset_count):
					arcpy.conversion.FeatureClassToFeatureClass(in_dataset_list[indx],paths[0],ds_import_list[indx],'"FID" = '+str(row[0]))
				method_list(paths[0],ds_import_list,ds_export)
				for ds_import in ds_import_list:
					arcpy.management.Delete(paths[0]+'/'+ds_import)
				#print("%d/%d"%(acc,feature_count))
	except:
		pass
	finally:
		codetool.df.EndUpdate()
	print("merging...")
	merge_list_str=""
	for filen in merge_list:
		merge_list_str+=filen+";"
	print(merge_list_str[:-1],paths[0]+'/'+out_dataset+out_format)
	arcpy.management.Merge(merge_list_str[:-1],paths[0]+'/'+out_dataset+out_format)
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

def __iter_list_nothing(pathn,inpns,outn):
	ds_list=""
	for inpn in inpns:
		ds_list+=pathn+"/"+inpn+";"
	arcpy.management.Merge(ds_list[:-1],pathn+'/'+outn)
	#print ds_list[:-1]

def iter_list_nothing(in_dataset_list,out_dataset,run_path):
	iterator_list(in_dataset_list,out_dataset,__iter_list_nothing,run_path)













