# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.font_manager as ftm
import math
import gc
import os
p=os.path.split(__file__)[0]
ch_font = ftm.FontProperties(fname=p+'/../assets/fonts/simhei.ttf')

def __floor(num,frac):
	return num - num%frac
def __ceil(num,frac):
	return num - num%frac + frac

def lines(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, xlim=None, ylim=None):
	if figsize == None:
		fig = plt.figure()
	else:
		fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if xlim != None:
		plt.xlim(xlim[0],xlim[1])
	if ylim != None:
		plt.ylim(ylim[0],ylim[1])
	ax.plot(data)
	fig.savefig(save_filename, dpi=dpi)
	fig.clf()
	plt.close()
	gc.collect()

def grids(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, colorsmap=None, cellscale=None, key=lambda arr:sum(arr)):
	'''argument data need list of tuple (x, y)'''
	
	#计算数据边界
	x_min = float('+Inf')
	x_max = float('-Inf')
	y_min = x_min
	y_max = x_max
	for datum in data:
		if datum[0] < x_min: x_min = datum[0]
		if datum[0] > x_max: x_max = datum[0]
		if datum[1] < y_min: y_min = datum[1]
		if datum[1] > y_max: y_max = datum[1]
	range_x = float(x_max - x_min)
	range_y = float(y_max - y_min)
	population = len(data)
	if cellscale==None:
		proportion = range_x / float(range_y)
		cnt_col = int((population)**0.5)+1
		cnt_row = int((population / proportion)**0.5)+1
		cellscale = (range_x / cnt_col, range_y / cnt_row)
	else:
		cnt_col = int(range_x / cellscale[0])+1
		cnt_row = int(range_y / cellscale[1])+1
		proportion = cellscale[0] / float(cellscale[1])
		
	reso_x = math.floor(math.log10(cellscale[0]))
	reso_y = math.floor(math.log10(cellscale[1]))
	x_min = __floor(x_min, 10**reso_x)
	y_min = __floor(y_min, 10**reso_y)
	x_max = __ceil(x_max, 10**reso_x)
	y_max = __ceil(y_max, 10**reso_y)
	
	#统计网格中的数据
	grid_data = []
	for row in range(cnt_row):
		grid_data.append([[] for x in range(cnt_col)])
	for datum in data:
		grid_x = int(cnt_col * (datum[0] - x_min) / range_x)
		grid_y = int(cnt_row * (datum[1] - y_min) / range_y)
		if grid_x >= cnt_col: grid_x = cnt_col-1
		if grid_y >= cnt_row: grid_y = cnt_row-1
		if len(datum)<3:
			grid_data[grid_y][grid_x].append(1)
		else:
			grid_data[grid_y][grid_x].append(datum[2])
	plot_data = [[key(elem) for elem in row] for row in grid_data]
	
	#计算画幅大小
	if figsize==None:
		fig_w = cnt_col * 0.5
		fig_h = cnt_row * 0.5
		if fig_w <  1: fig_w = 1
		if fig_w > 50: fig_w = 50
		if fig_h <  1: fig_h = 1
		if fig_h > 50: fig_h = 50
		figsize = (fig_w+2, fig_h)
	
	#确定色带位置
	if figsize[0]>figsize[1]:
		orientation = 'vertical'
		pad = 0.05 * figsize[1] / float(figsize[0])
	else:
		orientation = 'horizontal'
		pad = 0.05 * figsize[0] / float(figsize[1])

	fig, axs = plt.subplots(figsize=figsize)
	if colorsmap == None:
		colorsmap = mpc.LinearSegmentedColormap.from_list("villband",[(1,1,1),(0.75,0,0)])
	psm = axs.pcolormesh(plot_data, cmap = colorsmap, shading='nearest')
	axs.grid(True, linestyle='-', color='White', linewidth=3)
	fig.colorbar(psm, ax=axs, orientation=orientation, pad=pad)
	plt.xlim(0, cnt_col)
	plt.ylim(0, cnt_row)
	plt.xlabel(xlabel ,fontproperties=ch_font)
	plt.ylabel(ylabel ,fontproperties=ch_font)
	x_ticks=[]
	x_digit=max(0,int(-reso_x))
	while len(set(x_ticks))!=cnt_col+1:
		x_ticks = [("%."+str(x_digit)+"f")%(x_min+i*cellscale[0],) for i in range(cnt_col+1)]
		x_digit += 1
	y_ticks=[]
	y_digit=max(0,int(-reso_y))
	while len(set(y_ticks))!=cnt_row+1:
		y_ticks = [("%."+str(y_digit)+"f")%(y_min+i*cellscale[1],) for i in range(cnt_row+1)]
		y_digit += 1
	plt.xticks(range(cnt_col+1), x_ticks)
	plt.yticks(range(cnt_row+1), y_ticks)
	fig.savefig(save_filename, bbox_inches='tight')
	fig.clf()
	plt.close('all')
	gc.collect()



