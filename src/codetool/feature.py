# -*- coding: UTF-8 -*-
# 根据图层返回集合列表

import arcpy

def __active_df_sr():
	return arcpy.mapping.MapDocument(r"CURRENT").activeDataFrame.spatialReference.exportToString()

def __sr_arg(spatial_reference):
	if spatial_reference == True:
		return arcpy.mapping.MapDocument(r"CURRENT").activeDataFrame.spatialReference.exportToString()
	elif spatial_reference == None:
		return None
	else:
		return spatial_reference

def to_list(dataset,field="SHAPE@",key=None):
	res=[]
	cursor=arcpy.da.SearchCursor(dataset,[field],spatial_reference=__active_df_sr())
	if key==None:
		key = lambda x:x
	for row in cursor:
		res.append(key(row[0]))
	del row,cursor
	return res

def to_set(dataset,field="SHAPE@",key=None):
	res=set()
	cursor=arcpy.da.SearchCursor(dataset,[field],spatial_reference=__active_df_sr())
	if key==None:
		key = lambda x:x
	for row in cursor:
		res.add(key(row[0]))
	del row,cursor
	return res

def to_dict(dataset,field="SHAPE@"):
	res=[]
	fields = arcpy.Describe(dataset).fields
	field_names = list(map(lambda x:x.name,fields))
	field_count = len(fields)
	cursor = arcpy.da.SearchCursor(dataset, field_names+["SHAPE@"], spatial_reference=__active_df_sr())
	for row in cursor:
		res.append({})
		for fs in range(field_count):
			res[-1][field_names[fs]]=row[fs]
		res[-1]["SHAPE@"]=row[field_count]
	del row,cursor
	return res

def shape_to_feature(geo,name,path="in_memory"):
	if geo.__class__ in [arcpy.PointGeometry, arcpy.Point, arcpy.Polyline, arcpy.Polygon]:
		pass
	else:
		raise Exception("无效的图形参数")
	if geo.firstPoint.Z != None:
		zz="Enabled"
	else:
		zz="Disabled"
	if geo.firstPoint.M != None:
		mm="Enabled"
	else:
		mm="Disabled"
	arcpy.management.CreateFeatureclass(path,name,geo.type.upper(),spatial_reference=geo.spatialReference,has_z=zz,has_m=mm)
	cursor=arcpy.da.InsertCursor(path+'/'+name,["SHAPE@"])
	cursor.insertRow([geo])
	del cursor

def to_file(list_of_geometry,dataset="temp_list_export",path="in_memory",spatial_reference=None):
	ty = list_of_geometry[0].type.upper()
	sr = __sr_arg(spatial_reference)
	hz = "Disabled" if list_of_geometry[0].firstPoint.Z == None else "Enabled"
	hm = "Disabled" if list_of_geometry[0].firstPoint.M == None else "Enabled"
	arcpy.management.CreateFeatureclass(path,dataset,ty,spatial_reference=sr,has_z=hz,has_m=hm)
	with arcpy.da.InsertCursor(path+"/"+dataset,["SHAPE@"]) as cursor:
		for shape in list_of_geometry:
			cursor.insertRow([shape])

def dict_to_file(list_of_dict,dataset="temp_listdict_export",path="in_memory",spatial_reference=None,sorted_field_list=None):
	#fields = []
	#fields_type = []
	field_infos = []
	fields_set = set([])
	for fea in list_of_dict:
		for fd in fea.keys():
			if not fd in fields_set:
				fields_set.add(fd)
				#fields.append(fd)
				#fields_type.append(type(fea[fd]))
				field_infos.append({"name":fd,"type":type(fea[fd])})
	
	# 检查第一行是否有图形字段
	first_one = list_of_dict[0]
	if not "SHAPE@" in first_one.keys():
		raise Exception(u"没有图形字段")
	ty = first_one["SHAPE@"].type.upper()
	sr = __sr_arg(spatial_reference)
	hz = "Disabled" if first_one["SHAPE@"].firstPoint.Z == None else "Enabled"
	hm = "Disabled" if first_one["SHAPE@"].firstPoint.M == None else "Enabled"
	arcpy.management.CreateFeatureclass(path,dataset,ty,spatial_reference=sr,has_z=hz,has_m=hm)
	try:
		geo_index = [x["name"] for x in field_infos].index("SHAPE@")
		field_infos.pop(geo_index)
	except:
		print("SHAPE@字段缺失")
	try:
		geo_index = [x["name"] for x in field_infos].index("Shape")
		field_infos.pop(geo_index)
	except:
		print("Shape字段缺失")
	field_infos.sort(key=lambda x:x["name"])
	# 如果名称在排序列表里，则放到最前，并排序
	if sorted_field_list != None:
		not_in_list = len(sorted_field_list)
		field_infos.sort(key=lambda x:sorted_field_list.index(x["name"]) if x["name"] in sorted_field_list else not_in_list)
	
	# 创建字段并排除类型不满足要求的字段
	fields_valid = []
	fields_index = {}
	row_template = []
	for idx in range(len(field_infos)):
		#field_name = fields[idx]
		#field_type = fields_type[idx]
		field_name = field_infos[idx]["name"]
		field_type = field_infos[idx]["type"]
		if field_type in [int]:
			arcpy.management.AddField(dataset,field_name,"LONG")
			fields_valid.append(field_name)
			row_template.append(0)
			fields_index[field_name] = len(fields_valid)
		elif field_type in [float]:
			arcpy.management.AddField(dataset,field_name,"DOUBLE")
			fields_valid.append(field_name)
			row_template.append(0.0)
			fields_index[field_name] = len(fields_valid)
		elif field_type in [str, unicode]:
			arcpy.management.AddField(dataset,field_name,"TEXT",field_length=255)
			fields_valid.append(field_name)
			row_template.append("")
			fields_index[field_name] = len(fields_valid)
		else:
			print(u"其中的“"+field_name+u"”字段不符合数据类型要求，未保存。")
	
	# 编辑
	row_template = [None] + row_template
	cursor = arcpy.da.InsertCursor(dataset, ["SHAPE@"]+fields_valid)
	for fea in list_of_dict:
		row=list(row_template)
		row[0]=fea["SHAPE@"]
		for key in fea.keys():
			index = fields_index.get(key)
			if index != None:
				row[index] = fea[key]
		cursor.insertRow(row)
	del cursor
	
	

#clear_feature("Test_Point2",["Shape@","Str"],lambda x:x[1]=="aaaaaaaaaa")
def clear_feature(feature_name,fields=["Shape@"],criterion=lambda x:True):
	with arcpy.da.UpdateCursor(feature_name,fields) as cursor:
		for row in cursor:
			if criterion(row):
				cursor.deleteRow()

def select_feature(in_feature,out_feature,fields=["Shape@"],criterion=lambda x:False):
	arcpy.management.CopyFeatures(in_feature,out_feature)
	clear_feature(out_feature,fields,criterion)


#apiglio.src.codetool.feature.listdict_to_line([{"x1":110.2,"y1":34.4,"x2":111.23,"y2":36.32,"testf":"d3wd"}],"x1","y1","x2","y2")
#apiglio.src.codetool.feature.listdict_to_line(part_of,"subject_lng","subject_lat","object_lng","object_lat")
def listdict_to_line(list_of_dictionary,x1,y1,x2,y2,dataset="temp_listdict_line_export",path="in_memory"):
	example=list_of_dictionary[0]
	example_key=example.keys()
	try:
		example_key.index(x1)
		example_key.index(x2)
		example_key.index(y1)
		example_key.index(y2)
	except:
		raise Exception("one of x1,y1,x2,y2 field not found.")
	filtered_fields=list(set(example_key)-set([x1,y1,x2,y2]))
	arcpy.management.CreateFeatureclass(path,dataset,"POLYLINE")
	output_edges = path + "/" + dataset
	for field in filtered_fields:
		arcpy.management.AddField(output_edges, field, "TEXT",field_length=100)
	with arcpy.da.InsertCursor(path+"/"+dataset,["SHAPE@"]+filtered_fields) as cursor:
		for dict_element in list_of_dictionary:
			coord_x1 = dict_element[x1]
			coord_y1 = dict_element[y1]
			coord_x2 = dict_element[x2]
			coord_y2 = dict_element[y2]
			p1 = arcpy.Point(coord_x1,coord_y1)
			p2 = arcpy.Point(coord_x2,coord_y2)
			line = arcpy.Polyline(arcpy.Array([p1,p2]))
			rows = [line]
			for field in filtered_fields:
				rows.append(dict_element[field])
			cursor.insertRow(rows)




