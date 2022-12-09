import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net

nodes        = arcpy.GetParameterAsText(0)
val_field    = arcpy.GetParameterAsText(1)
output_edges = arcpy.GetParameterAsText(2)

src.net.GenGeoNetworkByValue(nodes,output_edges,val_field,False)

