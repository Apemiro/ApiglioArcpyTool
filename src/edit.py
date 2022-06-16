# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da
import sys
import os.path
sys.path.append(os.path.split(__file__)[0])
import codetool.feature as ct_fea
	
	
def PointMove(dataset,x_offset,y_offset):
	cursor=arcpy.da.UpdateCursor(dataset,["SHAPE@"])
	for row in cursor:
		geo=row[0]
		if type(geo) == arcpy.geometries.PointGeometry:
			ptr=geo.firstPoint
			ptr.X+=x_offset
			ptr.Y+=y_offset
			row[0]=arcpy.geometries.PointGeometry(ptr)
		elif type(geo) == arcpy.geometries.Polyline:
			arr=geo.getPart()[0]
			for i in arr:
				i.X+=x_offset
				i.Y+=y_offset
			row[0]=arcpy.Polyline(arcpy.Array(arr))
		elif type(geo) == arcpy.geometries.Polygon:
			arr=geo.getPart()
			for i in arr:
				for j in i:
					j.X+=x_offset
					j.Y+=y_offset
			row[0]=arcpy.Polygon(arcpy.Array(arr))
		else:
			print(type(geo))
			raise Exception("错误的文件几何类型")
	del row,cursor


def GeoZone(dataset,x_times,y_times):
	cursor=arcpy.da.UpdateCursor(dataset,["SHAPE@"])
	for row in cursor:
		geo=row[0]
		if type(geo) == arcpy.geometries.PointGeometry:
			ptr=geo.firstPoint
			ptr.X*=x_times
			ptr.Y*=y_times
			row[0]=arcpy.geometries.PointGeometry(ptr)
		elif type(geo) == arcpy.geometries.Polyline:
			arr=geo.getPart()[0]
			for i in arr:
				i.X*=x_times
				i.Y*=y_times
			row[0]=arcpy.Polyline(arcpy.Array(arr))
		elif type(geo) == arcpy.geometries.Polygon:
			arr=geo.getPart()
			for i in arr:
				for j in i:
					j.X*=x_times
					j.Y*=y_times
			row[0]=arcpy.Polygon(arcpy.Array(arr))
		else:
			print(type(geo))
			raise Exception("错误的文件几何类型")
		cursor.updateRow(row)
	del row,cursor


def ContainsRecorder(iden_dataset,region_dataset,record_field):
	regions=[]
	for row in arcpy.da.SearchCursor(region_dataset,["FID","SHAPE@"]):
		regions.append(row)
	del row
	#print(regions)
	cursor=arcpy.da.UpdateCursor(iden_dataset,["SHAPE@",record_field.decode("utf8")])
	for row in cursor:
		comma=','
		for region in regions:
			if region[1].contains(row[0]):
				comma+=str(region[0])+','
				#print(region[0])
		#if comma[0]==',':
		#	comma=comma[1:]
		row[1]=comma
		cursor.updateRow(row)
	del row,cursor

def unique(dataset,path,out_name):
	shps=[]
	sr=arcpy.Describe(dataset).SpatialReference.ExportToString()
	arcpy.management.CreateFeatureDataset(path,out_name,sr)
	cur1=arcpy.da.SearchCursor(dataset,["SHAPE@"])
	cur2=arcpy.da.InsertCursor(path+"/"+out_name,["SHAPE@"])
	for row in cur1:
		pass
		#这没写完

def check_unique(dataset):
	shps=ct_fea.to_list(dataset)
	count=len(shps)
	for ii in range(count):
		for jj in range(count):
			if ii==jj:
				continue
			if shps[ii].equals(shps[jj]):
				return(shps[ii])
	return(None)

















