# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da
import math
import datetime

from random import seed as randomize
from random import random as get_random


def __has_field(dataset,field):
	target_fields = filter(lambda x:x.name==field,arcpy.Describe(dataset).fields)
	return len(target_fields)>=1

def __field_type(dataset,field):
	target_fields = filter(lambda x:x.name==field,arcpy.Describe(dataset).fields)
	return target_fields[0].type

def __geo_type(dataset):
	return arcpy.Describe(dataset).shapeType

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
	
def FieldTypeChanger(dataset, field_name, field_type, field_scale_or_length=0, field_precision=0, change_field_name=None, new_alias=None, delete_bak_field=False):
	'''临时字段最大长度为255，请注意可能存在截断丢失信息的情况。'''
	bak_field_name = (("bak_"+field_name.encode("utf8"))[:10]).decode("utf8") # 为了兼容Shapefile字段限制，全部截断到10字符
	bak_field_size = 255 # 如果字段值更大还会丢失，还可以再加判断
	func_name_options = \
		{\
		"TEXT":str,\
		"FLOAT":float,\
		"DOUBLE":float,\
		"SHORT":lambda x:int(float(x)),\
		"LONG":lambda x:int(float(x)),\
		"DATE":lambda x:datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"),\
		"BLOB":lambda x:x,\
		"RASTER":lambda x:x,\
		"GUID":lambda x:x\
		}
	if field_type.upper() not in func_name_options:
		arcpy.AddError(u"无效的字段类型："%(field_type,))
		raise Exception(u"无效的字段类型："%(field_type,))
	
	try:
		#始终创建文本字段，最大可能保留信息
		arcpy.management.AddField(dataset, bak_field_name, "TEXT", bak_field_size)
	except:
		arcpy.AddError(u"未能成功创建临时字段，字段修改失败。")
		raise Exception(u"未能成功创建临时字段，字段修改失败。")
	
	cursor = arcpy.da.UpdateCursor(dataset, [field_name, bak_field_name])
	for row in cursor:
		row[1] = str(row[0])
		cursor.updateRow(row)
	del cursor
	
	arcpy.management.DeleteField(dataset, field_name)
	
	new_field_name = field_name if change_field_name==None else change_field_name
	
	# 这里创建的字段
	if field_type in ["TEXT", "BLOB"]:
		arcpy.management.AddField(dataset, new_field_name, field_type, field_length=field_scale_or_length, field_alias=new_alias)
	else:
		arcpy.management.AddField(dataset, new_field_name, field_type, field_precision=field_precision, field_scale=field_scale_or_length, field_alias=new_alias)
	func_name = func_name_options[field_type.upper()]
	cursor = arcpy.da.UpdateCursor(dataset, [bak_field_name, new_field_name])
	for row in cursor:
		row[1] = func_name(row[0])
		cursor.updateRow(row)
	del cursor
	if len(arcpy.GetParameterInfo())==0:
		import ctypes
		ctypes.windll.user32.MessageBoxW(0, u"直接在python窗口调用FieldTypeChanger需要在表视图中重新打开修改的数据，否则不会触发更新。", u"表视图未更新", 0x40)
	
	if delete_bak_field:
		arcpy.management.DeleteField(dataset, bak_field_name)
	
	
	
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

def __mean(func,list):
	total = len(list)
	acc = 0.0
	for i in list:
		acc += func(i)
	return acc / total

def __active_df_sr():
	return arcpy.mapping.MapDocument(r"CURRENT").activeDataFrame.spatialReference.exportToString()

def __sr_arg(spatial_reference):
	if spatial_reference == True:
		return arcpy.mapping.MapDocument(r"CURRENT").activeDataFrame.spatialReference.exportToString()
	elif spatial_reference == None:
		return None
	else:
		return spatial_reference

#ContainsCounter('点要素','面要素','面统计字段')
def ContainsCounter(point_dataset,polygon_dataset,counter_field,spatial_reference=True):
	if not __geo_type(point_dataset) == "Point":raise Exception("第1参数不是点要素")
	if not __geo_type(polygon_dataset) == "Polygon":raise Exception("第2参数不是面要素")
	if not __has_field(polygon_dataset,counter_field):raise Exception("第2参数没有目标字段")
	if not __field_type(polygon_dataset,counter_field) == "Integer":raise Exception("目标字段不是整型")
	
	sr = __sr_arg(spatial_reference)
	
	polygons = []
	for row in arcpy.da.SearchCursor(polygon_dataset,["SHAPE@"],spatial_reference=sr):
		polygons.append(row[0])
	del row
	
	min_x = arcpy.Describe(polygon_dataset).extent.XMin
	max_x = arcpy.Describe(polygon_dataset).extent.XMax
	min_y = arcpy.Describe(polygon_dataset).extent.YMin
	max_y = arcpy.Describe(polygon_dataset).extent.YMax
	tot_w = arcpy.Describe(polygon_dataset).extent.width
	tot_h = arcpy.Describe(polygon_dataset).extent.height
	mea_w = __mean(lambda x:x.extent.width,  polygons)
	mea_h = __mean(lambda x:x.extent.height, polygons)
	
	x_index = [set() for i in range(int(math.ceil(float(tot_w) / mea_w))+1)]
	y_index = [set() for i in range(int(math.ceil(float(tot_h) / mea_h))+1)]
	count = len(polygons)
	for row in range(count):
		ext = polygons[row].extent
		x_idx_min = int(math.ceil(float(ext.XMin - min_x) / mea_w))
		x_idx_max = int(math.ceil(float(ext.XMax - min_x) / mea_w))
		y_idx_min = int(math.ceil(float(ext.YMin - min_y) / mea_h))
		y_idx_max = int(math.ceil(float(ext.YMax - min_y) / mea_h))
		for xx in range(x_idx_min, x_idx_max + 1):
			x_index[xx].add(row)
		for yy in range(y_idx_min, y_idx_max + 1):
			y_index[yy].add(row)
	
	point_counts = [0 for i in range(len(polygons))]
	for row in arcpy.da.SearchCursor(point_dataset,["SHAPE@"],spatial_reference=sr):
		if row[0]==None:
			continue
		point_xy = row[0].centroid
		x_idx = int(math.ceil(float(point_xy.X - min_x) / mea_w))
		y_idx = int(math.ceil(float(point_xy.Y - min_y) / mea_h))
		polygons_rough = x_index[x_idx].intersection(y_index[y_idx])
		for polygon_idx in list(polygons_rough):
			if polygons[polygon_idx].contains(row[0]):
				point_counts[polygon_idx]+=1
	del row
	
	cursor=arcpy.da.UpdateCursor(polygon_dataset,[counter_field])
	polygon_idx=0
	for row in cursor:
		row[0]=point_counts[polygon_idx]
		cursor.updateRow(row)
		polygon_idx+=1
	del row,cursor



#utf8_field这个参数名称有点问题
def FieldExtractor(dataset,field_name,utf8_field=True,key=lambda x:x):
	ll=set()
	cursor=arcpy.UpdateCursor(dataset)
	for row in cursor:
		str=row.getValue(field_name.decode("utf8"))
		if not utf8_field:
			str=str.encode("utf8")
		ll.add(str)
	del row,cursor
	return list(ll)


#utf8_field这个参数名称有点问题
def FieldLister(dataset,field_name,utf8_field=True,key=lambda x:x):
	ll=[]
	cursor=arcpy.da.SearchCursor(dataset,[field_name.decode("utf8")])
	for row in cursor:
		str=row[0]
		if not utf8_field:
			str=str.encode("utf8")
		ll.append(key(str))
	del row,cursor
	return ll

def FieldDicter(datatab, key_field, value_field):
	res={}
	cursor = arcpy.da.SearchCursor(datatab,[key_field,value_field])
	for row in cursor:
		res[row[0]]=row[1]
	del row,cursor
	return res

def edge_angle(edge_dataset,field_name):
	with arcpy.da.UpdateCursor(edge_dataset, ["SHAPE@",field_name]) as cursor:
		for row in cursor:
			edge=row[0].getPart()[0]
			if edge[1].X==edge[0].X:
				row[1]=0
			else:
				row[1]=math.atan((edge[1].Y-edge[0].Y)/(edge[1].X-edge[0].X))
			cursor.updateRow(row)
	
	
def XYGenerator(dataset,field_x,field_y,sr=None):
	if sr==None:
		cursor=arcpy.UpdateCursor(dataset)
	else:
		cursor=arcpy.UpdateCursor(dataset,spatial_reference=sr)
	for row in cursor:
		xy=row.getValue("Shape").centroid
		row.setValue(field_x.decode("utf8"),xy.X)
		row.setValue(field_y.decode("utf8"),xy.Y)
		cursor.updateRow(row)
	del row,cursor

#在照片转出的点要素基础上在targetpath目录中生成一个bat文件
#运行bat文件可以将选中的图片点要素照片硬连接到此处
def HardLinkGenerator(dataset,targetpath):
	fields = arcpy.Describe(dataset).fields
	field_names = list(map(lambda x:x.name,fields))
	path_field_id = field_names.index("Path")
	name_field_id = field_names.index("Name")
	# 没有以上两个字段会报错
	batch_here = targetpath+"/"+"_start_hard_link_.bat"
	fout = open(batch_here,"w")
	fout.write("setlocal")
	cursor = arcpy.da.SearchCursor(dataset,["Path","Name"])
	for row in cursor:
		path_value = row[0]
		name_value = row[1]
		command = "mklink /H \""+name_value.encode("cp936")+"\" \""+path_value.encode("cp936")+"\"\n"
		fout.write(command)
	del row,cursor
	fout.write("echo "+u"硬连接已完成。".encode("cp936")+"\n")
	fout.write("pause")
	fout.close()


def random_field_values(dataset, field_name, rand_value_func=lambda x:x*2.0-1.0):
	fields = arcpy.Describe(dataset).fields
	field_names = [x.name for x in fields]
	field_types = [x.type for x in fields]
	try:
		field_index = field_names.index(field_name)
	except:
		raise Exception("Field %s is not found"%(field_name,))
	if not field_types[field_index] in ['Double', 'Single']:
		raise Exception("Invalid field type %s is found"%(field_types[field_index],))
	with arcpy.da.UpdateCursor(dataset, [field_name]) as cursor:
		for row in cursor:
			row = [rand_value_func(get_random())]
			cursor.updateRow(row)




