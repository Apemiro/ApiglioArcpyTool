# -*- coding: UTF-8 -*-
# planning tool
# sheet tool

class HeaderedTable:
	def __init__(self):
		self.header = []
		self.values = []
	
	def __add__(self, the_other):
		result = HeaderedTable()
		result.header = self.header[:]
		col_indice = []
		for h in the_other.header:
			if h in result.header:
				col_indice.append(result.header.index(h))
			else:
				col_indice.append(len(result.header))
				result.header.append(h)
		ncols_new = len(result.header) - len(self.header)
		result.values = [x+[None]*ncols_new for x in self.values]
		for row in range(len(the_other.values)):
			row_data = [None]*len(result.header)
			for col in range(len(col_indice)):
				row_data[col_indice[col]] = the_other.values[row][col]
			result.values.append(row_data)
		return result
	
	def loadFromSheet(self, worksheet, nrows_header, titled=True):
		'''
		worksheet   	 - xlrd worksheet object
		nrows_header	 - how many rows of field header
		titled      	 - if the first row is table title
		'''
		import xlrd
		matrix = [[None] * (worksheet.ncols) for _ in range(worksheet.nrows)]
		for row in range(worksheet.nrows):
			for col in range(worksheet.ncols):
				matrix[row][col] = worksheet.cell(row, col).value
		
		merged_rows = set()
		for r0, r1, c0, c1 in worksheet.merged_cells:
			for row in range(r0, r1):
				merged_rows.add(row)
				for col in range(c0, c1):
					if row==r0 and col==c0: continue
					matrix[row][col] = matrix[r0][c0]
		
		# reduce相邻去重
		ordered_uniq = lambda a,b:([a,b] if a!=b else [a]) if type(a)!=list else a+[b] if a[-1]!=b else a
		fields = []
		header_r0 = 1 if titled else 0
		for col in range(worksheet.ncols):
			field_name_parts = [mat[col] for mat in matrix[header_r0:header_r0+nrows_header]]
			field_name_parts = reduce(ordered_uniq, field_name_parts)
			field_name = ".".join(["%s"%(x,) for x in field_name_parts])
			field_name = field_name.replace("\n","")
			fields.append(field_name)
		if len(fields) != len(set(fields)):
			fcount = {}
			for f in fields:
				fcount[f] = fcount.get(f, 0) + 1
			repeated_header = [x for x in fcount if fcount[x]>1]
			print(u"【存在重名字段】")
			print("\n".join(repeated_header))
			# raise Exception("repeated header: %s"%(", ".join(repeated_header),))
			
		data = []
		category = ""
		data_row = False
		for row in range(header_r0+nrows_header, worksheet.nrows):
			if row in merged_rows:
				category = matrix[row][0] if data_row else ".".join([category,matrix[row][0]])
				data_row = False
			else:
				data.append(matrix[row]+[category])
				data_row = True
		
		self.header = fields + ['__category__']
		self.values = data
	
	def saveToSheet(self, worksheet, title=None):
		'''
		worksheet   	 - xlwt worksheet object
		title        	 - insert title in the first row
		'''
		# import xlwt
		# worksheet.write()
		pass
		
	
	
	
# import sys
# sys.path.append(r"E:\ApiglioProject\ArcGISProject")
# import apiglio.src.specific.planning.sheet
# ash=apiglio.src.specific.planning.sheet
# from apiglio.src.specific.planning.sheet import HeaderedTable


if __name__ == '__main__':
	#测试代码
	import os
	import re
	import xlrd
	filenames = os.listdir(r"F:\__tmp\table")
	filenames = [r"F:\__tmp\table\%s"%(x,) for x in filenames]
	
	tables = []
	for filename in filenames:
		if re.search(u"电网|通信网", filename):
			head_height = 2
		else:
			head_height = 4
		wbook = xlrd.open_workbook(filename)
		sheet = wbook.sheet_by_index(4)
		table = HeaderedTable()
		table.loadFromSheet(sheet, head_height)
		tables.append(table)
		
	table_merged = reduce(lambda a,b:a+b, tables)
	
	a1 = table_merged.header.index(u"项目名称")
	a2 = table_merged.header.index(u"总投资（万元）")
	a3 = table_merged.header.index(u"主要建设内容")
	
	for i,row in enumerate(table_merged.values):
		print ("%04d\t%s\t%s\t%s"%(i,row[a1],row[a2],row[a3])).encode('gbk',errors='ignore')
	
	# for i in f: print(i)
	# for i,j in zip(f, d[4]): print "%s: \t %24s"%(i,j)
	# for i,j in [(x[2],x[14]) for x in d]: print "%s: \t %24s"%(i,j)