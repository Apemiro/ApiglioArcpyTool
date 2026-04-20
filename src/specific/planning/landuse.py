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




def summarize_area_to_excel(import_landuse, landuse_fields, export_xlsx, landuse_map='TSP', **excel_options):
	'''
	landuse_fields按照顺序依次在LanduseMap中寻找对应用地类型，均未找到时报错；
	excel_options控制表格细节：单位unit=[hm2(ha), km2, m2]; 条目title=[mc, dm, dm+mc]；剔除空项compact=[True, False]；总合项文字sum_caption=["合计", ...]；单一子类合并时注释子类solo_bracket=[True, False]
	'''
	LanduseMap.use_switch(landuse_map)
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
	return area_map

# 由gemini改写自summarize_area_to_excel，人工改写
def summarize_area_to_excel_2(import_landuse, landuse_fields, export_xlsx, district_field=None, floor_area_field=None, landuse_map='TSP', **excel_options):
	LanduseMap.use_switch(landuse_map)
	
	# 1. 统计数据初始化
	dist_area_map = {u"合计": {}}
	dist_floor_map = {u"合计": {}}

	# 字段校验与构造
	exist_fields = [f.name.lower() for f in arcpy.ListFields(import_landuse)]
	search_fields = ['SHAPE@'] + landuse_fields
	
	dist_idx = -1
	if district_field and district_field.lower() in exist_fields:
		search_fields.append(district_field)
		dist_idx = len(search_fields) - 1

	floor_idx = -1
	if floor_area_field and floor_area_field.lower() in exist_fields:
		search_fields.append(floor_area_field)
		floor_idx = len(search_fields) - 1

	with arcpy.da.SearchCursor(import_landuse, search_fields) as cursor:
		for row in cursor:
			dist_name = unicode(row[dist_idx]).strip() if dist_idx != -1 and row[dist_idx] is not None else None
			
			landuse = None
			for field_idx in range(1, len(landuse_fields) + 1):
				lu = row[field_idx]
				if not lu: continue
				lu = unicode(lu).strip()
				if lu[0] in u'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':
					if lu in LanduseMap.dm2mc: landuse = lu; break
				else:
					if lu in LanduseMap.mc2dm: landuse = LanduseMap.mc2dm[lu]; break
			
			if landuse:
				area_val = row[0].area
				f_val = 0.0
				if floor_idx != -1 and row[floor_idx] is not None:
					try: f_val = float(row[floor_idx])
					except: f_val = 0.0
				
				# 累加数据
				for m in [dist_area_map, dist_floor_map]:
					target = m[u"合计"]
					val = area_val if m == dist_area_map else f_val
					target[landuse] = target.get(landuse, 0.0) + val
					if dist_name:
						if dist_name not in m: m[dist_name] = {}
						m[dist_name][landuse] = m[dist_name].get(landuse, 0.0) + val

	# 2. 参数与样式设置
	unit_division = {"ha": 10000.0, "hm2": 10000.0, "km2": 1000000.0}.get(excel_options.get("unit"), 10000.0)
	unit_label = excel_options.get("unit", u"公顷").replace("2", u"²")
	compact, sum_caption = excel_options.get("compact", False), excel_options.get("sum_caption", u"其中")
	title_mode = excel_options.get("title", "dm+mc")
	get_title = {"dm": lambda x: x, "mc": lambda x: LanduseMap.dm2mc[x]}.get(title_mode, lambda x: u"%s(%s)" % (LanduseMap.dm2mc[x], x))
	title_str = {u"dm": u"用地代码", u"mc": u"用地名称"}.get(title_mode, u"用地名称(用地代码)")

	wb = xlwt.Workbook(encoding='utf8')
	style_bold = xlwt.easyxf('font: name Arial, bold on; align: vert center, horz left')
	style_normal = xlwt.easyxf('font: name Arial; align: vert center, horz left')
	style_num = xlwt.easyxf('font: name Arial; align: vert center, horz center', num_format_str='0.00')
	style_num_bold = xlwt.easyxf('font: name Arial, bold on; align: vert center, horz center', num_format_str='0.00')
	style_pct = xlwt.easyxf('font: name Arial; align: vert center, horz center', num_format_str='0.00%')
	style_pct_bold = xlwt.easyxf('font: name Arial, bold on; align: vert center, horz center', num_format_str='0.00%')

	# 3. 循环生成各分区 Sheet
	all_sheets = sorted(dist_area_map.keys(), key=lambda x: x != u"合计")
	for sheet_name in all_sheets:
		area_map = dist_area_map[sheet_name]
		floor_map = dist_floor_map.get(sheet_name, {})
		ws = wb.add_sheet(sheet_name, cell_overwrite_ok=True)
		
		# 动态列索引定义
		has_floor = (floor_idx != -1)
		# A, B, C 为用地名称
		col_area = 3  # D列
		col_pct = 4   # E列
		col_floor = 5 if has_floor else None # F列 (如果有)
		col_area_let = "D"
		col_floor_let = "F"

		# 写入表头
		headers = [u"一级类", u"二级类", u"三级类", u"用地面积(%s)" % unit_label]
		headers.append(u"占比")
		if has_floor: headers.append(u"建筑面积(m²)")
		for i, h in enumerate(headers): ws.write(0, i, h, style_bold)
		ws.write_merge(0, 0, 0, 2, title_str, style_bold)

		# 逻辑计算
		active_keys = {k for k in area_map if area_map[k] > 0}
		valid_keys = {p for k in active_keys for p in [k[:2], k[:4], k] if p in LanduseMap.dm2mc} if compact else set(LanduseMap.dm2mc.keys())
		curr_row, d1_row_refs, bold_rows = 1, [], []
		dm1_list = sorted([d for d in valid_keys if len(d) == 2])

		for d1 in dm1_list:
			d1_area = sum([v for k, v in area_map.items() if k.startswith(d1)])
			d1_floor = sum([v for k, v in floor_map.items() if k.startswith(d1)])
			if d1_area <= 0 and compact: continue

			d1_p_row = curr_row
			d1_row_refs.append(curr_row + 1)
			bold_rows.append(curr_row + 1)
			subs_d2 = sorted([d for d in valid_keys if len(d) == 4 and d.startswith(d1)])

			if len(subs_d2) == 1 and compact:
				d2_lone = subs_d2[0]
				subs_d3_lone = sorted([d for d in valid_keys if len(d) > 4 and d.startswith(d2_lone)])
				disp = u"%s [%s]" % (get_title(d1), get_title(d2_lone))
				if len(subs_d3_lone) == 1: disp += u" [%s]" % get_title(subs_d3_lone[0])
				ws.write_merge(curr_row, curr_row, 0, 2, disp, style_bold)
				ws.write(curr_row, col_area, d1_area / unit_division, style_num_bold)
				if has_floor: ws.write(curr_row, col_floor, d1_floor, style_num_bold)
				curr_row += 1
			else:
				ws.write_merge(curr_row, curr_row, 0, 2, get_title(d1), style_bold)
				curr_row += 1
				if subs_d2:
					d2_refs, sub_start_d1 = [], curr_row
					for d2 in subs_d2:
						d2_a = sum([v for k, v in area_map.items() if k.startswith(d2)])
						d2_f = sum([v for k, v in floor_map.items() if k.startswith(d2)])
						d2_p_row = curr_row
						d2_refs.append(curr_row + 1)
						subs_d3 = sorted([d for d in valid_keys if len(d) > 4 and d.startswith(d2)])
						
						if not subs_d3 or (len(subs_d3) == 1 and compact):
							disp = u"%s [%s]" % (get_title(d2), get_title(subs_d3[0])) if subs_d3 else get_title(d2)
							ws.write_merge(curr_row, curr_row, 1, 2, disp, style_normal)
							ws.write(curr_row, col_area, d2_a / unit_division, style_num)
							if has_floor: ws.write(curr_row, col_floor, d2_f, style_num)
							curr_row += 1
						else:
							ws.write_merge(curr_row, curr_row, 1, 2, get_title(d2), style_normal)
							curr_row += 1
							d3_refs, sub_start_d2, d3_sa, d3_sf = [], curr_row, 0.0, 0.0
							for d3 in subs_d3:
								a_v, f_v = area_map.get(d3, 0.0), floor_map.get(d3, 0.0)
								ws.write(curr_row, 2, get_title(d3), style_normal)
								ws.write(curr_row, col_area, a_v / unit_division, style_num)
								if has_floor: ws.write(curr_row, col_floor, f_v, style_num)
								d3_refs.append(curr_row + 1); d3_sa += a_v; d3_sf += f_v; curr_row += 1
							if d2_a - d3_sa > 0.0001:
								ws.write(curr_row, 2, u"其他%s" % LanduseMap.dm2mc[d2], style_normal)
								ws.write(curr_row, col_area, (d2_a - d3_sa) / unit_division, style_num)
								if has_floor: ws.write(curr_row, col_floor, d2_f - d3_sf, style_num)
								d3_refs.append(curr_row + 1); curr_row += 1
							ws.write_merge(sub_start_d2, curr_row - 1, 1, 1, sum_caption, style_normal)
							ws.write(d2_p_row, col_area, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_area_let, r) for r in d3_refs]) + ")"), style_num)
							if has_floor: ws.write(d2_p_row, col_floor, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_floor_let, r) for r in d3_refs]) + ")"), style_num)

					d2_all_a = sum([v for k, v in area_map.items() if len(k) >= 4 and k[:2] == d1])
					if d1_area - d2_all_a > 0.0001:
						ws.write_merge(curr_row, curr_row, 1, 2, u"其他%s" % LanduseMap.dm2mc[d1], style_normal)
						ws.write(curr_row, col_area, (d1_area - d2_all_a) / unit_division, style_num)
						if has_floor: ws.write(curr_row, col_floor, d1_floor - sum([v for k, v in floor_map.items() if len(k) >= 4 and k[:2] == d1]), style_num)
						d2_refs.append(curr_row + 1); curr_row += 1
					
					ws.write_merge(sub_start_d1, curr_row - 1, 0, 0, sum_caption, style_normal)
					ws.write(d1_p_row, col_area, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_area_let, r) for r in d2_refs]) + ")"), style_num_bold)
					if has_floor: ws.write(d1_p_row, col_floor, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_floor_let, r) for r in d2_refs]) + ")"), style_num_bold)
				else:
					ws.write(d1_p_row, col_area, d1_area / unit_division, style_num_bold)
					if has_floor: ws.write(d1_p_row, col_floor, d1_floor, style_num_bold)

		# 合计与占比回填
		total_idx = curr_row
		ws.write_merge(total_idx, total_idx, 0, 2, u"合计", style_bold)
		ws.write(total_idx, col_area, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_area_let, r) for r in d1_row_refs]) + ")"), style_num_bold)
		if has_floor: ws.write(total_idx, col_floor, xlwt.Formula("SUM(" + ",".join(["%s%d"%(col_floor_let, r) for r in d1_row_refs]) + ")"), style_num_bold)
		ws.write(total_idx, col_pct, 1.0, style_pct_bold)
		
		t_ref = "%s$%d" % (col_area_let, total_idx + 1)
		for r in range(1, total_idx):
			st = style_pct_bold if (r + 1) in bold_rows else style_pct
			ws.write(r, col_pct, xlwt.Formula("%s%d/%s" % (col_area_let, r + 1, t_ref)), st)

	wb.save(export_xlsx)




# 生成批量插入CAD控制指标块的autoLisp代码
# prop_map = {"块参数":"字段名", ...}
# 测试：res=alu.conv_autolisp_insertKZBlock("规划用地0127","e:/temp/out.lsp",{u"地类编码":u"国空混合类",u"编码A":u"国空一级类",u"编码B":u"国空二级类",u"编码C":u"国空三级类"})
def conv_autolisp_insertKZBlock(dataset, output_lsp, prop_map, block_name = u"控制指标", fields_need_trans = [], translation = lambda x:x):
	features = af.to_dict(dataset)
	commands = []
	for fea in features:
		try:
			ct = fea['SHAPE@'].centroid
		except:
			print(u"几何出错未导出： \n%s\n"%(fea,))
			continue
		x  = ct.X
		y  = ct.Y
		props  = prop_map.values()
		values = []
		for field_name in props:
			if field_name in fields_need_trans:
				values.append(translation(fea[field_name]))
			else:
				values.append(fea[field_name])
		command = '(insertKZBlock "%s" %f %f'+' "%s"'*len(props)+')'
		command %= (block_name,x,y)+tuple(values)
		commands.append(command)
	
	prop_titles = u" ".join([u"arg_%d"%(i) for i in range(len(props))])
	prop_definitions = u"".join([u'''              ((wcmatch tag "*%s*") (vla-put-TextString attr (vl-princ-to-string arg_%d)))'''%(key,idx) for idx,key in enumerate(props)])
	autolisp_function = u'''
(vl-load-com)

;;; 主函数：insertKZBlock
;;; 参数：块名, X, Y, 以及 N 个业务属性
(defun insertKZBlock (bn x y %s / acadObj doc ms pt obj attrs tag val)
  (setq acadObj (vlax-get-acad-object)
        doc (vla-get-ActiveDocument acadObj)
        ms (vla-get-ModelSpace doc)
        pt (vlax-3d-point (list x y 0.0)))

  ;; 1. 验证块定义是否存在
  (if (tblsearch "BLOCK" bn)
    (progn
      ;; 2. 插入块引用
      (setq obj (vla-InsertBlock ms pt bn 1.0 1.0 1.0 0.0))
      
      ;; 3. 如果块有属性，开始批量填充
      (if (= (vla-get-HasAttributes obj) :vlax-true)
        (progn
          (setq attrs (vlax-invoke obj 'GetAttributes))
          (foreach attr attrs
            (setq tag (vla-get-TagString attr))
            ;; 根据标签名匹配对应的参数值 (请确保 CAD 块内的 Tag 名字与下面引号内一致)
            (cond
%s
            )
          )
          (vla-update obj) ; 强制刷新显示
          (princ (strcat "\\n[成功] 已在 (" (rtos x 2 2) "," (rtos y 2 2) ") 插入指标块。"))
        )
        (princ "\\n[警告] 该块定义没有属性标签。")
      )
    )
    (princ (strcat "\\n[错误] 图纸中找不到块: " bn))
  )
  (princ)
)
	'''%(prop_titles,prop_definitions)
	autolisp_function+="\n\n"
	for command in commands:
		autolisp_function+=command+"\n"
	with open(output_lsp, "w") as f:
		f.write(autolisp_function.encode('utf8'))
	



