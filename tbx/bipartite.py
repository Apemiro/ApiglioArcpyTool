import sys
sys.path.append("..")
import src
import src.net

point_1=arcpy.GetParameterAsText(0)
point_2=arcpy.GetParameterAsText(1)
fs1_str=arcpy.GetParameterAsText(2)
if fs1_str=="":
	fields_1=[]
else:
	fields_1=fs1_str.split(";")
fs2_str=arcpy.GetParameterAsText(3)
if fs2_str=="":
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

src.net.Bipartite(point_1,point_2,edge_out,fields_1,fields_2,method,method_calc,False)