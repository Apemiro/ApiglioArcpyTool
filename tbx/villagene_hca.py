import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.villagene

def arctool_warning_func(x):
	arcpy.AddWarning(x)

node_dataset = arcpy.GetParameterAsText(0)
calc_field   = arcpy.GetParameterAsText(1)
out_fig      = arcpy.GetParameterAsText(2)
dist_base    = float(arcpy.GetParameterAsText(3))
phi          = float(arcpy.GetParameterAsText(4))
label_field  = arcpy.GetParameterAsText(5)
ngroups      = arcpy.GetParameter(6)
field_prep   = arcpy.GetParameter(7)

out_fields   = [(x, field_prep+str(x)) for x in ngroups]

src.specific.villagene.village_comprehensive_hca(node_dataset, calc_field, out_fig, dist_base, phi, label_field, out_fields, arctool_warning_func)
