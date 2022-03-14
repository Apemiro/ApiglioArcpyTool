# -*- coding: UTF-8 -*-
import arcpy
import arcpy.sa
import arcpy.da
	
	
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
			row[0]=arcpy.Polyline(acrpy.Array(arr))
		elif type(geo) == arcpy.geometries.Polygon:
			arr=geo.getPart()
			for i in arr:
				for j in i:
					j.X+=x_offset
					j.Y+=y_offset
			row[0]=arcpy.Polygon(acrpy.Array(arr))
		else:
			print(type(geo))
			raise Exception("错误的文件几何类型")
		for region in regions:
			if region[1].contains(row[0]):
				comma+=str(region[0])+','
		row[1]=comma
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