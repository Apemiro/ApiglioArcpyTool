import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import arcpy
import src
import src.geoop.randgeo as argeo
import src.codetool.feature as afea

polyline     = arcpy.GetParameterAsText(0)
density_str  = arcpy.GetParameterAsText(1)
outp_dataset = arcpy.GetParameterAsText(2)
outp, outf = os.path.split(outp_dataset)
try:
	density = float(density_str)
except:
	density = 10.0

sr_str = arcpy.Describe(polyline).spatialReference.ExportToString()
res = []
with arcpy.da.SearchCursor(polyline, ["SHAPE@"]) as cursor:
	for row in cursor:
		pl = row[0]
		num = pl.length * density // 100;
		if num<3:
			res.append(pl.positionAlongLine(pl.length/2.0))
		else:
			res += argeo.points_on_polyline(pl, int(num))
afea.to_file(res, dataset=outf, path=outp, spatial_reference=sr_str)