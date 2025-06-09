import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.planning.road as rd

input_lines   = arcpy.GetParameterAsText(0)
output_lines  = arcpy.GetParameterAsText(1)
max_dist      = arcpy.GetParameter(2)

rd.edge_line_closure(input_lines, output_lines, max_dist)
