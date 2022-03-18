import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.net

nodes=arcpy.GetParameterAsText(0)
id_field=arcpy.GetParameterAsText(1)
# fields=arcpy.ListFields(nodes)
# fields.sort(key=lambda x:x.name==id_field,reverse=True)
adjacent_matrix=arcpy.GetParameterAsText(2)
max_dist=arcpy.GetParameterAsText(3)
criterion_str=arcpy.GetParameterAsText(4)
if criterion_str=="" or criterion_str=="#":
	# if fields[0].type.upper()=="STRING":
		# criterion=lambda x,y:x==y
	# else:
		criterion=lambda x,y:int(x)==y
else:
	criterion=eval(criterion_str)
output_edges=arcpy.GetParameterAsText(5)

src.net.Adjacent2GeoNetwork(nodes,id_field,adjacent_matrix,output_edges,max_dist,criterion,False)