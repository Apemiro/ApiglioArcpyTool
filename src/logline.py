# -*- coding: UTF-8 -*-
import arcpy

log_line_message = None
log_line_warning = None
log_line_error = None

# m-message w-warning e-error
def log(string,logtype="m"):
	if logtype == "m":
		if log_line_message == None:
			print(string)
		else:
			log_line_message(string)
	elif logtype == "w":
		if log_line_warning == None:
			print(string)
		else:
			log_line_warning(string)
	elif logtype == "e":
		if log_line_error == None:
			print(string)
		else:
			log_line_error(string)
	else:
		raise Exception("logtype wrong: expect m/w/e.")