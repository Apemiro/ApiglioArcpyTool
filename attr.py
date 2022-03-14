# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da




#utf8_field这个参数名称有点问题
def FieldStringReplace(dataset,field_name,old_pattern,new_pattern,utf8_field=True):
	cursor=arcpy.UpdateCursor(dataset)
	old_pattern=old_pattern.decode("utf8")
	new_pattern=new_pattern.decode("utf8")
	for row in cursor:
		str=row.getValue(field_name.decode("utf8"))
		if not utf8_field:
			str=str.encode("utf8")
		str2=str.replace(old_pattern,new_pattern)
		if not utf8_field:
			str2=str2.decode("utf8")
		if str!=str2:
			print(str+'  ->  '+str2)
		row.setValue(field_name.decode("utf8"),str2)
		cursor.updateRow(row)
	del row,cursor
	
	
# TEXT —名称或其他文本特性。 
# FLOAT —特定范围内含小数值的数值。 
# DOUBLE —特定范围内含小数值的数值。 
# SHORT —特定范围内不含小数值的数值；编码值。 
# LONG —特定范围内不含小数值的数值。 
# DATE —日期和/或时间。 
# BLOB —影像或其他多媒体。 
# RASTER —栅格影像。 
# GUID —GUID 值 

	
def FieldUpdater(dataset,field_name,rule=lambda x:x):
	cursor=arcpy.UpdateCursor(dataset)
	for row in cursor:
		value=row.getValue(field_name.decode("utf8"))
		new_value=rule(value)
		row.setValue(field_name.decode("utf8"),new_value)
		cursor.updateRow(row)
	del row,cursor
	
def FieldTypeChanger(dataset,field_name,field_type,field_precision=0,field_scale=0):
	arcpy.AddField_management(dataset, field_name+"_", field_type, field_precision, field_scale, field_scale)
	func_name={"TEXT":"str","FLOAT":"float","DOUBLE":"float","SHORT":"int","LONG":"long","DATE":"","BLOB":"","RASTER":"","GUID":""}
	arcpy.CalculateField_management(dataset, field_name+"_", func_name[field_type.upper()]+"( !"+field_name+"! )", "PYTHON_9.3", "#")
	arcpy.DeleteField_management(dataset,field_name)
	arcpy.AddField_management(dataset, field_name, field_type, field_precision, field_scale, field_scale)
	arcpy.CalculateField_management(dataset, field_name, "!"+field_name+"_!", "PYTHON_9.3", "#")
	arcpy.DeleteField_management(dataset,field_name+"_")
	
	
	
def FieldDefiner(dataset,field_name,value):
	cursor=arcpy.UpdateCursor(dataset)
	for row in cursor:
		row.setValue(field_name.decode("utf8"),value)
		cursor.updateRow(row)
	del row,cursor
	
	
#判断iden_dataset(点数据)分别能够被纳入多少个region_dataset中的面域内。符合条件的FID结果记录在record_field中，以逗号隔开。
#ContainsRecorder('待识别要素','文本字段','面要素','面ID')
def ContainsRecorder(iden_dataset,record_field,region_dataset,idenitiy_field):
	regions=[]
	for row in arcpy.da.SearchCursor(region_dataset,[idenitiy_field,"SHAPE@"]):
		regions.append(row)
	del row
	try:
		cursor=arcpy.da.UpdateCursor(iden_dataset,["SHAPE@",record_field.decode("utf8")])
	except:
		cursor=arcpy.da.UpdateCursor(iden_dataset,["SHAPE@",record_field])
	for row in cursor:
		comma=','
		for region in regions:
			if region[1].contains(row[0]):
				comma+=str(region[0])+','
		row[1]=comma
		cursor.updateRow(row)
	del row,cursor
	
	
	
#utf8_field这个参数名称有点问题
def FieldExtractor(dataset,field_name,utf8_field=True):
	ll=set()
	cursor=arcpy.UpdateCursor(dataset)
	for row in cursor:
		str=row.getValue(field_name.decode("utf8"))
		if not utf8_field:
			str=str.encode("utf8")
		ll.add(str)
	del row,cursor
	return list(ll)
	
	
import math
def edge_angle(edge_dataset,field_name):
	with arcpy.da.UpdateCursor(edge_dataset, ["SHAPE@",field_name]) as cursor:
		for row in cursor:
			edge=row[0].getPart()[0]
			if edge[1].X==edge[0].X:
				row[1]=0
			else:
				row[1]=math.atan((edge[1].Y-edge[0].Y)/(edge[1].X-edge[0].X))
			cursor.updateRow(row)
	
	
	
	