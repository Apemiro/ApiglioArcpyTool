import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.codetool.doc

path_name = arcpy.GetParameterAsText(0)
layer = arcpy.GetParameter(1)
arcpy.AddMessage(type(layer))
arcpy.AddMessage(layer)

field_name = arcpy.GetParameterAsText(2)
ext = arcpy.GetParameterAsText(3)
dpi = int(arcpy.GetParameterAsText(4))
if field_name=="#" or field_name=="":
	field_name=None

src.codetool.doc.export_by_layer_selection(path_name, layer, field_name, ext,dpi, 0.075)