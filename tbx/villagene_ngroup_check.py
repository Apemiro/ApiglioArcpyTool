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

points     = arcpy.GetParameterAsText(0)
gene_field = arcpy.GetParameterAsText(1)
dist_base  = float(arcpy.GetParameterAsText(2))
phi        = float(arcpy.GetParameterAsText(3))
n_min      = int(arcpy.GetParameterAsText(4))
n_max      = int(arcpy.GetParameterAsText(5))
out_fig    = arcpy.GetParameterAsText(6)

ngroup_list = range(n_min,n_max+1)

src.specific.villagene.village_comph_hca_quality(points, gene_field, dist_base, phi, ngroup_list, out_fig, warning_func=arctool_warning_func)