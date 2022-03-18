# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da
import os
import os.path


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
	
	
def Bipartite(dataset_1,dataset_2,output_edges,fields_1=[],fields_2=[],criterion=lambda fs1,fs2,pl:True,field_calc=lambda fs1,fs2:0.0,in_memory=True):
	#获取节点坐标，保存在列表中
	id_field_1=arcpy.ListFields(dataset_1)[0].name
	id_field_2=arcpy.ListFields(dataset_2)[0].name
	pos_1=[]
	for row in arcpy.da.SearchCursor(dataset_1,[id_field_1,"SHAPE@XY"]+fields_1):
		pos_1.append(row)
	del row
	pos_2=[]
	for row in arcpy.da.SearchCursor(dataset_2,[id_field_2,"SHAPE@XY"]+fields_2):
		pos_2.append(row)
	del row
	
	#新建网络output_edges
	if in_memory:
		feature_class=arcpy.CreateFeatureclass_management("in_memory", output_edges, "POLYLINE")[0]
	else:
		fs=os.path.split(output_edges)
		feature_class=arcpy.CreateFeatureclass_management(fs[0], fs[1], "POLYLINE")[0]
	arcpy.AddField_management(output_edges, "length", "DOUBLE")
	arcpy.AddField_management(output_edges, "node_1", "LONG")
	arcpy.AddField_management(output_edges, "node_2", "LONG")
	arcpy.AddField_management(output_edges, "calc", "DOUBLE")
	
	for r1 in pos_1:
		id_1=r1[0]
		po_1=r1[1]
		for r2 in pos_2:
			id_2=r2[0]
			po_2=r2[1]
			_from=arcpy.Point(po_1[0],po_1[1])
			_to=arcpy.Point(po_2[0],po_2[1])
			arr = arcpy.Array([_from,_to])
			polyline = arcpy.Polyline(arr)
			if criterion(r1[2:],r2[2:],polyline):
				cursor = arcpy.da.InsertCursor(output_edges, ["SHAPE@","length","node_1","node_2","calc"])
				cursor.insertRow([polyline,polyline.length,id_1,id_2,field_calc(r1[2:],r2[2:])])
	
	


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

	
	
	
	
	
	
	