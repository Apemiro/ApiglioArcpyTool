# -*- coding: UTF-8 -*-
import arcpy
import numpy

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


def raster_xy(raster,xy):
	ll=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","LEFT")
	rr=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","RIGHT")
	tt=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","TOP")
	bb=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","BOTTOM")
	cx=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","CELLSIZEX")
	cy=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","CELLSIZEY")
	count_col=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","COLUMNCOUNT")
	count_row=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","ROWCOUNT")
	count_band=arcpy.management.GetRasterProperties("Tsinan_dem_ave_5_prj.tif","BANDCOUNT")














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