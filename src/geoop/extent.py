# -*- coding: UTF-8 -*-
# 与范围对象（Extent）有关的计算
import arcpy

def extent_union(a, b):
	return arcpy.Extent( \
		min(a.XMin, b.XMin), min(a.YMin, b.YMin), \
		max(a.XMax, b.XMax), max(a.YMax, b.YMax), \
		min(a.ZMin, b.ZMin), max(a.ZMax, b.ZMax), \
		min(a.MMin, b.XMin), max(a.MMax, b.MMax)  \
	)

def extent_intersect(a, b):
	return arcpy.Extent( \
		max(a.XMin, b.XMin), max(a.YMin, b.YMin), \
		min(a.XMax, b.XMax), min(a.YMax, b.YMax), \
		max(a.ZMin, b.ZMin), min(a.ZMax, b.ZMax), \
		max(a.MMin, b.XMin), min(a.MMax, b.MMax)  \
	)

def extent_offset(ext, dist):
	return arcpy.Extent( \
		ext.XMin - dist, ext.YMin - dist, \
		ext.XMax + dist, ext.YMax + dist, \
		ext.ZMin, ext.ZMax, \
		ext.MMin, ext.MMax \
	)

def extent_scale(ext, factor):
	wInc = factor * (ext.XMax - ext.XMin)
	hInc = factor * (ext.YMax - ext.YMin)
	return arcpy.Extent( \
		ext.XMin - wInc, ext.YMin - hInc, \
		ext.XMax + wInc, ext.YMax + hInc, \
		ext.ZMin, ext.ZMax, \
		ext.MMin, ext.MMax \
	)

















