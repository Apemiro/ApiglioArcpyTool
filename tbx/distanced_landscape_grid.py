# -*- coding: UTF-8 -*-
import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.skl as skl
import src.plot as aplot
import math
import numpy

def key_count(arr):
	return(len(arr))
def key_mean(arr):
	if len(arr)<2:
		return(0)
	return(numpy.mean(arr))
def key_min(arr):
	if len(arr)<1:
		return(0)
	return(min(arr))
def key_max(arr):
	if len(arr)<1:
		return(0)
	return(max(arr))

input_filename  = arcpy.GetParameterAsText(0)
output_filename = arcpy.GetParameterAsText(1)
value_mode = arcpy.GetParameterAsText(2)
stats_mode = arcpy.GetParameterAsText(3)
colorsmap  = arcpy.GetParameterAsText(4)
data_range_str  = arcpy.GetParameterAsText(5)
vertical_reso   = int(arcpy.GetParameterAsText(6))

if value_mode == "COUNT":
	key = key_count
else:
	if stats_mode == "MAX":
		key = key_max
	elif stats_mode == "MIN":
		key = key_min
	else:
		key = key_mean
if colorsmap in [None,""]:
	colorsmap = "Greens"
try:
	data_range=[float(x) for x in data_range_str.split(" ")]
except:
	data_range=None
ls = skl.dat_to_landscape(input_filename)
ls_in_angle_minute = [(x[0]/math.pi*180.0,x[1]/math.pi*180.0,x[2]) for x in ls]
aplot.grids(ls_in_angle_minute, output_filename, u'\u65b9\u4f4d\u89d2', u'\u4fef\u4ef0\u89d2', cellscale=(1,1), figsize=(200,12), key=key, colorsmap=colorsmap, datarange=data_range, cellcount=[360, vertical_reso])
