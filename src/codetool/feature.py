# -*- coding: UTF-8 -*-
# 根据图层返回集合列表

import arcpy


def to_list(dataset,field="SHAPE@"):
	res=[]
	cursor=arcpy.da.SearchCursor(dataset,[field])
	for row in cursor:
		res.append(row[0])
	del row,cursor
	return res

def to_set(dataset,field="SHAPE@"):
	res=set()
	cursor=arcpy.da.SearchCursor(dataset,[field])
	for row in cursor:
		res.add(row[0])
	del row,cursor
	return res

















