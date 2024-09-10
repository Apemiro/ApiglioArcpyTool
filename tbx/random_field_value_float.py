import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import arcpy
import src
import src.attr as aattr
import scipy.stats # 如果没有安装scipy，则需要python.exe -m pip install scipy 

dataset     = arcpy.GetParameterAsText(0)
field_name  = arcpy.GetParameterAsText(1)
mean_str    = arcpy.GetParameterAsText(2)
scale_str   = arcpy.GetParameterAsText(3)
ppf_mode    = arcpy.GetParameterAsText(4).split(" ")[0]
try:
	mean = float(mean_str)
except:
	mean = 0.0
try:
	scale = float(scale_str)
except:
	scale = 1

if ppf_mode=='Normal':
	aattr.random_field_values(dataset, field_name, rand_value_func=lambda x:scipy.stats.norm.ppf(x, loc=mean, scale=scale))
elif ppf_mode=='Uniform':
	aattr.random_field_values(dataset, field_name, rand_value_func=lambda x:((x-mean)*2-1)*scale)
else:
	arcpy.AddError(u"无效的分布函数选项")