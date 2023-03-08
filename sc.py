# -*- coding: UTF-8 -*-
# 缩写运行

import src.codetool.df as agd
import src.codetool.feature as agf
import src.geoop.geolib as ageo


doc         = agd.active_doc
df          = agd.active_df
sr          = agd.active_sr
ex          = lambda:agd.active_df().extent
genbox      = agd.createViewBox
gencircle   = agd.createViewCircle
gencenter   = agd.createViewCenter

to_list     = agf.to_list
to_set      = agf.to_set
to_dict     = agf.to_dict
to_file     = agf.to_file

to_point    = ageo.to_point
to_pointgeo = ageo.to_pointgeo
to_polyline = ageo.to_polyline
to_polygon  = ageo.to_polygon

split       = ageo.split
randpoint   = ageo.random_point
