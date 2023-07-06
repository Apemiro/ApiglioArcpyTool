import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.villagene

node_dataset = arcpy.GetParameterAsText(0)
calc_field   = arcpy.GetParameterAsText(1)
out_csv      = arcpy.GetParameterAsText(2)
dist_base    = float(arcpy.GetParameterAsText(3))
phi          = float(arcpy.GetParameterAsText(4))

src.specific.villagene.village_comprehensive_relationship(node_dataset, calc_field, out_csv, dist_base, phi)
