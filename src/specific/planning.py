# -*- coding: UTF-8 -*-
# planning tool

import arcpy
import os.path
import sys
sys.path.append(os.path.split(__file__)[0]+"/..")
import codetool.feature as af




def __bae(x):
	vs=x.getPart()[0]
	return [vs[0],vs[len(vs)-1]]

def __dist(a,b):
	return((a.X-b.X)**2+(a.Y-b.Y)**2)**0.5

def __find_nearest(target_point, points):
	res = None
	mindist = float('infinity')
	for ptmp in points:
		dtmp = __dist(ptmp, target_point)
		if dtmp<mindist:
			res = ptmp
			mindist = dtmp
	return res


# road

def edge_line_closure(input_lines, output_lines, max_dist=None):
	'''在线要素中找到所有线要素端头，筛选出其中互为最近点的点对创建短线。建议将断线整合后再使用此工具，避免生成一些重合线。'''
	lines = af.to_list(input_lines)
	thrum = []
	for line in lines:
		thrum += __bae(line)
	points_uniq = [arcpy.Point(*p.split(",")) for p in set(["%f,%f"%(x.X,x.Y) for x in thrum])]
	
	nearest_map = {}
	for point in points_uniq:
		other_points = [p for p in points_uniq if p != point]
		nearest = __find_nearest(point, other_points)
		nearest_map[point] = nearest

	mutual_pairs = set()
	for point_a, point_b in nearest_map.items():
		if nearest_map.get(point_b, None) == point_a:
			pair = tuple(sorted([point_a, point_b], key=lambda x: (x.X, x.Y)))
			mutual_pairs.add(pair)

	if max_dist==None:
		max_dist = float('infinity')
	lines = []
	for pair in mutual_pairs:
		if __dist(*pair)>max_dist: continue
		lines.append(arcpy.Polyline(arcpy.Array(pair)))

	all_lines = af.to_dict(input_lines)
	all_lines += [{"SHAPE@":x} for x in lines]
	fpath, fname = os.path.split(output_lines)
	sr = arcpy.Describe(input_lines).spatialReference.ExportToString()
	af.dict_to_file(all_lines, dataset=fname, path=fpath, spatial_reference=sr)
















