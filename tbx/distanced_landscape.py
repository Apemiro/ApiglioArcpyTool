import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.specific.skl
import src.logline

def arctool_message_func(x):
	arcpy.AddMessage(x)
def arctool_warning_func(x):
	arcpy.AddWarning(x)
def arctool_error_func(x):
	arcpy.AddError(x)

src.logline.log_line_message = arctool_message_func
src.logline.log_line_warning = arctool_warning_func
src.logline.log_line_error = arctool_error_func

view_points    = arcpy.GetParameterAsText(0)
dem_raster     = arcpy.GetParameterAsText(1)
max_dist       = float(arcpy.GetParameterAsText(2))
min_dist       = float(arcpy.GetParameterAsText(3))
export_path    = arcpy.GetParameterAsText(4)
name_field     = arcpy.GetParameterAsText(5)
if name_field == "": name_field = None
export_formats = arcpy.GetParameter(6)
src.specific.skl.viewpoints_to_landscape(view_points, dem_raster, max_dist, min_dist, export_path, name_field, export_formats)