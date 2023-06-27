# -*- coding: UTF-8 -*-
import arcpy
import numpy
import math

def con(condition,t_value,f_value):
	if condition:
		return t_value
	else:
		return f_value

#raster_ca(f1,f2,6,lambda arr:con(arr[3:-4,3:-4].mean()-arr.mean()>5,1,0))
#raster_ca(f1,f2,9,lambda arr:con(max(arr[0:9,:].max(),arr[10:19,:].max(),arr[9,0:9].max(),arr[9,10:19].max())<arr[9,9],1,0))
#raster_ca(f1,f1,9,lambda arr:con(max(arr[0:9,:].max(),arr[10:19,:].max(),arr[9,0:9].max(),arr[9,10:19].max())<arr[9,9],1,0))
#我看还是允许覆盖编辑吧
def raster_ca(dataset,output,neighbor_dist=1,ca_func=lambda arr:arr[1,1],no_data=-1):
	my_array=arcpy.RasterToNumPyArray(dataset)
	new_array=my_array.copy()
	shape=my_array.shape
	max_col=shape[0]-1
	max_line=shape[1]-1
	for line in range(0,max_line):
		for col in range(0,max_col):
			first_line=line-neighbor_dist
			last_line=line+neighbor_dist
			first_col=col-neighbor_dist
			last_col=col+neighbor_dist
			neigh_array=my_array[first_col:last_col+1,first_line:last_line+1]
			if neigh_array.shape[0]==2*neighbor_dist+1 and neigh_array.shape[1]==2*neighbor_dist+1:
				new_array[col,line]=ca_func(neigh_array)
			else:
				new_array[col,line]=no_data
	new_raster = arcpy.NumPyArrayToRaster(new_array)
	new_raster.save(output)

#给定像元坐标，返回对应的地理坐标
def uv_to_xy(raster,uv):
	ll = arcpy.Describe(raster).extent.XMin
	rr = arcpy.Describe(raster).extent.XMax
	bb = arcpy.Describe(raster).extent.YMin
	tt = arcpy.Describe(raster).extent.YMax
	cw = arcpy.Describe(raster).meanCellWidth
	ch = arcpy.Describe(raster).meanCellHeight
	cx = arcpy.Describe(raster).width
	cy = arcpy.Describe(raster).height
	u = uv[0]
	v = uv[1]
	if u>=cx or v>=cy or u<0 or v<0:
		return None
	x = ll + (u+0.5)*cw
	y = tt - (v+0.5)*ch
	return [x,y]

#给定地理坐标，返回对应的像元坐标
def xy_to_uv(raster,xy):
	ll = arcpy.Describe(raster).extent.XMin
	rr = arcpy.Describe(raster).extent.XMax
	bb = arcpy.Describe(raster).extent.YMin
	tt = arcpy.Describe(raster).extent.YMax
	cw = arcpy.Describe(raster).meanCellWidth
	ch = arcpy.Describe(raster).meanCellHeight
	cx = arcpy.Describe(raster).width
	cy = arcpy.Describe(raster).height
	x = xy[0]
	y = xy[1]
	if x<ll or x>rr or y<bb or y>tt:
		return None
	u = math.trunc((x-ll)/float(cw))
	v = math.trunc((tt-y)/float(ch))
	return [u,v]









'''
my_array = arcpy.RasterToNumPyArray('C:/data/inRaster')
my_array_sum = my_array.sum(1)
my_array_sum.shape = (my_array.shape[0], 1)
my_array_perc = (my_array * 1.0) / my_array_sum
new_raster = arcpy.NumPyArrayToRaster(my_array_perc)
new_raster.save("C:/output/fgdb.gdb/PercentRaster")
'''



'''
net.clear
io.inp.json "K:\LAB_Pascal\table_calc\Table_Calc_2\test_file\block_edges.json"
net.len2weight
//net.reverseweight
io.out.adj "K:\LAB_Pascal\table_calc\Table_Calc_2\test_file\ad_rev.txt"
'''