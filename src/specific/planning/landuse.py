# -*- coding: UTF-8 -*-
# planning tool
# landuse tool

import arcpy
import os.path
import sys
sys.path.append(os.path.split(__file__)[0]+"/../..")
import codetool.feature as af
from constants import LanduseMap
from constants import LanduseMapError
import xlwt
import copy




def summarize_area_to_excel(import_landuse, landuse_fields, export_xlsx, **excel_options):
	'''
	landuse_fields按照顺序依次在LanduseMap中寻找对应用地类型，均未找到时报错；
	excel_options控制表格细节：单位unit=[hm2(ha), km2, m2]; 条目title=[mc, dm, dm+mc]；剔除空项compact=[True, False]；总合项文字sum_caption=["合计", ...]；单一子类合并时注释子类solo_bracket=[True, False]
	'''
	#LanduseMap.use_GB50137() # 目前是手动修改兼容GB50137
	area_map = {}
	field_count = len(landuse_fields)
	cursor = arcpy.da.SearchCursor(import_landuse, ['SHAPE@']+landuse_fields)
	for row in cursor:
		for field_idx in range(1,field_count+1):
			lu = row[field_idx]
			if lu==None or lu=='': continue
			if lu[0] in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':
				if lu in LanduseMap.dm2mc:
					landuse = lu
					break
			else:
				if lu in LanduseMap.mc2dm:
					landuse = LanduseMap.mc2dm[lu]
					break
		else:
			#no break
			raise LanduseMapError(lu)
		area = row[0].area
		if landuse in area_map:
			area_map[landuse] += area
		else:
			area_map[landuse] =  area
	del row, cursor
	
	unit = excel_options.get("unit")
	if unit in ["ha","hm2"]:
		unit_division = 10000.0
	elif unit in ["km2"]:
		unit_division = 1000000.0
	else:
		unit_division = 1.0
	title = excel_options.get("title")
	if not isinstance(title,str):
		title_func = lambda x:" ".join([x,LanduseMap.dm2mc[x]])
	elif title.lower() in ["dm"]:
		title_func = lambda x:x
	elif title.lower() in ["mc"]:
		title_func = lambda x:LanduseMap.dm2mc[x]
	else:
		title_func = lambda x:" ".join([x,LanduseMap.dm2mc[x]])
	compact = excel_options.get("compact")
	sum_caption = excel_options.get("sum_caption")
	sum_caption = u"合计" if sum_caption == None else "%s"%(sum_caption,)
	solo_bracket = excel_options.get("solo_bracket")
	
	wb = xlwt.Workbook(encoding='utf8')
	ws = wb.add_sheet(u"用地面积统计", cell_overwrite_ok=True)
	style_center = xlwt.easyxf(num_format_str='0.00')
	alignment = xlwt.Alignment()
	alignment.vert = xlwt.Alignment.VERT_CENTER
	style_center.alignment = alignment
	style_ctbold = copy.deepcopy(style_center)
	style_ctbold.font.bold = True
	style_percent = copy.deepcopy(style_center)
	style_perbold = copy.deepcopy(style_ctbold)
	style_percent.num_format_str = '0.00%'
	style_perbold.num_format_str = '0.00%'
	
	total_area = 0.0
	for key in area_map:
		total_area += area_map[key]
	dm_list = LanduseMap.dm2mc.keys()
	dm_list.sort()
	area_map_list = area_map.keys()
	if compact:
		dm_list = [x for x in dm_list if x in area_map_list]
	dm_list.append("")
	row = 0
	prev_dm1 = ""
	prev_dm2 = ""
	prev_dm3 = ""
	first_dm1_row = -1
	first_dm2_row = -1
	dm0_sum_area = 0.0
	dm1_sum_area = 0.0
	dm2_sum_area = 0.0
	for dm3 in dm_list:
		dm1 = dm3[:2]
		dm2 = dm3[:4]
		if dm2!=prev_dm2:
			if row-first_dm2_row>1:
				row+=1
			if first_dm2_row>=0:
				if row-first_dm2_row>1:
					ws.write_merge(first_dm2_row, row-1, 1, 1, title_func(prev_dm2), style_center)
					ws.write(row-1, 2, sum_caption, style_ctbold)
					value_label = dm2_sum_area/unit_division
					ws.write(row-1, 3, value_label, style_ctbold)
					ws.write(row-1, 4, xlwt.Formula("10000*$d%d/%f"%(row, total_area)), style_perbold)
				else:
					if prev_dm3==prev_dm2 or (not solo_bracket):
						ws.write_merge(row-1, row-1, 1, 2, title_func(prev_dm2), style_center)
					else:
						ws.write_merge(row-1, row-1, 1, 2, "%s (%s)"%(title_func(prev_dm2),title_func(prev_dm3)), style_center)
			prev_dm2 = dm2
			first_dm2_row = row
			dm2_sum_area = 0.0
		else:
			ws.write(row, 1, title_func(dm2), style_center)
		if dm1!=prev_dm1:
			if row-first_dm1_row>1:
				first_dm2_row+=1 # 一类修改时二类肯定修改
				row+=1
			if first_dm1_row>=0:
				if row-first_dm1_row>1:
					ws.write_merge(first_dm1_row, row-1, 0, 0, title_func(prev_dm1), style_center)
					ws.write_merge(row-1, row-1, 1, 2, sum_caption, style_ctbold)
					value_label = dm1_sum_area/unit_division
					ws.write(row-1, 3, value_label, style_ctbold)
					ws.write(row-1, 4, xlwt.Formula("10000*$d%d/%f"%(row, total_area)), style_perbold)
				else:
					if prev_dm3==prev_dm1 or (not solo_bracket):
						ws.write_merge(row-1, row-1, 0, 2, title_func(prev_dm1), style_center)
					else:
						ws.write_merge(row-1, row-1, 0, 2, "%s (%s)"%(title_func(prev_dm1),title_func(prev_dm3)), style_center)
			prev_dm1 = dm1
			first_dm1_row = row
			dm1_sum_area = 0.0
		else:
			ws.write(row, 0, title_func(dm1), style_center)
		area = area_map.get(dm3)
		if dm3 in LanduseMap.dm2mc:
			ws.write(row, 2, title_func(dm3), style_center)
		if area!=None:
			dm0_sum_area += area
			dm1_sum_area += area
			dm2_sum_area += area
			value_label = area/unit_division
			ws.write(row, 3, value_label, style_center)
			ws.write(row, 4, xlwt.Formula("10000*$d%d/%f"%(row+1, total_area)), style_percent)
		else:
			ws.write(row, 3, 0.0, style_center)
			ws.write(row, 4, xlwt.Formula("10000*$d%d/%f"%(row+1, total_area)), style_percent)
		row += 1
		prev_dm3 = dm3
	ws.write_merge(row-1, row-1, 0, 2, sum_caption, style_ctbold)
	value_label = dm0_sum_area/unit_division
	ws.write(row-1, 3, value_label, style_ctbold)
	ws.write(row-1, 4, xlwt.Formula("10000*$d%d/%f"%(row, total_area)), style_perbold)
	
	
	wb.save(export_xlsx)
	print("hell")
	return area_map
	







