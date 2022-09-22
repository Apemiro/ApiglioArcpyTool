import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.codetool.doc

path_name=arcpy.GetParameterAsText(0)
feature_name=arcpy.GetParameterAsText(1)
field_name=arcpy.GetParameterAsText(2)
if field_name=="#" or field_name=="":
	field_name=None

src.codetool.doc.export_by_features(path_name,feature_name,field_name)