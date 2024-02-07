# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import math
import gc


def lines(data, save_filename, xlabel, ylabel, figsize=None, dpi=300):
	if figsize == None:
		fig = plt.figure()
	else:
		fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.plot(data)
	fig.savefig(save_filename, dpi=dpi)
	fig.clf()
	plt.close()
	gc.collect()

def grids(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, colorsmap=None, cellscale=None):
	'''argument data need list of tuple (x, y)'''
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
		cnt_col = int((population * proportion)**0.5)+1
		cnt_row = int((population / proportion)**0.5)+1
		cellscale = (range_x / cnt_col, range_y / cnt_row)
	else:
		cnt_col = int(range_x / cellscale[0])+1
		cnt_row = int(range_y / cellscale[1])+1
		proportion = cellscale[0] / float(cellscale[1])
	
	grid_data = []
	for row in range(cnt_row):
		grid_data.append([0 for x in range(cnt_col)])
	for datum in data:
		grid_x = int(cnt_col * (datum[0] - x_min) / range_x)
		grid_y = int(cnt_row * (datum[1] - y_min) / range_y)
		if grid_x >= cnt_col: grid_x = cnt_col-1
		if grid_y >= cnt_row: grid_y = cnt_row-1
		grid_data[grid_y][grid_x] += 1
	
	if figsize==None:
		fig_w = cnt_col * 0.5
		fig_h = cnt_row * 0.5
		if fig_w <  1: fig_w = 1
		if fig_w > 50: fig_w = 50
		if fig_h <  1: fig_h = 1
		if fig_h > 50: fig_h = 50
		figsize = (fig_w+2, fig_h)
	fig, axs = plt.subplots(figsize=figsize)
	if colorsmap == None:
		colorsmap = mpc.LinearSegmentedColormap.from_list("villband",[(1,1,1),(0.75,0,0)])
	psm = axs.pcolormesh(grid_data, cmap = colorsmap, shading='nearest')
	axs.grid(True, linestyle='-', color='White', linewidth=3)
	fig.colorbar(psm, ax=axs)
	plt.xlim(0, cnt_col)
	plt.ylim(0, cnt_row)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	reso_x = -int(math.log10(cellscale[0]))
	reso_y = -int(math.log10(cellscale[1]))
	if reso_x<0: reso_x=0
	if reso_y<0: reso_y=0
	plt.xticks(range(cnt_col+1), [("%."+str(reso_x)+"f")%(x_min+i*cellscale[0],) for i in range(cnt_col+1)])
	plt.yticks(range(cnt_row+1), [("%."+str(reso_y)+"f")%(x_min+i*cellscale[1],) for i in range(cnt_row+1)])
	fig.savefig(save_filename)
	fig.clf()
	plt.close('all')
	gc.collect()



