# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da
import os
import os.path
import scipy.spatial


#Adjacent2GeoNetwork(0,0,"F:/temp/test.txt",0)

def list_select(list,key):
	tmp_list=list[:]
	index=0
	while index<len(tmp_list):
		if key(tmp_list[index]):
			index+=1
		else:
			tmp_list.pop(index)
	return tmp_list

#criterion为匿名函数
#Adjacent2GeoNetwork("HouseJC","社群",'f:/temp/szk.txt',"inner_net_300",300,lambda x,y:x.find(str(y))>=0)
#Adjacent2GeoNetwork("vills_prj_market","markets",list(numpy.identity(812)),"market_edges",0,lambda x,y:x.find(","+str(y)+",")>=0)
def Adjacent2GeoNetwork(nodes,id_field,adjacent_matrix,output_edges,max_dist=0,criterion=lambda x,y:x==y,in_memory=True):
	if type(adjacent_matrix)==str or type(adjacent_matrix)==unicode:
		#读取邻接矩阵txt文件
		mat_f = open(adjacent_matrix, "r+")
		mat_str = mat_f.read()
		mat_res=[]
		for ii in mat_str.split("\n"):
			mat_res.append(ii.split(","))
		mat_f.close()
		max_rows=len(mat_res)
	else:
		if type(adjacent_matrix)==list:
			mat_res=adjacent_matrix[:]
		else:
			raise Exception("adjacent_matrix参数必须是列表。")
	
	#获取节点坐标，保存在列表中
	positions=[]
	for row in arcpy.da.SearchCursor(nodes,[id_field,"SHAPE@XY"]):
		positions.append(row)
	del row
	
	#新建网络output_edges
	if in_memory:
		feature_class=arcpy.CreateFeatureclass_management("in_memory", output_edges, "POLYLINE")[0]
	else:
		fs=os.path.split(output_edges)
		feature_class=arcpy.CreateFeatureclass_management(fs[0], fs[1], "POLYLINE")[0]
	
	arcpy.AddField_management(output_edges, "weight", "DOUBLE")
	arcpy.AddField_management(output_edges, "node_1", "LONG")
	arcpy.AddField_management(output_edges, "node_2", "LONG")
	print("adjacent matrix=\n{}".format([mat_res]))
	
	#绘制边线
	for i in range(0,len(mat_res)):
		mat_row=mat_res[i]
		pis=list_select(positions,lambda x:criterion(x[0],i))
		for j in range(0,len(mat_row)):
			if mat_row[j]==0:
				#print("skip")
				continue
			pjs=list_select(positions,lambda x:criterion(x[0],j))
			for pix in pis:
				for pjx in pjs:
					pi=pix[1]
					pj=pjx[1]
					_from=arcpy.Point(pi[0],pi[1])
					_to=arcpy.Point(pj[0],pj[1])
					arr = arcpy.Array([_from,_to])
					polyline = arcpy.Polyline(arr)
					if max_dist==0 or polyline.length<=max_dist:
						cursor = arcpy.da.InsertCursor(output_edges, ["SHAPE@","weight","node_1","node_2"])
						cursor.insertRow([polyline,mat_row[j],i,j])


def GenGeoNetworkByLength(nodes,output_edges,max_dist,in_memory=True):

	#获取节点坐标，保存在列表中
	positions=[]
	for row in arcpy.da.SearchCursor(nodes,["SHAPE@XY"]):
		positions.append(row[0])
	del row
	
	#新建网络output_edges
	sr=arcpy.Describe(nodes).SpatialReference.ExportToString()
	if in_memory:
		feature_class=arcpy.management.CreateFeatureclass("in_memory", output_edges, "POLYLINE",spatial_reference=sr)[0]
	else:
		fs=os.path.split(output_edges)
		feature_class=arcpy.management.CreateFeatureclass(fs[0], fs[1], "POLYLINE",spatial_reference=sr)[0]
	
	arcpy.management.AddField(output_edges, "node_1", "LONG")
	arcpy.management.AddField(output_edges, "node_2", "LONG")
	arcpy.management.AddField(output_edges, "length", "DOUBLE")
	
	#绘制边线
	points_count = len(positions)
	for i in range(points_count):
		for j in range(points_count):
			if i==j:
				continue
			pi = arcpy.Point(positions[i][0],positions[i][1])
			pj = arcpy.Point(positions[j][0],positions[j][1])
			arr = arcpy.Array([pi,pj])
			polyline = arcpy.Polyline(arr)
			plen = polyline.length
			if max_dist==0 or plen<=max_dist:
				cursor = arcpy.da.InsertCursor(output_edges, ["SHAPE@","node_1","node_2","length"])
				cursor.insertRow([polyline,i,j,plen])

def GenGeoNetworkByValue(nodes,output_edges,valfield,in_memory=True):

	#获取节点坐标，保存在列表中
	positions=[]
	for row in arcpy.da.SearchCursor(nodes,["SHAPE@XY",valfield]):
		positions.append(row[0:2])
	del row
	
	#新建网络output_edges
	sr=arcpy.Describe(nodes).SpatialReference.ExportToString()
	if in_memory:
		feature_class=arcpy.management.CreateFeatureclass("in_memory", output_edges, "POLYLINE",spatial_reference=sr)[0]
	else:
		fs=os.path.split(output_edges)
		feature_class=arcpy.management.CreateFeatureclass(fs[0], fs[1], "POLYLINE",spatial_reference=sr)[0]
	fs=list(filter(lambda x:x.name==valfield,arcpy.Describe(nodes).fields))
	if fs==[]:
		raise Exception("找不到字段"+valfield)
	else:
		fieldtype=fs[0].type
	
	
	arcpy.management.AddField(output_edges, "node_1", "LONG")
	arcpy.management.AddField(output_edges, "node_2", "LONG")
	arcpy.management.AddField(output_edges, valfield, fieldtype)
	
	#绘制边线
	points_count = len(positions)
	for i in range(points_count):
		for j in range(points_count):
			if i==j or positions[i][1]<>positions[j][1]:
				continue
			pi = arcpy.Point(positions[i][0][0],positions[i][0][1])
			pj = arcpy.Point(positions[j][0][0],positions[j][0][1])
			val = positions[i][1]
			arr = arcpy.Array([pi,pj])
			polyline = arcpy.Polyline(arr)
			cursor = arcpy.da.InsertCursor(output_edges, ["SHAPE@","node_1","node_2",valfield])
			cursor.insertRow([polyline,i,j,val])




def Bipartite(dataset_1,dataset_2,output_edges,fields_1=[],fields_2=[],criterion=lambda fs1,fs2,pl:True,field_calc=lambda fs1,fs2:0.0,in_memory=True):
	#获取节点坐标，保存在列表中
	id_field_1=arcpy.ListFields(dataset_1)[0].name
	id_field_2=arcpy.ListFields(dataset_2)[0].name
	pos_1=[]
	for row in arcpy.da.SearchCursor(dataset_1,[id_field_1,"SHAPE@"]+fields_1):
		pos_1.append(row)
	del row
	pos_2=[]
	for row in arcpy.da.SearchCursor(dataset_2,[id_field_2,"SHAPE@"]+fields_2):
		pos_2.append(row)
	del row
	
	#新建网络output_edges
	if in_memory:
		feature_class=arcpy.CreateFeatureclass_management("in_memory", output_edges, "POLYLINE",has_z="ENABLED",has_m="ENABLED")[0]
	else:
		fs=os.path.split(output_edges)
		feature_class=arcpy.CreateFeatureclass_management(fs[0], fs[1], "POLYLINE",has_z="ENABLED",has_m="ENABLED")[0]
	arcpy.AddField_management(output_edges, "length", "DOUBLE")
	arcpy.AddField_management(output_edges, "node_1", "LONG")
	arcpy.AddField_management(output_edges, "node_2", "LONG")
	arcpy.AddField_management(output_edges, "calc", "DOUBLE")
	
	for r1 in pos_1:
		id_1=r1[0]
		po_1=r1[1].firstPoint
		for r2 in pos_2:
			id_2=r2[0]
			po_2=r2[1].firstPoint
			_from=arcpy.Point(po_1.X,po_1.Y,po_1.Z,po_1.M)
			_to=arcpy.Point(po_2.X,po_2.Y,po_2.Z,po_2.M)
			#print(po_1,po_2)
			arr = arcpy.Array([_from,_to])
			polyline = arcpy.Polyline(arr)
			if criterion(r1[2:],r2[2:],polyline):
				cursor = arcpy.da.InsertCursor(output_edges, ["SHAPE@","length","node_1","node_2","calc"])
				cursor.insertRow([polyline,polyline.length,id_1,id_2,field_calc(r1[2:],r2[2:])])

def Delaunay(node_dataset,id_field,out_face_dataset,vertice_type="SET",in_memory=True):
	pts = []
	ids = []
	for row in arcpy.da.SearchCursor(node_dataset,["SHAPE@",id_field]):
		pos = row[0].firstPoint
		pts.append([pos.X,pos.Y])
		ids.append(row[1])
	del row
	dly = scipy.spatial.Delaunay(pts)
	polygons = dly.simplices
	pgs = [arcpy.Polygon(arcpy.Array([arcpy.Point(*pts[x]) for x in simp])) for simp in polygons]
	idf = [set([ids[x] for x in simp]) for simp in polygons]
	
	sr = arcpy.Describe(node_dataset).SpatialReference.ExportToString()
	if in_memory:
		feature_class = arcpy.management.CreateFeatureclass("in_memory", out_face_dataset, "POLYGON",spatial_reference=sr)[0]
	else:
		fs=os.path.split(out_face_dataset)
		feature_class = arcpy.management.CreateFeatureclass(fs[0], fs[1], "POLYGON",spatial_reference=sr)[0]
	
	if vertice_type.lower()=="set":
		arcpy.AddField_management(out_face_dataset, "vertices", "TEXT", 255)
		cursor = arcpy.da.InsertCursor(out_face_dataset, ["SHAPE@","vertices"])
		for index in range(len(pgs)):
			f = pgs[index]
			s = idf[index]
			cursor.insertRow([f,str(s)])
	else:
		arcpy.AddField_management(out_face_dataset, "vert_1", "LONG")
		arcpy.AddField_management(out_face_dataset, "vert_2", "LONG")
		arcpy.AddField_management(out_face_dataset, "vert_3", "LONG")
		cursor = arcpy.da.InsertCursor(out_face_dataset, ["SHAPE@","vert_1","vert_2","vert_3"])
		for index in range(len(pgs)):
			f = pgs[index]
			s = list(idf[index])
			cursor.insertRow([f]+s)


#在Delaunay三角形vertices字段的基础上统计类型
#class_dict = {1:1, 2:1, 3:2, 4:2, 5:1, 6:3 ... }
#key默认参数意义：端点值一致时返回1，否则返回0
def Delaunay_stat(delaunay_dataset,vertices_field,stat_field,class_dict,key=lambda s,d:int(all([d.get(x)==d.get(list(s)[0]) for x in s]))):
	cursor = arcpy.da.UpdateCursor(delaunay_dataset,[vertices_field,stat_field])
	for row in cursor:
		verts  = eval(row[0])
		row[1] = key(verts,class_dict)
		cursor.updateRow(row)
	del row, cursor





def CostDistPath(nodes,cost_raster,out_edges):
	arcpy.gp.PathDistance_sa("NetTest/vills_prj","F:/_UrbanPlanning/GIS/ShandongVillages/analyst/pathdis_test.tif","NetTest/slp_pcs.tif","#","#","BINARY 1 45","#","BINARY 1 -30 30","#","#")
	
	
	
	
	
	
#node_offset("PeakIndex",-0.0060,-0.0005)
def node_offset(node_dataset,x_offset,y_offset):
	with arcpy.da.UpdateCursor(node_dataset, ["SHAPE@"]) as cursor:
		for row in cursor:
			pos=row[0].getPart()
			pos.X+=x_offset
			pos.Y+=y_offset
			row[0]=pos
			cursor.updateRow(row)

def __field_type(dataset,field):
	target_fields = filter(lambda x:x.name==field,arcpy.Describe(dataset).fields)
	return target_fields[0].type

def __set_polyline_length(line,length):
	points = line.getPart()[0]
	origin = points[0]
	deltax = points[1].X - points[0].X
	deltay = points[1].Y - points[0].Y
	orilen = line.length
	new_x  = origin.X + deltax * float(length)/orilen
	new_y  = origin.Y + deltay * float(length)/orilen
	new_pt = arcpy.Point(new_x,new_y)
	return arcpy.Polyline(arcpy.Array([origin,new_pt]))

#从origin_coord放射到每一个点创建射线, 不规定长度时为两点间线段
#apiglio.src.net.create_vectors("villageGene_20221209","temp",ori,"code")
#field可以改成fields
def create_vectors(point_dataset,line_dataset,origin,field,length=None,in_memory=True):
	field_type=__field_type(point_dataset,field)
	points_rec=[]
	for row in arcpy.da.SearchCursor(point_dataset,["SHAPE@",field]):
		points_rec.append(row)
	del row
	#新建line_dataset
	sr=arcpy.Describe(point_dataset).SpatialReference.ExportToString()
	if in_memory:
		feature_class=arcpy.management.CreateFeatureclass("in_memory", line_dataset, "POLYLINE",spatial_reference=sr)[0]
	else:
		fs=os.path.split(line_dataset)
		feature_class=arcpy.management.CreateFeatureclass(fs[0], fs[1], "POLYLINE",spatial_reference=sr)[0]
	arcpy.AddField_management(line_dataset, field, field_type)
	for point_rec in points_rec:
		point = point_rec[0].firstPoint
		value = point_rec[1]
		line  = arcpy.Polyline(arcpy.Array([origin,point]))
		if length != None:
			line = __set_polyline_length(line,length)
		cursor = arcpy.da.InsertCursor(line_dataset, ["SHAPE@",field])
		cursor.insertRow([line,value])


#计算点坐标分类排斥性
def calc_exclusiveness(point_dataset,field,func=lambda x:x):
	field_type=__field_type(point_dataset,field)
	points_rec=[]
	for row in arcpy.da.SearchCursor(point_dataset,["SHAPE@",field]):
		points_rec.append([row[0],func(row[1])])
	del row
	class_dict = {}
	for point_rec in points_rec:
		point = point_rec[0].firstPoint
		value = point_rec[1]
		if class_dict.has_key(value):
			class_dict[value].append(point)
		else:
			class_dict[value]=[point]
	# print class_dict.keys()
	inner_distance = 0.0
	outer_distance = 0.0
	inner_count = 0
	outer_count = 0
	for key in class_dict.keys():
		count = len(class_dict[key])
		for i in range(count):
			for j in range(i):
				p1   = class_dict[key][i]
				p2   = class_dict[key][j]
				line = arcpy.Polyline(arcpy.Array([p1,p2]))
				inner_distance+=line.length
				inner_count+=1
	key_count = len(class_dict.keys())
	key_list  = class_dict.keys()[:]
	for i in range(key_count):
		for j in range(i):
			i_count = len(class_dict[key_list[i]])
			j_count = len(class_dict[key_list[j]])
			for ii in range(i_count):
				for jj in range(j_count):
					p1   = class_dict[key_list[i]][ii]
					p2   = class_dict[key_list[j]][jj]
					line = arcpy.Polyline(arcpy.Array([p1,p2]))
					outer_distance+=line.length
					outer_count+=1
	if inner_count*outer_count == 0:
		return None
	aver_inner = inner_distance/inner_count
	aver_outer = outer_distance/outer_count
	return aver_inner, aver_outer, aver_outer/aver_inner


#计算点要素空间距离并返回二维数组
def calc_geodistance_point(point_dataset):
	points = []
	for row in arcpy.da.SearchCursor(point_dataset,["SHAPE@"]):
		points.append(row[0])
	del row
	res = []
	cnt = len(points)
	#矩阵左下部分赋值
	for i in range(cnt):
		row_res = []
		for j in range(i):
			row_res.append(points[i].distanceTo(points[j]))
		res.append(row_res)
	#矩阵对角线赋值
	for i in range(cnt):
		res[i].append(0.0)
	#矩阵右上部分赋值
	for i in range(cnt):
		for j in range(i+1,cnt):
			res[i].append(res[j][i])
	return res


#计算点要素属性距离并返回二维数组
def calc_fielddistance_point(point_dataset, field_name, type_exchange=lambda x:float(x), relationship=lambda x,y:1.0/(a-b)**2):
	values = []
	for row in arcpy.da.SearchCursor(point_dataset,[field_name]):
		values.append(type_exchange(row[0]))
	del row
	res = []
	cnt = len(values)
	#矩阵左下部分和对角线赋值
	for i in range(cnt):
		row_res = []
		for j in range(i+1):
			row_res.append(relationship(values[i],values[j]))
		res.append(row_res)
	#矩阵右上部分赋值
	for i in range(cnt):
		for j in range(i+1,cnt):
			res[i].append(res[j][i])
	return res




