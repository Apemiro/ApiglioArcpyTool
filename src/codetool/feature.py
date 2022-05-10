# -*- coding: UTF-8 -*-
# 根据图层返回集合列表

import arcpy


def to_list(dataset):
	res=[]
	cursor=arcpy.da.SearchCursor(dataset,["SHAPE@"])
	for row in cursor:
		res.append(row[0])
	del row,cursor
	return res



















