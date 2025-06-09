# -*- coding: UTF-8 -*-
import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.planning.landuse as lu

import_landuse  = arcpy.GetParameterAsText(0)
landuse_field_1 = arcpy.GetParameterAsText(1)
landuse_field_2 = arcpy.GetParameterAsText(2)
landuse_field_3 = arcpy.GetParameterAsText(3)
landuse_fields  = [landuse_field_1]
if landuse_field_2 and landuse_field_2!="": landuse_fields.insert(0, landuse_field_2)
if landuse_field_3 and landuse_field_3!="": landuse_fields.insert(0, landuse_field_3)
export_xlsx     = arcpy.GetParameterAsText(4)
unit_str        = arcpy.GetParameterAsText(5)
title_str       = arcpy.GetParameterAsText(6)
sumcap_str      = arcpy.GetParameterAsText(7)
compact         = arcpy.GetParameter(8)
bracket         = arcpy.GetParameter(9)
if unit_str == u'\u516c\u9877':
	unit_val = "hm2"
elif unit_str == u"\u5e73\u65b9\u7c73":
	unit_val = "m2"
else:
	unit_val = "km2"
if title_str == u"\u5730\u7c7b\u4ee3\u7801":
	title_val = "dm"
elif title_str == u"\u5730\u7c7b\u540d\u79f0":
	title_val = "mc"
else:
	title_val = "dm+mc"
arcpy.AddMessage(landuse_fields)
lu.summarize_area_to_excel(import_landuse, landuse_fields, export_xlsx, unit=unit_val, title=title_val, sum_caption=sumcap_str, compact=compact, solo_bracket=bracket)
