import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.attr as attr

lyr = arcpy.GetParameter(0)
ori_field_name = arcpy.GetParameterAsText(1)
new_field_name = arcpy.GetParameterAsText(2)
new_field_type = arcpy.GetParameterAsText(3)
new_field_size = arcpy.GetParameter(4)
new_field_alias = arcpy.GetParameterAsText(5)
delete_bak_field = arcpy.GetParameter(6)

attr.FieldTypeChanger(lyr.dataSource, ori_field_name, new_field_type, field_scale_or_length=new_field_size, change_field_name=new_field_name, new_alias=new_field_alias, delete_bak_field=delete_bak_field)