import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.codetool.doc

lyr = arcpy.GetParameter(0)
mxd = arcpy.mapping.MapDocument("current")
dfm = mxd.activeDataFrame
ext = lyr.getSelectedExtent()
dfm.extent = ext