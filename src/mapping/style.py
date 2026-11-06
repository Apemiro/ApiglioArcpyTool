# -*- coding: UTF-8 -*-
# style tool
# 导出样式的工具

import arcpy
import json


def layerStyleToAutoLisp_CADLayerColor(lyr_filename, layer_template="%s"):
	lyr = arcpy.mapping.Layer(lyr_filename)
	render_text = lyr._arc_object.getsymbology()
	render = json.loads(render_text)
	labels = {}
	legend = {}
	for uniq_info in render[u'renderer'][u'uniqueValueInfos']:
		val = uniq_info["value"]
		lab = uniq_info["label"]
		if lab not in labels:
			labels[lab] = uniq_info["symbol"]["color"]
		legend[val] = labels[lab]

	lisp_cmds = []
	for value in legend:
		color = legend[value]
		lisp_cmds.append('''(setLayer-RGB "YD-%s" %d %d %d)'''%(value, color[0], color[1], color[2]))

	return lisp_cmds