import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net
import src.attr

delaunay_dataset = arcpy.GetParameterAsText(0)
vertices_field   = arcpy.GetParameterAsText(1)
stat_field       = arcpy.GetParameterAsText(2)
node_dataset     = arcpy.GetParameterAsText(3)
key_field        = arcpy.GetParameterAsText(4)
value_field      = arcpy.GetParameterAsText(5)

if not stat_field in [x.name for x in arcpy.Describe(delaunay_dataset).fields]:
	arcpy.management.AddField(delaunay_dataset,stat_field,"SHORT")
class_dict = src.attr.FieldDicter(node_dataset,key_field,value_field)
src.net.Delaunay_stat(delaunay_dataset,vertices_field,stat_field,class_dict)
