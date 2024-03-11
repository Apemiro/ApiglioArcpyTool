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
	for inpf, oupf in zip(inputfiles, outputfiles):
		fig, axes = aplot.bandplot([1]*8+[6],["polar"]*6+["cart"]*3,figsize=(80,4),gap=1.0)
		ls = skl.dat_to_landscape(inpf)
		vecs = skl.landscape_to_360vectors(ls)
		vectors = [(math.pi*azi/180.0,v) for azi,v in enumerate(vecs)]
		aplot.skyline(vectors, "#", data_mode='radian', axis=axes[0])
		vectors_xy = skl.vectors_xyize(vectors)
		vectors_xy_new = avec.vector_combine(vectors_xy)
		for x in range(347):
			vectors_xy_new = avec.vector_combine(vectors_xy_new)
		aplot.vectors(vectors_xy_new,"#",data_mode="xy",axis=axes[1])
		for x in range(5):
			vectors_xy_new = avec.vector_combine(vectors_xy_new)
		aplot.vectors(vectors_xy_new,"#",data_mode="xy",axis=axes[2])
		for x in range(3):
			vectors_xy_new = avec.vector_combine(vectors_xy_new)
		aplot.vectors(vectors_xy_new,"#",data_mode="xy",axis=axes[3])
		vectors_xy_new = avec.vector_combine(vectors_xy_new)
		aplot.vectors(vectors_xy_new,"#",data_mode="xy",axis=axes[4])
		vectors_xy_new = avec.vector_combine(vectors_xy_new)
		aplot.vectors(vectors_xy_new,"#",data_mode="xy",axis=axes[5])
		azimuth, pitch, dist = zip(*ls)
		pitch = list(pitch)
		dist = list(dist)
		pitch.sort()
		dist.sort()
		aplot.lines(pitch,"#",str_rank, str_pitch, xlim=(0,len(pitch)),ylim=(-0.1,0.2),axis=axes[6])
		aplot.lines(dist,"#",str_rank ,str_dist ,xlim=(0,len(dist)),ylim=(dist[0],dist[-1]),axis=axes[7])
		aplot.scatters([(-180.0*x[0]/math.pi,x[1],x[2]) for x in ls], "#", str_azimuth, str_pitch, xlim=(-360,0), ylim=(0.0, +0.2), axis=axes[8])

		for idx in range(6):
			axes[idx].axes.get_yaxis().set_visible(False)
		for idx in range(6,8):
			xmin,xmax = axes[idx].axes.get_xlim()
			axes[idx].axes.set_xticks([xmin,xmin+(xmax-xmin)/2,xmax])
			axes[idx].axes.set_xticklabels(["0","50%","100%"])
		axes[8].axes.set_xticks([45*x-360 for x in range(9)])
		axes[8].axes.set_xticklabels(["E","SE","S","SW","W","NW","N","NE","E"])
		#axes[8].axes.set_xticklabels([str_e,str_e+str_s,str_s,str_w+str_s,str_w,str_w+str_n,str_n,str_e+str_n,str_e]) //why not work??
		aplot.saveplot(fig, oupf)
		#progressor_acc += 1
		#arcpy.SetProgressorPosition(progressor_acc)
finally:
	adf.EndUpdate()
