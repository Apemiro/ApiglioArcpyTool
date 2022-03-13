# -*- coding: UTF-8 -*-
import arcpy
import numpy
import random

#clear_feature("Test_Point2",["Shape@","Str"],lambda x:x[1]=="aaaaaaaaaa")
def clear_feature(feature_name,fields=["Shape@"],criterion=lambda x:True):
	with arcpy.da.UpdateCursor(feature_name,fields) as cursor:
		for row in cursor:
			if criterion(row):
				cursor.deleteRow()
			
	
def iterator(feature_name,method=None,final_result="Iterator_Result",temp_name="TMP"):
	if not callable(method):
		raise Exception("method参数需要是函数")
	tmp_feature=temp_name
	toto=int(arcpy.GetCount_management(feature_name).getOutput(0))
	acc=0
	merge_list=[]
	with arcpy.da.UpdateCursor(feature_name,["FID"]) as cursor:
		for row in cursor:
			acc+=1
			tmp_feature_order=tmp_feature+str(acc).zfill(6)
			arcpy.FeatureClassToFeatureClass_conversion(feature_name,"in_memory",tmp_feature_order,'"FID" = '+str(row[0]))
			merge_list.append(method(tmp_feature_order,row[0]))
			arcpy.DeleteFeatures_management(tmp_feature_order)
			arcpy.Delete_management(tmp_feature_order)
			print("%d/%d"%(acc,toto))
	#arcpy.Delete_management(tmp_feature)
	
	# prj_info=arcpy.Describe(feature_name).spatialReference.exportToString()
	# ngr=arcpy.SpatialReference()
	# ngr.loadFromString(prj_info)
	# arcpy.CreateFeatureclass_management("in_memory","test2",spatial_reference=ngr)
	print("merging...")
	arcpy.Merge_management(merge_list,final_result)
	for i in merge_list:
		arcpy.DeleteFeatures_management(i)
		arcpy.Delete_management(i)
	print("done.")
	
def visibility_mtd(x,_FID):
	#arcpy.FeatureClassToFeatureClass_conversion(x,"in_memory",target_layer_name)
	visibl_tif=x+"Img"
	arcpy.CreateRasterDataset_management("in_memory",visibl_tif,pixel_type="8_BIT_UNSIGNED")
	arcpy.Visibility_3d(_DEM_TIFF_,x,visibl_tif,"#","FREQUENCY","ZERO","1","FLAT_EARTH",".13","#","#","#","#","#","#","#","#","#")
	#视高还解决不了
	visibl_fac=x+"F"
	arcpy.RasterToPolygon_conversion(visibl_tif,visibl_fac)
	clear_feature(visibl_fac,["Shape@","gridcode"],lambda x:x[1]==0)
	visibl_fac_mul=visibl_fac+"M"
	arcpy.Dissolve_management(visibl_fac,visibl_fac_mul,"#","#","MULTI_PART","DISSOLVE_LINES")
	#arcpy.DeleteFeatures_management(visibl_tif)
	arcpy.DeleteFeatures_management(visibl_fac)
	arcpy.Delete_management(visibl_tif)
	arcpy.Delete_management(visibl_fac)
	arcpy.AddField_management(visibl_fac_mul,"ITERA_ID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","")
	arcpy.CalculateField_management(visibl_fac_mul,"ITERA_ID",_FID,"VB","#")
	return(visibl_fac_mul)

#批量生成Nodes数据集中每一个点在DEM_TIFF中的视域范围
#内存没删干净，后续处理
def Visibility_Iterator(dem_data,Nodes,out_data,tmp_name="TMP"):
	global _DEM_TIFF_
	_DEM_TIFF_= dem_data
	iterator(Nodes,visibility_mtd,out_data,tmp_name)

