import numpy as np 
import pandas as pd 


def boxplot(data, kind="boxplot", options = None, plot_options = None):
	"""
	data: pd.DataFrame (for tabular data) OR dict of {seriesName: seriesData} (for irregular shape data)
	kind: {"boxplot", "hboxplot"}
	options: options params specific to zingchart boxplot
	plot_options: other options to zing chart, e.g. , 'ScaleX' and etc.

	return plot_data: json for zingchart plot data 
	"""
	if type(data) == dict:
		colnames = list(data.keys())
		describes = dict([ (c, data[c].describe()) for c in colnames])
		describes = pd.DataFrame(describes)
	else:
		describes = data.describe()
		colnames = list(describes.columns)
	
	iqrs = [describes.loc["75%", c] - describes.loc["25%", c] for c in colnames]
	lowers = [describes.loc["25%", c] - iqr*1.5 for c, iqr in zip(colnames, iqrs)]
	uppers = [describes.loc["75%", c] + iqr*1.5 for c, iqr in zip(colnames, iqrs)]
	#data_outliers = [ [[i, o] for o in data.loc[:, c][(data.loc[:, c]<lower) | (data.loc[:, c]>upper)]]  
	#					for i, (c, lower, upper) in enumerate(zip(colnames, lowers, uppers))]
	data_outliers = [ [[i, o] for o in data[c][(data[c]<lower) | (data[c]>upper)]]  
						for i, (c, lower, upper) in enumerate(zip(colnames, lowers, uppers))]
	data_outliers = sum(data_outliers, [])

	data_box = [[lowers[i]]+list(describes.loc[[ "25%", "50%", "75%"], c])+[uppers[i]] for i,c in enumerate(colnames)]
	#data_box = [list(describes.loc[["min", "25%", "50%", "75%", "max"], c]) for i,c in enumerate(colnames)]
	plot_data = { "type": kind
				, "scaleX": {"values": colnames}
				, "options": options
				, "series": [{
					  "data-box": data_box
					, "data-outlier": data_outliers
				}]}
	if plot_options:
		plot_data.update(plot_options)
	return plot_data


def scatterplot(data, makers = None, plot_options = None):
	pass