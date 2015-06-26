## Supported Chart Types

def categorical_histogram_bar():
	"""
	Distribution barchart for one categorical variable
	"""
	pass

def categorical_histogram_row():
	"""
	Distribution rowchart (commodating more values) for one categorical variable
	"""
	pass

def categorical_timeseries_area():
	"""
	Timeseries distribution for one cateogorical variable
	"""
	pass

def categorical_pair_heatmap():
	"""
	Pivot table for a pair of categorical variables
	"""
	pass

def numerical_timeseries_line():
	"""
	Timeseries for one numerical variable 
	"""
	pass

def numerical_pair_scatter():
	"""
	Scatterplot for a pair numerical variables
	"""
	pass

def numerical_pair_by_categorical_bubble():
	"""
	Bubble: grouped by one categorcial, in each group, three numerical variables can be specified: x, y, radius
	"""
	pass

def numerical_by_categorical_box():
	"""
	Boxplot of a numerical variable grouped by values of a categorical variable
	"""
	pass

## Helper function to generate javascript
def cdn_css():
	return r"""<link rel="stylesheet" type="text/css" href="http://dc-js.github.io/dc.js/css/dc.css">
	<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	"""

def cdn_script():
	return r"""<script type="text/javascript" src="http://dc-js.github.io/dc.js/js/d3.js"></script>
	<script type="text/javascript" src="http://dc-js.github.io/dc.js/js/crossfilter.js"></script>
	<script type="text/javascript" src="http://dc-js.github.io/dc.js/js/dc.js"></script>
	"""

## Crossfiltered chart dashboard for a dataset - main interface
def plot_dataset():
	pass

