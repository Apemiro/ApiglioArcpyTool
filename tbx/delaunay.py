import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net

node_dataset     = arcpy.GetParameterAsText(0)
id_field         = arcpy.GetParameterAsText(1)
out_face_dataset = arcpy.GetParameterAsText(2)
vertice_type     = arcpy.GetParameterAsText(3)

src.net.Delaunay(node_dataset,id_field,out_face_dataset,vertice_type,in_memory=False)

