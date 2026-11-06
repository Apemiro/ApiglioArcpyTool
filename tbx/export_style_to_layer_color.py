import os
import os.path
p=os.path.split(__file__)[0]
rp=os.path.realpath(p+"/..")
import sys
sys.path.append(rp)
import src
import src.mapping.style

lyr_filename = arcpy.GetParameterAsText(0)
template     = arcpy.GetParameterAsText(1)
lsp_filename = arcpy.GetParameterAsText(2)

commands = src.mapping.style.layerStyleToAutoLisp_CADLayerColor(lyr_filename, template)
lsp_text = u'''
(defun setLayer-RGB (layer-name red green blue / doc layers layer-obj true-color)
  (vl-load-com)
  (setq doc (vla-get-activedocument (vlax-get-acad-object)))
  (setq layers (vla-get-layers doc))
  
  (if (not (tblsearch "layer" layer-name))
    (setq layer-obj (vla-add layers layer-name))
    (setq layer-obj (vla-item layers layer-name))
  )
  
  (setq true-color (vlax-create-object (strcat "AutoCAD.AcCmColor." (substr (getvar "acadver") 1 2))))
  (vla-setRGB true-color red green blue)
  
  (vla-put-TrueColor layer-obj true-color)
  
  (vlax-release-object true-color)
  (princ (strcat "\nColor of Layer '" layer-name "' is set to RGB(" (itoa red) "," (itoa green) "," (itoa blue) "). "))
  (princ)
)
'''+"\n".join(commands)

if lsp_filename=="#" or lsp_filename=="":
	arcpy.AddMessage(lsp_text)
else:
	f = open(lsp_filename, "w")
	f.write(lsp_text.encode('utf8'))
	f.close()
	