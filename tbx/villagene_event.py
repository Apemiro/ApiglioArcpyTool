import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.villagene

node_dataset  = arcpy.GetParameterAsText(0)
value_field   = arcpy.GetParameterAsText(1)
grouped_field = arcpy.GetParameterAsText(2)
out_img       = arcpy.GetParameterAsText(3)

src.specific.villagene.grouped_eventplot(node_dataset, value_field, grouped_field, out_img, ext="")