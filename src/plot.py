# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.font_manager as ftm
import matplotlib.gridspec as mgs
import math
import numpy
import gc
import os
p=os.path.split(__file__)[0]
ch_font = ftm.FontProperties(fname=p+'/../assets/fonts/simhei.ttf')

line_styles = ['solid','dashed','dotted','dashdot']
colors = [(0.12,0.47,0.71), (0.68,0.78,0.91), (1.00,0.50,0.05), (1.00,0.73,0.47), (0.17,0.63,0.17), (0.60,0.87,0.54), (0.84,0.15,0.16), (1.00,0.60,0.59), (0.58,0.40,0.74), (0.77,0.69,0.84), (0.55,0.34,0.29), (0.77,0.61,0.58), (0.89,0.47,0.76), (0.97,0.71,0.82), (0.50,0.50,0.50), (0.78,0.78,0.78), (0.74,0.74,0.13), (0.86,0.86,0.55), (0.09,0.75,0.81), (0.62,0.85,0.90)]


def __floor(num,frac):
	return num - num%frac
def __ceil(num,frac):
	return num - num%frac + frac

def list_enum(list_of_list, output_length):
	count_total = len(list_of_list)
	count_of_grp = [len(x) for x in list_of_list]
	acc = [0 for x in range(count_total)]
	result = []
	while len(result)<output_length:
		elem = [(list_of_list[idx][pos]) for idx, pos in enumerate(acc)]
		result.append(elem)
		acc[-1]+=1
		for idx in range(count_total-1,-1,-1):
			if acc[idx]>=count_of_grp[idx]:
				acc[idx]=0
				if idx>0: acc[idx-1]+=1
	return result

def bandplot(subplot_widths, projections=None, figsize=None, gap=0.5):
	'''
	argument subplot_widths need list of integer.
	argument projections need list of string, "cart" or "polar".
	return list of matplotlib.axis
	'''
	if min(subplot_widths)<1 or max(subplot_widths)>10:
		raise Exception("every subplot_width has to be limited between 1 to 10.")
	ncol = sum(subplot_widths)
	if projections==None:
		projections = ["cart"]*ncol
	spec = mgs.GridSpec(nrows=1, ncols=ncol, hspace=gap, wspace=gap)
	'''left=0.1, right=0.9, top=0.9, bottom=0.1'''
	fig = plt.figure(figsize=figsize)
	left = 0
	axes = []
	while left < ncol:
		subplot_index = len(axes)
		width = subplot_widths[subplot_index]
		projection = 'polar' if projections[subplot_index].lower()=='polar' else None
		new_axis = fig.add_subplot(spec[0,left:left+width],projection=projection)
		axes.append(new_axis)
		left += width
	return fig, axes

def saveplot(fig, save_filename, dpi=300):
	fig.savefig(save_filename, dpi=dpi, bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

def lines(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, xlim=None, ylim=None, axis=None):
	if axis==None:
		if figsize == None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=figsize)
		ax = fig.add_subplot(111)
	else:
		ax = axis
		fig = axis.figure
	ax.set_xlabel(xlabel, fontproperties=ch_font)
	ax.set_ylabel(ylabel, fontproperties=ch_font)
	if xlim != None:
		ax.set_xlim(xlim[0],xlim[1])
	if ylim != None:
		ax.set_ylim(ylim[0],ylim[1])
	ax.plot(data)
	if axis==None:
		fig.savefig(save_filename, dpi=dpi)
		fig.clf()
		plt.close()
		gc.collect()

def percentile(data, save_filename, ylabel, legends, legend_ncols=1, figsize=None, dpi=300, axis=None):
	'''
	argument data need list of list of decimal values. 
	this function sorts each group of values and plot by percentile rank.
	'''
	max_value=float('-Inf')
	min_value=float('+Inf')
	max_length=0
	percentile_groups = []
	for grp in data:
		cnt = len(grp)
		if max_length < cnt: max_length = cnt
		cnt = float(cnt-1)
		tmp = list(grp)
		tmp.sort()
		percentile_groups.append([(index/cnt, value) for index,value in enumerate(tmp)])
		max_in_tmp = max(tmp)
		min_in_tmp = min(tmp)
		if max_in_tmp > max_value: max_value = max_in_tmp
		if min_in_tmp < min_value: min_value = min_in_tmp
	if axis==None:
		if figsize == None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=figsize)
		ax = fig.add_subplot(111)
	else:
		ax = axis
		fig = axis.figure
	ax.set_xlabel(u'\u4f4d\u5e8f', fontproperties=ch_font)
	ax.set_ylabel(ylabel, fontproperties=ch_font)
	ax.set_xlim(0,1)
	ax.set_ylim(min_value, max_value)
	
	
	xs = []
	ys = []
	for idx in range(max_length):
		xs.append([])
		ys.append([])
		for grp in percentile_groups:
			if idx<len(grp):
				xs[-1].append(grp[idx][0])
				ys[-1].append(grp[idx][1])
			else:
				xs[-1].append(None)
				ys[-1].append(None)
	lines = ax.plot(xs, ys)
	# style_color = list_enum([line_styles, colors], len(percentile_groups))
	# lines = []
	# for idx, grp in enumerate(percentile_groups):
		# lines.append(ax.plot(zip(*grp),linestyle=style_color[0], color=style_color[1]))


	ax.legend(lines, legends, prop=ch_font, ncol=legend_ncols, loc="upper left")
	if axis==None:
		fig.savefig(save_filename, dpi=dpi)
		fig.clf()
		plt.close()
		gc.collect()

def scatters(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, cmap='magma_r', xlim=None, ylim=None, axis=None, s=1):
	'''
	argument data need list of tuple (x, y, depth).
	'''
	if axis==None:
		if figsize == None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=figsize)
		ax = fig.add_subplot(111)
	else:
		ax = axis
		fig = axis.figure
	ax.set_xlabel(xlabel, fontproperties=ch_font)
	ax.set_ylabel(ylabel, fontproperties=ch_font)
	if xlim != None:
		ax.set_xlim(xlim[0],xlim[1])
	if ylim != None:
		ax.set_ylim(ylim[0],ylim[1])
	xs, ys, depths = zip(*data)
	ax.scatter(xs, ys, s=s, c=depths, cmap=cmap, edgecolor='none')
	if axis==None:
		fig.savefig(save_filename, dpi=dpi)
		fig.clf()
		plt.close()
		gc.collect()

def vectors(data, save_filename, figsize=None, dpi=300, data_mode='radian', axis=None):
	'''
	argument data need list of tuple.
	tuple format: 
	  (radian, radius) when data_mode="radian" / "r"; 
	  (degree, radius) when data_mode="degree" / "d"; 
	  (xcoord, ycoord) when data_mode="cartesian" / "xy". 
	'''
	if axis==None:
		if figsize == None:
			fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
		else:
			fig, ax = plt.subplots(subplot_kw={'projection':'polar'}, figsize=figsize)
	else:
		ax = axis
		fig = axis.figure
	vec_count = len(data)
	mode_str = data_mode.lower()
	if mode_str in ['d','deg','degree']:
		xs_deg, ys = zip(*data)
		xs = [x/180.0*math.pi for x in xs_deg]
	elif mode_str in ['r','rad','radian']:
		xs, ys = zip(*data)
	else:
		xs, ys = [],[]
		for x,y in data:
			rho = (x**2+y**2)**0.5
			phi = numpy.arctan2(y,x)
			xs.append(phi)
			ys.append(rho)
	ax.plot([[0]*vec_count,xs],[[0]*vec_count,ys],color="red")
	if axis==None:
		fig.savefig(save_filename, dpi=dpi)
		fig.clf()
		plt.close()
		gc.collect()

def skyline(data, save_filename, figsize=None, dpi=300, data_mode='radian', axis=None):
	'''
	argument data need list of tuple.
	tuple format: 
	  (radian, radius) when data_mode="radian" / "r"; 
	  (degree, radius) when data_mode="degree" / "d"; 
	  (xcoord, ycoord) when data_mode="cartesian" / "xy". 
	'''
	if axis==None:
		if figsize == None:
			fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
		else:
			fig, ax = plt.subplots(subplot_kw={'projection':'polar'}, figsize=figsize)
	else:
		ax = axis
		fig = axis.figure
	vec_count = len(data)
	mode_str = data_mode.lower()
	if mode_str in ['d','deg','degree']:
		xs_deg, ys = zip(*data)
		xs = [x/180.0*math.pi for x in xs_deg]
	elif mode_str in ['r','rad','radian']:
		xs, ys = zip(*data)
	else:
		xs, ys = [],[]
		for x,y in data:
			rho = (x**2+y**2)**0.5
			phi = numpy.arctan2(y,x)
			xs.append(phi)
			ys.append(rho)
	ax.plot(xs,ys)
	if axis==None:
		fig.savefig(save_filename, dpi=dpi)
		fig.clf()
		plt.close()
		gc.collect()
	return numpy.array(zip(xs,ys))

def grids(data, save_filename, xlabel, ylabel, figsize=None, dpi=300, colorsmap=None, cellscale=None, key=lambda arr:sum(arr), datarange=None, cellcount=[10,10]):
	'''
	argument data need list of tuple (x, y).
	argument cellscale is enabled only when datarange is None.
	argument cellcount is enabled only when datarange is NOT None.
	argument datarange need a 4-element list [xmin, ymin, xmax, ymax]
	argument cellcount need list [ncol, nrow]
	'''
	
	#计算数据边界
	if datarange==None:
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
		
		disp_x_min = x_min
		disp_y_min = y_min
		disp_x_range = range_x
		disp_y_range = range_y
		disp_cnt_col = cnt_col
		disp_cnt_row = cnt_row
	else:
		disp_x_min = datarange[0]
		disp_y_min = datarange[1]
		disp_x_max = datarange[2]
		disp_y_max = datarange[3]
		if disp_x_max<=disp_x_min: raise Exception("invalid datarange: xmax<=xmin")
		if disp_y_max<=disp_y_min: raise Exception("invalid datarange: ymax<=ymin")
		disp_cnt_col = cellcount[0]
		disp_cnt_row = cellcount[1]
		if type(disp_cnt_col*disp_cnt_row)!=int: raise Exception("invalid cellcount: int type expected")
		disp_x_range = float(disp_x_max - disp_x_min)
		disp_y_range = float(disp_y_max - disp_y_min)
		cellscale = (disp_x_range / disp_cnt_col, disp_y_range / disp_cnt_row)
		reso_x = math.floor(math.log10(cellscale[0]))
		reso_y = math.floor(math.log10(cellscale[1]))
		
	
	#统计网格中的数据
	grid_data = []
	for row in range(disp_cnt_row):
		grid_data.append([[] for x in range(disp_cnt_col)])
	for datum in data:
		grid_x = int(disp_cnt_col * (datum[0] - disp_x_min) / disp_x_range)
		grid_y = int(disp_cnt_row * (datum[1] - disp_y_min) / disp_y_range)
		if not (0<=grid_x<disp_cnt_col): continue
		if not (0<=grid_y<disp_cnt_row): continue
		if len(datum)<3:
			grid_data[grid_y][grid_x].append(1)
		else:
			grid_data[grid_y][grid_x].append(datum[2])
	plot_data = [[key(elem) for elem in row] for row in grid_data]
	
	#计算画幅大小
	if figsize==None:
		fig_w = disp_cnt_col * 0.5
		fig_h = disp_cnt_row * 0.5
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
	plt.xlim(0, disp_cnt_col)
	plt.ylim(0, disp_cnt_row)
	plt.xlabel(xlabel, fontproperties=ch_font)
	plt.ylabel(ylabel, fontproperties=ch_font)
	x_ticks=[]
	x_digit=max(0,int(-reso_x))
	while len(set(x_ticks))!=disp_cnt_col+1:
		x_ticks = [("%."+str(x_digit)+"f")%(disp_x_min+i*cellscale[0],) for i in range(disp_cnt_col+1)]
		x_digit += 1
	y_ticks=[]
	y_digit=max(0,int(-reso_y))
	while len(set(y_ticks))!=disp_cnt_row+1:
		y_ticks = [("%."+str(y_digit)+"f")%(disp_y_min+i*cellscale[1],) for i in range(disp_cnt_row+1)]
		y_digit += 1
	plt.xticks(range(disp_cnt_col+1), x_ticks)
	plt.yticks(range(disp_cnt_row+1), y_ticks)
	fig.savefig(save_filename, bbox_inches='tight')
	fig.clf()
	plt.close('all')
	gc.collect()



