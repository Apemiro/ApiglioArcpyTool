# -*- coding: UTF-8 -*-
import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.geoop.vector as avec
import src.specific.skl as skl
import src.plot as aplot
import src.codetool.df as adf
import math
import numpy

input_filename  = arcpy.GetParameterAsText(0)
output_filename = arcpy.GetParameterAsText(1)
min_pitch_str = arcpy.GetParameterAsText(2)
max_pitch_str = arcpy.GetParameterAsText(3)
try:
	min_pitch = float(min_pitch_str)
except:
	min_pitch = 0.0
try:
	max_pitch = float(max_pitch_str)
except:
	max_pitch = +0.2


'''
str_rank = 'rank'       # 位序
str_dist = 'dist'       # 视距
str_pitch = 'pitch'     # 仰角
str_azimuth = 'azimuth' # 方位角
'''
str_rank = u'\u4f4d\u5e8f'
str_dist = u'\u89c6\u8ddd'
str_pitch = u'\u4ef0\u89d2'
str_azimuth = u'\u65b9\u4f4d\u89d2'
str_e = u'\u4e1c'
str_s = u'\u5357'
str_w = u'\u897f'
str_n = u'\u5317'

if not os.path.exists(input_filename):
	raise Exception("Input file or directory does not exist.")
if os.path.isdir(input_filename):
	if not os.path.isdir(output_filename):
		raise Exception("Ouput should be directory as input is.")
	fs = os.listdir(input_filename)
	inputfiles = ["%s/%s"%(input_filename,x) for x in fs if x[-4:]=='.dat']
	target_test_files = ["%s/%s"%(input_filename,x) for x in fs if x[-7:]=='.tp.log']
	outputfiles = ["%s/%s.png"%(output_filename,x[:-4]) for x in fs if x[-4:]=='.dat']
elif os.path.isfile(input_filename):
	if os.path.exists(output_filename):
		raise Exception("Ouput file already exists.")
	inputfiles = [input_filename]
	outputfiles = [output_filename]
else:
	raise Exception("Invalid input type.")

#arcpy.SetProgressor("绘制", "正在绘制图表...", 0, len(inputfiles)+1, 1)
#进度条为什么没用？
adf.BeginUpdate()
try:
	#progressor_acc = 0
	for inpf, oupf, tpf in zip(inputfiles, outputfiles, target_test_files):
		fig, axes = aplot.bandplot([6],["cart"],figsize=(80,4),gap=1.0)
		ls = skl.dat_to_landscape(inpf)
		if os.path.exists(tpf):
			with open(tpf,"r") as ftmp:
				stmp = ftmp.read()
				target_point_data = eval(stmp)
		else:
			target_point_data = []
		
		fig_height = (max_pitch - min_pitch)*6000
		aplot.scatters([(-180.0*x[0]/math.pi,x[1],x[2]) for x in ls], oupf, str_azimuth, str_pitch, figsize=(18880,fig_height), xlim=(-360,0), ylim=(min_pitch, max_pitch), axis=axes[0], cmap='magma')
		cxs, cys = [],[]
		for row in target_point_data:
			if row[0]==None: continue
			cx = -180.0*row[0]/math.pi
			cy = row[1]
			cxs.append(cx)
			cys.append(cy)
			label = row[2]
			if cy>max_pitch or cy<min_pitch: continue
			axes[0].text(cx,cy,label,rotation=0,fontsize=3,fontproperties=aplot.ch_font)
		axes[0].scatter(cxs,cys,s=2,c="red")
		aplot.saveplot(fig, oupf)
		
		arcpy.AddMessage("inpf=%s | oupf=%s | tpf=%s"%(inpf, oupf, tpf))
		#progressor_acc += 1
		#arcpy.SetProgressorPosition(progressor_acc)
finally:
	adf.EndUpdate()
