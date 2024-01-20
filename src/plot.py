# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import gc


def lines(data, save_filename, xlabel, ylabel, figsize=None, dpi=300):
	if figsize == None:
		fig = plt.figure()
	else:
		fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.plot(data)
	fig.savefig(save_filename, dpi=dpi)
	fig.clf()
	plt.close()
	gc.collect()









