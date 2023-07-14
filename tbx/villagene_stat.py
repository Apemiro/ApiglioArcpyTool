import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.villagene

node_dataset  = arcpy.GetParameterAsText(0)
gene_field    = arcpy.GetParameterAsText(1)
grouped_field = arcpy.GetParameterAsText(2)
out_folder    = arcpy.GetParameterAsText(3)
header        = arcpy.GetParameterAsText(4)

out_img = out_folder + "/" + header

src.specific.villagene.grouped_gene(node_dataset, gene_field, grouped_field, out_img, ext=".png")
