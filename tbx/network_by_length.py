import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net

nodes        = arcpy.GetParameterAsText(0)
max_dist     = float(arcpy.GetParameterAsText(1))
output_edges = arcpy.GetParameterAsText(2)

src.net.GenGeoNetworkByLength(nodes,output_edges,max_dist,False)

