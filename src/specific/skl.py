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
import logline
import plot
import struct
import gc

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
		elif y<0: return math.pi*3.0/2.0
		else: return None
	res=math.atan(y/x)
	if x<0:res+=math.pi
	if res<0:res+=2*math.pi
	return res
	
def vector_substract(a,b):
	return [a[0]-b[0],a[1]-b[1]]

def vector_length(a):
	return (a[0]**2+a[1]**2)**0.5

# 返回结果[ls]  其中ls : array[0..2] = [x,y,dist]
# x为方位角: E=0; N=pi/2; W=pi; S=3*pi/2
# y为仰角：horizontal=0; top=pi/2; bottom=-pi/2
def viewpoint_to_landscape(view_point, dem_raster, max_distance, min_distance=0, landscape_fn='TempViewDist', export_path='in_memory',export_formats=["shp","dat"]):
	export_formats = [x.lower() for x in export_formats]
	cw = arcpy.Describe(dem_raster).meanCellWidth
	ch = arcpy.Describe(dem_raster).meanCellHeight
	cw_sqr = cw * cw
	ch_sqr = ch * ch
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
	if arcpy.Exists("in_memory/"+view_point_fn):
		arcpy.management.Delete("in_memory/"+view_point_fn)
	if arcpy.Exists("in_memory/"+vis_file_name):
		arcpy.management.Delete("in_memory/"+vis_file_name)
	codetool.feature.to_file([view_point],view_point_fn,path='in_memory')
	arcpy.Visibility_3d(in_raster=dem_raster, in_observer_features="in_memory/"+view_point_fn, out_raster="in_memory/"+vis_file_name, out_agl_raster="", analysis_type="OBSERVERS", nonvisible_cell_value="ZERO", z_factor="1", curvature_correction="FLAT_EARTH", refractivity_coefficient="0.13", surface_offset="", observer_elevation="", observer_offset=obs_height, inner_radius="", outer_radius="", horizontal_start_angle="", horizontal_end_angle="", vertical_upper_angle="", vertical_lower_angle="")
	vis = arcpy.RasterToNumPyArray("in_memory/"+vis_file_name)
	logline.log("可见性计算完成","m")
	nrow = len(vis)
	ncol = vis.size / nrow
	landscape = []
	elev_vp = dem[viewpoint_uv[1]][viewpoint_uv[0]]
	logline.log("计算每一个像元（%d, %d），视点坐标（%d, %d）"%(nrow,ncol,viewpoint_uv[0],viewpoint_uv[1]),"m")
	for pi in range(nrow):
		delta_y = abs(pi-viewpoint_uv[1])
		if delta_y*ch>max_distance: continue
		for pj in range(ncol):
			delta_x = abs(pj-viewpoint_uv[0])
			if delta_x*cw>max_distance: continue
			target_distance = (cw_sqr*delta_x**2+ch_sqr*delta_y**2)**0.5
			if target_distance>max_distance: continue
			if target_distance<min_distance: continue
			if vis[pi][pj] == 0: continue
			tar = raster.uv_to_xy(dem_raster,[pj,pi])
			vec = vector_substract(tar,viewpoint_xy)
			orie = vector_angle(vec)
			if orie == None: continue
			dist = vector_length(vec)
			# elev = dem[pi][pj] #改用仰角而不是高度
			elev = math.atan((dem[pi][pj] - elev_vp)/dist)
			landscape.append([orie, elev, dist])
	logline.log("保存到文件中","m")
	valid_fn = arcpy.ValidateTableName(landscape_fn)
	if "shp" in export_formats:
		list_of_dict = []
		for row in landscape:
			pos_x = row[0]*10800/math.pi
			pos_y = row[1]*10800/math.pi
			ptmp = geoop.geolib.to_point([21600-pos_x,pos_y]) #x轴根据方位角的定义做左右镜像
			geop = geoop.geolib.to_pointgeo(ptmp)
			dict_in_list = {}
			dict_in_list["SHAPE@"] = geop
			dict_in_list["Shape"] = geop
			dict_in_list["dist"] = row[2]
			list_of_dict.append(dict_in_list)
		if len(list_of_dict)>0:
			logline.log('%s  %s.shp'%(export_path, valid_fn),"m")
			codetool.feature.dict_to_file(list_of_dict,"%s.shp"%(valid_fn,),export_path)
		else:
			logline.log("无有效视点","w")
			landscape = []
	if "dat" in export_formats:
		with open("%s/%s.dat"%(export_path,valid_fn),"wb") as f:
			acc=0
			for row in landscape:
				f.write(struct.pack("<d",row[0]))
				f.write(struct.pack("<d",row[1]))
				f.write(struct.pack("<d",row[2]))
				acc+=1
	del dem, vis, viewpoint_uv, viewpoint_xy
	plot.plt.close('all')
	plot.plt.clf()
	gc.collect()
	return landscape


def viewpoints_to_landscape(view_points, dem_raster, max_dist, min_dist, export_path, name_field=None, export_formats=["shp","dat"]):
	try:
		codetool.df.BeginUpdate()
		vps = codetool.feature.to_dict(view_points)
		if name_field == None:
			nf = arcpy.Describe(view_points).fields[0].name
		else:
			nf = name_field
		for vp, fn in [(x["SHAPE@"],x[nf]) for x in vps]:
			viewpoint_to_landscape(vp, dem_raster, max_dist, min_dist, "%s"%(fn,), export_path, export_formats)
	except Exception as err:
		logline.log("Failed: %s"%(fn,),"e")
		for arg in err.args:
			logline.log(arg,"e")
		logline.log(err.message,"e")
	finally:
		codetool.df.EndUpdate()

def dat_to_landscape(filename):
	result=[]
	with open(filename, "rb") as f:
		while True:
			chunk = f.read(24)
			if len(chunk) != 24: break
			x = struct.unpack("<d",chunk[:8])[0]
			y = struct.unpack("<d",chunk[8:16])[0]
			d = struct.unpack("<d",chunk[16:])[0]
			result.append([x,y,d])
	return result

def shp_to_landscape(dataset):
	shp_dicts = codetool.feature.to_dict(dataset)
	result=[]
	for fea in shp_dicts:
		point = fea["SHAPE@"].firstPoint
		pos_x = point.X*math.pi/10800.0
		pos_y = point.Y*math.pi/10800.0
		result.append([pos_x,pos_y,fea["dist"]])
	return result

def landscape_to_360vectors(ls):
	'''
	divide (azimuth, pitch, distance) into 360 groups by pitch. 
	calculate IQR of pitch(radian). 
	return list of (azimuth, IQR). 
	'''
	values=[list() for x in range(360)]
	for v in ls:
		if v[2]<=0: continue
		azimuth = int(math.floor(0.5+180.0*v[0]/math.pi))
		azimuth %= 360
		# values[azimuth].append(v[1]*v[2]/1000.0)
		values[azimuth].append(v[1])
	result=[]
	for value in values:
		vp_cnt = len(value)
		if vp_cnt==0:
			result.append(0)
		else:
			q1 = numpy.percentile(value,25)
			q3 = numpy.percentile(value,75)
			result.append(q3-q1)
		# result.append(sum(value)/float(vp_cnt) if vp_cnt!=0 else 0)
	return result

def vectors_xyize(list_of_azimuth_radius):
	result=[]
	for azimuth, radius in list_of_azimuth_radius:
		x = radius * math.cos(azimuth)
		y = radius * math.sin(azimuth)
		result.append((x,y))
	return result

def grouped_landscape(ls):
	orientation_cell = math.pi / 60.0 # 3.degrees
	group_count = int(2*math.pi / orientation_cell)
	result = [list() for x in range(group_count)]
	for one in ls:
		group_no = group_count - int(one[0] / orientation_cell) - 1
		result[group_no].append(one)
	return result

def gls_to_plot(gls,filename):
	g_max_y = [max([one[1] for one in grp]) for grp in gls]
	g_min_y = [min([one[1] for one in grp]) for grp in gls]
	g_max_dist = [max([one[2] for one in grp]) for grp in gls]
	g_min_dist = [min([one[2] for one in grp]) for grp in gls]
	plot.lines(zip(g_min_y,g_max_y),filename+'_y.png','each 3-degree-horizontal angle','radian vertical angle',figsize=[36,3])
	plot.lines(zip(g_min_dist,g_max_dist),filename+'_dist.png','each 3-degree-horizontal angle','visible distance',figsize=[36,3])
	#增加K-means聚类出2~3类的聚类系数比较得出的景别判断图





