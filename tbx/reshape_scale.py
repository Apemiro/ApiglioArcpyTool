import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.codetool.reshape as ars
import src.geoop.transform as atrans


input_feature=arcpy.GetParameterAsText(0)
output_feature=arcpy.GetParameterAsText(1)
scale_base=arcpy.GetParameterAsText(2)
scale_field=arcpy.GetParameterAsText(3)
if scale_field=="#" or scale_field=="":
	scale_field=None


ars.scaling(input_feature, output_feature, scale_base, scale_field)


'''
wotm服了
直接调用函数可以，工具箱不行
保存在数据库可以，shapefile不行
sbgis
'''