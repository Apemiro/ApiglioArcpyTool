# -*- coding: UTF-8 -*-
# villagene

import arcpy
import numpy
import math
import os.path
import sys
sys.path.append(os.path.split(__file__)[0]+"/..")
import net


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

