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
			
	
def iterator(feature_name,method=None,final_result="Iterator_Result"):
	if not callable(method):
		raise Exception("method参数需要是函数")
	tmp_feature="TM_"
	acc=0
	merge_list=[]
	with arcpy.da.UpdateCursor(feature_name,["FID"]) as cursor:
		for row in cursor:
			acc+=1
			tmp_feature_order=tmp_feature+str(acc).zfill(6)
			arcpy.FeatureClassToFeatureClass_conversion(feature_name,"in_memory",tmp_feature_order,'"FID" = '+str(row[0]))
			merge_list.append(method(tmp_feature_order,row[0]))
			arcpy.Delete_management(tmp_feature_order)
			print(acc)
	#arcpy.Delete_management(tmp_feature)
	
	# prj_info=arcpy.Describe(feature_name).spatialReference.exportToString()
	# ngr=arcpy.SpatialReference()
	# ngr.loadFromString(prj_info)
	# arcpy.CreateFeatureclass_management("in_memory","test2",spatial_reference=ngr)
	arcpy.Merge_management(merge_list,final_result)
	for i in merge_list:
		arcpy.Delete_management(i)

	
def tmp_mtd(x,_FID):
	#arcpy.FeatureClassToFeatureClass_conversion(x,"in_memory",target_layer_name)
	visibl_tif=x+"Img"
	arcpy.CreateRasterDataset_management("in_memory",visibl_tif,pixel_type="8_BIT_UNSIGNED")
	arcpy.Visibility_3d(DEM_TIFF,x,visibl_tif,"#","FREQUENCY","ZERO","1","FLAT_EARTH",".13","#","#","#","#","#","#","#","#","#")
	visibl_fac=x+"F"
	arcpy.RasterToPolygon_conversion(visibl_tif,visibl_fac)
	clear_feature(visibl_fac,["Shape@","gridcode"],lambda x:x[1]==0)
	visibl_fac_mul=visibl_fac+"M"
	arcpy.Dissolve_management(visibl_fac,visibl_fac_mul,"#","#","MULTI_PART","DISSOLVE_LINES")
	arcpy.Delete_management(visibl_tif)
	arcpy.Delete_management(visibl_fac)
	arcpy.AddField_management(visibl_fac_mul,"ITERA_ID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","")
	arcpy.CalculateField_management(visibl_fac_mul,"ITERA_ID",_FID,"VB","#")
	return(visibl_fac_mul)
	
arcpy.CreateRasterDataset_management("in_memory","ttt",pixel_type="8_BIT_UNSIGNED")
arcpy.Visibility_3d(DEM_TIFF,OBS_POINT,"in_memory/test","#","FREQUENCY","ZERO","1","FLAT_EARTH",".13","#","#","#","#","#","#","#","#","#")






