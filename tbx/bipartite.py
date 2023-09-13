import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net

point_1=arcpy.GetParameterAsText(0)
point_2=arcpy.GetParameterAsText(1)
fs1_str=arcpy.GetParameterAsText(2)
if fs1_str=="#" or fs1_str=="":
	fields_1=[]
else:
	fields_1=fs1_str.split(";")
fs2_str=arcpy.GetParameterAsText(3)
if fs2_str=="#" or fs2_str=="":
	fields_2=[]
else:
	fields_2=fs2_str.split(";")
method_str=arcpy.GetParameterAsText(4)
if method_str=='':
	method=lambda x,y,z:True
else:
	method=eval(method_str)
str_calc=arcpy.GetParameterAsText(5)
if str_calc=='':
	method_calc=lambda x,y:True
else:
	method_calc=eval(str_calc)

edge_out=arcpy.GetParameterAsText(6)
id_field_1=arcpy.GetParameterAsText(7)
id_field_2=arcpy.GetParameterAsText(8)
max_length_str=arcpy.GetParameterAsText(9)

try:
	max_length = float(max_length_str)
except:
	max_length = None

calc_field_type = arcpy.GetParameterAsText(10)

src.net.Bipartite(point_1,point_2,edge_out,fields_1,fields_2,method,method_calc,False,max_length,id_field_1,id_field_2,calc_field_type)