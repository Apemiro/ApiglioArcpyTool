# -*- coding: UTF-8 -*-
# villagene

import arcpy
import numpy
import scipy.cluster.hierarchy as hier
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import math
import os.path
import sys
import gc
sys.path.append(os.path.split(__file__)[0]+"/..")
import net
import codetool.feature
import codetool.dicts


def _decode_LSBI_(lsbi):
	res = set(lsbi.split("-"))
	if "" in res: res.remove("")
	return(res)

def _similarity_(v1,v2):
	u=len(v1.union(v2))
	if u==0:
		return(0.0)
	i=len(v1.intersection(v2))
	return(i/float(u))

# G_{i,j} = exp(\frac {ln 10 \cdot d_{i,j}} {-d_{0.1}})
# S_{i,j} = \frac{card(V_i \cap V_j)}{card(V_i \cup V_j)}
# D_{i,j} = \phi \cdot G_{i,j}+(1-\phi) \cdot S_{i,j}
# dist_std = G
# relation = S
# result = D
def village_comprehensive_relationship(points, fields, out_csv, dist_base, phi):
	distance = net.calc_geodistance_point(points)
	func = lambda d:math.exp(math.log(10)*d/-dist_base)
	dist_std = [[func(cell) for cell in row] for row in distance]
	relation = net.calc_fielddistance_point(points, fields, _decode_LSBI_, _similarity_)
	result = phi*numpy.array(dist_std) + (1-phi)*numpy.array(relation)
	f = open(out_csv,"w")
	for row in result.tolist():
		for cell in row:
			f.write(str(cell)+",")
		f.write("\n")
	f.close()

def hca_warning_func(x):
	print(x)

# out_fields = [(ngroup, out_field), ...]
def village_comprehensive_hca(points, fields, out_fig, dist_base, phi, label_field=None, out_fields=None, warning_func=hca_warning_func):
	distance = net.calc_geodistance_point(points)
	func = lambda d:math.exp(math.log(10)*d/-dist_base)
	dist_std = [[func(cell) for cell in row] for row in distance]
	relation = net.calc_fielddistance_point(points, fields, _decode_LSBI_, _similarity_)
	result = phi*numpy.array(dist_std) + (1-phi)*numpy.array(relation)
	hca = hier.linkage(result, "ward")
	count = len(hca)+1
	if label_field == None:
		labellist = range(1,count+1)
	else:
		labellist = codetool.feature.to_list(points, label_field)
	fig = plt.figure(figsize=[20,8])
	hier.dendrogram(hca,labels=labellist)
	fig.savefig(out_fig,dpi=800)
	fig.clf()
	plt.close()
	fieldnames = [x.name for x in arcpy.Describe(points).fields]
	if out_fields != None:
		for ngroup, out_field in out_fields:
			try:
				division = dendrogram_division_by_ngroup(hca,ngroup)
				identify = {}
				for idx,nodes in enumerate(division):
					for node in nodes:
						identify[node] = idx+1
				acc = 0
				if not out_field in fieldnames:
					arcpy.management.AddField(points, out_field, "LONG")
					fieldnames.append(out_field)
				cursor = arcpy.da.UpdateCursor(points,[out_field])
				for row in cursor:
					value = identify.get(acc)
					if value != None:
						cursor.updateRow([value])
					acc += 1
				del cursor
			except Exception, info:
				warning_func("无法将层次聚类结果分为"+str(ngroup)+"类，未输出结果。\n错误信息：")
				for info_str in info.args:
					warning_func(info_str)

# 几何级数划分
def geometric_rank(seq,ngroup,ratio):
	sequence = list(seq)
	sequence.sort()
	array_len = len(sequence)
	total_len = 0.0
	for i in range(ngroup):
		total_len += ratio**(i+1)
	ticks_delta = [ratio**(ngroup-x)/total_len for x in range(ngroup)]
	groups = []
	ltick = 0.0
	for i in range(ngroup):
		rge = [int(math.ceil(ltick*array_len))]
		ltick += ticks_delta[i]
		rge.append(int(math.ceil(ltick*array_len)))
		groups.append(rge)
	for pair in groups:
		if pair[0]==pair[1]:
			raise Exception("部分分组过小，请选择更接近1的底数或减小分类数。")
	return [[sequence[rge[0]],sequence[rge[1]]] for rge in groups[:-1]]+[[sequence[groups[-1][0]],None]]

# 几何级数划分，返回识别函数
def geometric_rank_function(seq,ngroup,ratio):
	rge = geometric_rank(seq,ngroup,ratio)
	def func(x):
		for i,r in enumerate(rge):
			bol = True
			if r[0]!=None: bol = bol and (x>=r[0])
			if r[1]!=None: bol = bol and (x<r[1])
			if bol: return i
		return None
	return func

def __recur_cluster(id,dict_of_cluster,used_cluster):
	used_cluster.append(id)
	clu = dict_of_cluster.get(id)
	if clu==None: return [id]
	n1 = clu["nodes"][0]
	n2 = clu["nodes"][1]
	return __recur_cluster(n1,dict_of_cluster,used_cluster)+__recur_cluster(n2,dict_of_cluster,used_cluster)

# 根据level划分树状图
def dendrogram_division_by_level(dendrogram,level):
	clusters = {}
	nelement = len(dendrogram)+1
	for i,cluster in enumerate(dendrogram):
		tmp_dict = {}
		tmp_dict["nodes"] = [int(x) for x in cluster[:2]]
		tmp_dict["level"] = cluster[2]
		tmp_dict["count"] = cluster[3]
		clusters[nelement+i] = tmp_dict
	reverse_dg = dendrogram.tolist()
	reverse_dg.reverse()
	used_cluster = []
	result = []
	for i,cluster in enumerate(reverse_dg):
		cid = 2*nelement-i-2
		if cluster[2]>level:
			used_cluster.append(cid)
			continue
		if not cid in used_cluster: result.append(__recur_cluster(cid,clusters,used_cluster))
	return result

# 根据组数划分树状图
def dendrogram_division_by_ngroup(dendrogram,ngroup):
	if ngroup<2: raise Exception("至少分为两个组。")
	level = dendrogram[-ngroup][2]
	return dendrogram_division_by_level(dendrogram,level)

def __cmap(length):
	# colors = ["red","yellow","green","cyan","violet"]
	# colors = ["blue","green","lime","cyan"]
	h = 0.75
	l = 0.25
	colors = [(h,l,l),(h,h,l),(l,h,l),(l,h,h),(l,l,h),(h,l,h)]
	return colors[:length]

# 分组统计基因类型并绘制饼图
# 写的真臭
def grouped_gene(points, gene_field, grouped_field, out_img, ext=".png"):
	list_of_dict = codetool.feature.to_dict(points)
	tmplist = []
	for point in list_of_dict:
		genome = set(point[gene_field].replace(" ","").split("-"))
		if "" in genome:
			genome.remove("")
		tmplist.append((point[grouped_field],genome))
	tmpdict = {}
	for group, gene in tmplist:
		if group in tmpdict:
			tmpdict[group].append(gene)
		else:
			tmpdict[group] = []
	proto_entries = ["L1","L2","L3","S1","S2","S3","B1","B2","B3","B4","B5","B6","B7","I1","I2","I3"]
	ncol = 5
	nrow = int(math.ceil(len(proto_entries) / float(ncol)))
	groups = tmpdict.keys()
	fig_list = []
	for grp in groups:
		fig = plt.figure()
		ino = 1
		for entry in proto_entries:
			plt.subplot(nrow, ncol, ino)
			plt.title(entry)
			protos = [entry+str(x) for x in range(1,5)]
			stat = {}
			void = 0
			for proto in protos:
				stat[proto]=0
			for gene in tmpdict[grp]:
				all_void = True
				for proto in protos:
					if proto in gene:
						all_void = False
						stat[proto]+=1
				if all_void:
					void+=1
			data = stat.items()
			data = list(filter(lambda x:x[1]>0,data))
			data.sort(key=lambda x:x[1],reverse=True)
			_x = [x[1] for x in data]
			_labels = [x[0] for x in data]
			_colors = __cmap(len(data))
			if void>0:
				_x = _x+[void]
				_labels = _labels+[""]
				_colors = _colors+["gray"]
			plt.pie(_x, labels=_labels, wedgeprops={"width":0.3,"edgecolor":"white"}, radius=0.7, colors=_colors)
			ino += 1
		fig.suptitle("Group #"+str(grp))
		fig.savefig(out_img+str(grp)+ext)
		fig.clf()
		plt.close('all')
		gc.collect()


# 分组统计基因类型并绘制计数网格图
def grid_gene(points, gene_field, grouped_field, out_img, colorsmap=None):
	vills = codetool.feature.to_dict(points)
	stats = {}
	groups = []
	for vill in vills:
		grp = vill[grouped_field]
		genome = set(vill[gene_field].replace(" ","").split("-"))
		if "" in genome: genome.remove("")
		if not grp in stats:
			stats[grp]={}
			groups.append(grp)
		for proto in genome:
			if not proto in stats[grp]:
				stats[grp][proto]=1
			else:
				stats[grp][proto]+=1
	groups.sort()
	groups_pop = {g:float(len(stats[g])) for g in groups}
	proto_entries = ["L1","L2","L3","S1","S2","S3","B1","B2","B3","B4","B5","B6","B7","I1","I2","I3"]
	protos =  ["L11","L12","L13","L14","L21","L22","L23","L24","L31","L32","L33","L34"]+[" "]
	protos += ["S11","S12","S13","S21","S22","S23","S31","S32","S33"]+[" "]
	protos += ["B11","B12","B13","B21","B22","B23","B31","B32","B33","B34","B41","B42","B43","B51","B52","B53","B61","B62","B63","B71","B72","B73"]+[" "]
	protos += ["I11","I12","I13","I21","I22","I23","I31","I32","I33"]
	protos.reverse()
	data = []
	for proto in protos:
		row=[]
		for grp in groups:
			count = stats[grp].get(proto)
			grpct = groups_pop[grp]
			if count==None: count=0
			if grpct != 0:
				row.append(count/groups_pop[grp])
			else:
				row.append(0)
		data.append(row)
	xlen = len(groups)
	ylen = len(protos)
	fig, axs = plt.subplots(figsize=(xlen*1.25,20))
	if colorsmap == None:
		colorsmap = mpc.LinearSegmentedColormap.from_list("villband",[(1,1,1),(0.75,0,0)])
	psm = axs.pcolormesh(data, cmap = colorsmap, shading='nearest')
	# psm = axs.imshow(data, cmap = colorsmap, interpolation = 'none')
	fig.colorbar(psm, ax=axs)
	plt.xlim(0,xlen)
	plt.ylim(0,ylen)
	plt.xlabel(grouped_field)
	plt.ylabel("prototype")
	plt.xticks(range(xlen), groups)
	plt.yticks(range(ylen), protos)
	fig.savefig(out_img)
	fig.clf()
	plt.close('all')
	gc.collect()
	


# 分组统计基因类型并输出事件图表
def grouped_eventplot(points, value_field, grouped_field, out_img, ext=".png"):
	list_of_dict = codetool.feature.to_dict(points)
	dict_of_listdict = codetool.dicts.group_by(list_of_dict,lambda x:x.get(grouped_field))
	groups = dict_of_listdict.keys()
	grplen = len(groups)
	fig = plt.figure()
	data = [[x.get(value_field) for x in dict_of_listdict[key]] for key in groups]
	plt.eventplot(data, orientation="vertical", linewidth=1.25)
	plt.xticks(range(grplen),groups)
	plt.xlabel(grouped_field)
	plt.ylabel(value_field)
	fig.savefig(out_img+ext)
	fig.clf()
	plt.close('all')
	gc.collect()


