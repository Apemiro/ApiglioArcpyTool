import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.edit
import arcpy

edges        = arcpy.GetParameterAsText(0)
output_edges = arcpy.GetParameterAsText(1)

arcpy.management.CopyFeatures(edges,output_edges)
src.edit.EdgeToOD(output_edges)

