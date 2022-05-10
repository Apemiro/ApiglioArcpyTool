# -*- coding: UTF-8 -*-
# 栅格操作

import arcpy
import arcpy.sa

#但是真的太慢了，原理上讲不通，只能说arctool真慢
def pixel_value(raster,point):
	out_raster=arcpy.sa.ExtractByPoints(raster,[point])
	return out_raster.maximum




























