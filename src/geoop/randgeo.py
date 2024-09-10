# -*- coding: UTF-8 -*-

import arcpy
import transform
import points
import geometry

from random import seed as randomize
from random import random as get_random

def points_on_polyline(polyline, number_of_points):
	if not isinstance(polyline, arcpy.Polyline):
		raise Exception("argument polyline is not an arcpy.Polyline")
	if polyline.length<=0:
		raise Exception("invald length of polyline")
	if number_of_points<=1:
		raise Exception("invald number of points (must greater than 1)")
	randomize()
	acc = 0.0
	steps = [0.0]
	for idx in range(number_of_points-1):
		step_length = get_random()
		acc += step_length
		steps.append(acc)
	ratio = polyline.length / acc
	return [polyline.positionAlongLine(st * ratio) for st in steps]

def points_in_extent(extent, number_of_points):
	if not isinstance(extent, arcpy.Extent):
		raise Exception("argument extent is not an arcpy.Extent")
	if extent.height*extent.width<=0:
		raise Exception("invald area of extent")
	randomize()
	x0 = extent.lowerLeft.X
	y0 = extent.lowerLeft.Y
	x1 = extent.upperRight.X
	y1 = extent.upperRight.Y
	result = []
	for idx in range(number_of_points):
		x = get_random()*(x1-x0)+x0
		y = get_random()*(y1-y0)+y0
		p = arcpy.Point(x,y)
		ptr = arcpy.PointGeometry(p)
		result.append(ptr)
	return result

def points_in_polygon(polygon, number_of_points):
	if not isinstance(polygon, arcpy.Polygon):
		raise Exception("argument polygon is not an arcpy.Polygon")
	if polygon.area<=0:
		raise Exception("invald area of polygon")
	if number_of_points<=1:
		raise Exception("invald number of points (must greater than 1)")
	randomize()
	return "暂不实现，需要使用三角剖分"





















