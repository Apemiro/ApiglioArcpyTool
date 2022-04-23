# -*- coding: UTF-8 -*-
# data frame tool
import arcpy

def cmxd():
	return arcpy.mapping.MapDocument("CURRENT")


def lyrs():
	return arcpy.mapping.ListLayers(cmxd(),"*")
	