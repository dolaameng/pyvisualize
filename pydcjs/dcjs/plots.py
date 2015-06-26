## Supported Chart Types


def categorical_histogram_bar(anchor_id, feature, 
	width = 600, height = 300, 
	xAxisLabel = "", yAxisLabel = "", 
	cf_obj = "ndx"):
	"""
	Distribution barchart for one categorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx" 
	"""
	return r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, feature: "%(feature)s"
		, width: %(width)d
		, height: %(height)d
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: '%(yAxisLabel)s'
	};
	charts["%(anchor_id)s"] = dc.barChart(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {return d[options["%(anchor_id)s"].feature];});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group();

	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.x(d3.scale.ordinal())
		.xUnits(dc.units.ordinal)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		;
		""" % dict(anchor_id = anchor_id, feature = feature, 
				width = width, height = height, 
				xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel, 
				cf_obj = cf_obj)

def categorical_histogram_row(anchor_id, feature,
	width = 600, height = 600, cf_obj = "ndx"):
	"""
	Distribution rowchart (commodating more values) for one categorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx" 
	"""
	return """
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, feature: "%(feature)s"
		, width: %(width)d
		, height: %(height)d
		// doesnt support xAxisLabel and yAxisLabel
	};
	charts["%(anchor_id)s"] = dc.rowChart(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {return d[options["%(anchor_id)s"].feature];});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group();

	charts["#%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.elasticX(true)
		;
	""" % dict(anchor_id = anchor_id, feature = feature,
		width = width, height = height, cf_obj = cf_obj)

def categorical_timeseries_area(anchor_id, timefeature, feature,
	width = 600, height = 300, margins = None, 
	xAxisLabel = "", yAxisLabel = "", cf_obj = "ndx"):
	"""
	Timeseries distribution for one cateogorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	timefeature: name of column that contains timestamp
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx" 
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	return """
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, timefeature: "%(timefeature)s"
		, feature: "%(feature)s"
		, width: %(width)d
		, height: %(height)d
		, margins: {top: %(top)d, right: %(right)d, bottom: %(bottom)d, left: %(left)d}
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: "%(yAxisLabel)s"
	};
	charts["%(anchor_id)s"] = dc.lineChart(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {
		return new Date(d[options["%(anchor_id)s"].timefeature]); 
	});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group().reduce(
		// reduce add
		function (p, v) {
			var f = options["%(anchor_id)s"].feature; 
			p[v[f]] = (p[v[f]] || 0) + 1;
			return p;
		}
		// reduce remove
		, function (p, v) {
			var f = options["%(anchor_id)s"].feature; 
			p[v[f]] = (p[v[f]] || 0) - 1;
			return p;
		}
		// reduce init
		, function () {
			return {};
		}
	);
	var minDate = new Date(dims["%(anchor_id)s"].bottom(1)[0][options["%(anchor_id)s"].timefeature]);
	var maxDate = new Date(dims["%(anchor_id)s"].top(1)[0][options["%(anchor_id)s"].timefeature]);
	var feature_values = [];
	%(cf_obj)s.dimension(function (d) {return d[options["%(anchor_id)s"].feature];})
							.group().top(Infinity).forEach(function(kv){feature_values.push(kv.key);});
	var select_stack = function (i) {return function(kv) {return (kv.value[i] || 0); } };
	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"], feature_values[0], select_stack(feature_values[0]))
		.margins(options["%(anchor_id)s"].margins)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.renderArea(true)
		.elasticY(true)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		.legend(dc.legend())
		;
	for (var i = 1; i < feature_values.length; ++i) {
		charts["%(anchor_id)s"].stack(groups["%(anchor_id)s"], feature_values[i], 
			select_stack(feature_values[i]));
	}
	""" % dict(anchor_id = anchor_id, timefeature = timefeature,
			feature = feature, width = width, height = height,
			top = default_margins["top"], bottom = default_margins["bottom"],
			left = default_margins["left"], right = default_margins["right"], 
			xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel, cf_obj = cf_obj)

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

charts = {
	"categorical_histogram_bar": categorical_histogram_bar
	# ??  
}

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

