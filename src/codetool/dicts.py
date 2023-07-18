# -*- coding: UTF-8 -*-
# 把要素类当做list of dict来操作

import arcpy
import arcpy.sa

# 用一个字段名的值索引另一个字段的值
def unique(table,key_header,value_header):
	res={}
	for row in table:
		if not key_header in row.keys():
			raise Exception("Cannot find "+key_header+" header.")
		if not value_header in row.keys():
			raise Exception("Cannot find "+value_header+" header.")
		k = row[key_header]
		v = row[value_header]
		if k in res.keys():
			raise Exception(k+" is not unique value for key value.")
		else:
			res[k]=v
	return res

# 根据条件返回子表
def filter(table,key_header,condition=lambda x:x):
	res=[]
	for row in table:
		if not key_header in row.keys():
			raise Exception("Cannot find "+key_header+" header.")
		if condition(row[key_header]):
			res.append(row)
	return res

# 返回字段列表
def fields(table):
	res=set([])
	for row in table:
		res = res.union(set(row.keys()))
	res = list(res)
	res.sort()
	return res

# 返回字段值列表
def values(table,key_header):
	res=[]
	for row in table:
		if not key_header in row.keys():
			raise Exception("Cannot find "+key_header+" header.")
		res.append(row[key_header])
	return res

def counter(list_value):
	res={}
	for element in list_value:
		if element in res.keys():
			res[element]+=1
		else:
			res[element]=1
	return(res)

# 按照条件分类
def group_by(table, key):
	res={}
	for row in table:
		grouped_value = key(row)
		if grouped_value in res.keys():
			res[grouped_value].append(row)
		else:
			res[grouped_value]=[row]
	return res

'''

sys.path.append("k:/python")
import apiglio.src.net
import apiglio.src.codetool.feature
import apiglio.src.codetool.dicts

recs = apiglio.src.codetool.feature.to_dict("class_20230401")

tmp = apiglio.src.codetool.dicts.filter(recs,"calc_str",lambda x:x=="b2a1b")
tlt = [list(eval(i)) for i in apiglio.src.codetool.dicts.values(tmp,"code")]
tol = reduce(lambda x,y:x+y,tlt)
counter(tol)

'''

















