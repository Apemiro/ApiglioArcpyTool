# -*- coding: UTF-8 -*-
# skyline tool

import arcpy
import numpy
import os.path
import sys
sys.path.append(os.path.split(__file__)[0]+"/..")
import codetool.df
import map_feature
import codetool.feature
import raster
import geoop.geolib
import math

class SkylineGrid:
	"指定水平和垂直角度范围及秒单位步长，创建用于天际线轮廓分析的点阵。\nSkylineGrid(a_horiz_range=[0,360],a_zenith_range=[75,105],a_cell_width_second=900,a_cell_height_second=900)"
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
	point_coords_sorted.insert(0,[360.0,0.0])
	point_coords_sorted.append([0.0,0.0])
	points=[]
	for p in point_coords_sorted:
		points.append(arcpy.Point(*p))
	polygon=arcpy.Polygon(arcpy.Array(points))
	try:
		arcpy.management.CreateFeatureclass(path,out_dataset,"POLYGON")
		cursor=arcpy.da.InsertCursor(path+'/'+out_dataset,["SHAPE@"])
		cursor.insertRow([polygon])
	except:
		return polygon
	finally:
		del cursor


#将天际线轮廓图形转为每位由0-200值的字符串，默认每个字符表示0.25度的水平角宽度
#点阵的初始化应该放在别的地方
def skyline_polygon_to_text(geo,horiz_range=[0,360],zenith_range=[75,105],cell_width_second=900,cell_height_second=900):
	cells=SkylineGrid(horiz_range,zenith_range,cell_width_second,cell_height_second)
	return cells
















def __iter__skyline_graph(pathn,inpns,outn):
	#paths=[obs_point,sky_line]
	temp_table_name=pathn+'/'+"TempSklTab.dbf"
	arcpy.SkylineGraph_3d(pathn+'/'+inpns[0],pathn+'/'+inpns[1],out_angles_table=temp_table_name)
	skyline_table_to_polygon(temp_table_name,outn,pathn)

def iter_skyline_graph(obspoint,skyline,out_dataset,run_path):
	map_feature.iterator_list([obspoint,skyline],out_dataset,__iter__skyline_graph,run_path,'.shp')


def vector_angle(vec):
	x = float(vec[0])
	y = float(vec[1])
	if x==0:
		if y>0: return math.pi/2.0
		elif y<0: return math.pi/-2.0
		else: return None
	res=math.atan(y/x)
	if x<0:res+=math.pi
	if res<0:res+=2*math.pi
	return res
	
def vector_substract(a,b):
	return [a[0]-b[0],a[1]-b[1]]

def vector_length(a):
	return (a[0]**2+a[1]**2)**0.5

def ss(view_point, dem_raster, max_distance, landscape_fn='TempViewDist'):
	if not isinstance(view_point,arcpy.PointGeometry):
		raise Exception('view_point 不是arcpy.PointGeometry')
	lng = view_point.firstPoint.X
	lat = view_point.firstPoint.Y
	dem = arcpy.RasterToNumPyArray(dem_raster)
	viewpoint_uv = raster.xy_to_uv(dem_raster, [lng, lat])
	viewpoint_xy = raster.uv_to_xy(dem_raster, viewpoint_uv)
	view_point_fn = 'TempViewPoint'
	vis_file_name = 'Visibility'
	obs_height = "20.0"
	codetool.feature.to_file([view_point],view_point_fn,path="in_memory")
	arcpy.Visibility_3d(in_raster=dem_raster, in_observer_features=view_point_fn, out_raster="in_memory/"+vis_file_name, out_agl_raster="", analysis_type="OBSERVERS", nonvisible_cell_value="ZERO", z_factor="1", curvature_correction="FLAT_EARTH", refractivity_coefficient="0.13", surface_offset="", observer_elevation="", observer_offset=obs_height, inner_radius="", outer_radius="", horizontal_start_angle="", horizontal_end_angle="", vertical_upper_angle="", vertical_lower_angle="")
	vis = arcpy.RasterToNumPyArray(vis_file_name)
	print("可见性计算完成")
	nrow = len(vis)
	ncol = vis.size / nrow
	landscape = []
	elev_vp = dem[viewpoint_uv[1]][viewpoint_uv[0]]
	print("计算每一个像元（%d, %d），视点坐标（%d, %d）"%(nrow,ncol,viewpoint_uv[0],viewpoint_uv[1]))
	for pi in range(nrow):
		delta_y = abs(pi-viewpoint_uv[1])
		if delta_y>max_distance: continue
		for pj in range(ncol):
			delta_x = abs(pj-viewpoint_uv[0])
			if delta_x>max_distance: continue
			if (delta_x**2+delta_y**2)**0.5>max_distance: continue
			if vis[pi][pj] == 0: continue
			tar = raster.uv_to_xy(dem_raster,[pj,pi])
			vec = vector_substract(tar,viewpoint_xy)
			orie = vector_angle(vec)
			if orie == None: continue
			dist = vector_length(vec)
			# elev = dem[pi][pj] #改用仰角而不是高度
			elev = math.atan((dem[pi][pj] - elev_vp)/dist)
			landscape.append([orie, elev, dist, pj, pi, tar[0],tar[1], vec[0], vec[1]])
	print("保存到文件中")
	list_of_dict = []
	for row in landscape:
		ptmp = geoop.geolib.to_point([row[0],float(row[1])])
		geop = geoop.geolib.to_pointgeo(ptmp)
		dict_in_list = {}
		dict_in_list["SHAPE@"] = geop
		dict_in_list["Shape"] = geop
		dict_in_list["dist"] = row[2]
		list_of_dict.append(dict_in_list)
	if len(list_of_dict)>0:
		codetool.feature.dict_to_file(list_of_dict,landscape_fn)
	else:
		print("无有效视点")
		landscape = []
	return landscape


























