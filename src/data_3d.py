# -*- coding: UTF-8 -*-
import arcpy
import sys
import os.path
sys.path.append(os.path.split(__file__)[0])
import geoop.points as apgeo_points
#import geoop.geometry as apgeo_geometry


def CopyTo3D(dataset,dst_dataset,field_name,key=lambda x:x):
	#dst_dataset="temp_3d_"+dataset
	shape_type=arcpy.Describe(dataset).shapeType
	prj_info=arcpy.Describe(dataset).spatialReference.exportToString()
	arcpy.management.CreateFeatureclass("in_memory", dst_dataset, geometry_type=shape_type,has_z="ENABLED",spatial_reference=prj_info)
	fields_list=arcpy.Describe(dataset).fields
	fields_list_str=[]
	idx=-1
	acc=0
	for field in fields_list[2:]:
		fields_list_str.append(field.name)
		arcpy.management.AddField(dst_dataset,field.name,field.type,field.precision,field.scale,field.length,field.aliasName,field.isNullable,field.required,field.domain)
		if field.name==field_name:
			idx=acc
		acc+=1
	if idx<0:
		raise Exception("找不到字段"+field_name+"。")
	cursor=arcpy.da.SearchCursor(dataset,["SHAPE@"]+fields_list_str)
	dst_cursor=arcpy.da.InsertCursor(dst_dataset,["SHAPE@"]+fields_list_str)
	tmp_lst=[]
	for row in cursor:
		shp=row[0]
		z=key(row[idx+1])
		shp=apgeo_points.set_z_points(shp,z)
		tmp_lst.append(z)
		other_values=row[1:]
		dst_cursor.insertRow([shp]+list(other_values))
	del row,cursor,dst_cursor
	return(tmp_lst)

def skyline_table_to_polygon(in_table,out_dataset,path="in_memory"):
	point_coords=[]
	acc=-1
	break_point=-1
	last_value=400 # 大于最大水平角
	cursor=arcpy.da.UpdateCursor(in_table,["HORIZ_ANG","ZENITH_ANG"])
	for row in cursor:
		acc+=1
		point_coords.append(row)
		if row[0]>last_value+10:
			break_point=acc
			#循环条件的+10毫无意义，浮点型比较的特性，以后再管为啥吧
		last_value=row[0]
	point_coords_sorted=point_coords[break_point:]+point_coords[:break_point]
	del cursor
	point_coords_sorted.insert(0,[360.0,0.0])
	point_coords_sorted.append([0.0,0.0])
	points=[]
	for p in point_coords_sorted:
		points.append(arcpy.Point(*p))
	ploygon=arcpy.Polygon(arcpy.Array(points))
	arcpy.management.CreateFeatureclass(path,out_dataset,"POLYGON")
	cursor=arcpy.da.InsertCursor(path+'/'+out_dataset,["SHAPE@"])
	cursor.insertRow([ploygon])
	del cursor
	return ploygon



#将天际线轮廓图形转为每位由0-200值的字符串，默认每个字符表示0.25度的水平角宽度
#点阵的初始化应该放在别的地方
def skyline_polygon_to_text(geo,horiz_range=[0,360],zenith_range=[75,105],cell_width_second=900,cell_height_second=900):
	cells=SkylineGrid(horiz_range,zenith_range,cell_width_second,cell_height_second)
	return cells




















class SkylineGrid:
	"指定水平和垂直角度范围及秒单位步长，创建用于天际线轮廓分析的点阵"
	point_cells=[]
	horiz_range=[0,360]
	zenith_range=[75,105]
	cell_width_second=900
	cell_height_second=900
	grid_width=None
	grid_height=None
	def __init__(self,a_horiz_range=[0,360],a_zenith_range=[75,105],a_cell_width_second=900,a_cell_height_second=900):
		self.horiz_range=a_horiz_range
		self.zenith_range=a_zenith_range
		self.cell_width_second=a_cell_width_second
		self.cell_height_second=a_cell_height_second
		self.point_cells=[]
		self.grid_width=(self.horiz_range[1]-self.horiz_range[0])*3600/self.cell_width_second
		self.grid_height=(self.zenith_range[1]-self.zenith_range[0])*3600/self.cell_height_second
		h_unit=self.cell_height_second/3600.0
		w_unit=self.cell_width_second/3600.0
		h2=h_unit/2.0
		w2=w_unit/2.0
		for x in range(self.grid_width):
			self.point_cells.append([])
			for y in range(self.grid_height):
				x0=self.horiz_range[0]+x*w_unit+w2
				y0=self.zenith_range[0]+y*h_unit+h2
				#tmp=apgeo_geometry.polygon_cell(y0+h_unit,x0,x0+w_unit,y0)
				tmp=arcpy.Point(x0,y0)
				self.point_cells[-1].append(tmp)
	def stamp_of_polygon(self,geo):
		if geo.__class__<>arcpy.Polygon:
			raise Exception("geo需要是arcpy.Polygon类型")
		stamp_array=[]
		for x in range(self.grid_width):
			tmp=0
			for y in range(self.grid_height-1,-1,-1):
				if geo.contains(self.point_cells[x][y]):
					tmp=y
					break
			stamp_array.append(tmp)
		return stamp_array







'''
slgrid=apiglio.src.data_3d.SkylineGrid()



'''











