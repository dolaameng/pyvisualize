## Supported Chart Types


def categorical_histogram_bar(anchor_id, feature,
	width = 600, height = 300,
	xAxisLabel = "", yAxisLabel = "",
	cf_obj = "ndx", div_template=None):
	"""
	Distribution barchart for one categorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx"
	RETURN: (div, js)
	"""
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
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
	return (div, jscode)

def categorical_histogram_row(anchor_id, feature,
	width = 600, height = 600, cf_obj = "ndx", div_template=None):
	"""
	Distribution rowchart (commodating more values) for one categorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx"
	"""
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
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

	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.elasticX(true)
		;
	""" % dict(anchor_id = anchor_id, feature = feature,
		width = width, height = height, cf_obj = cf_obj)
	return (div, jscode)

def categorical_timeseries_area(anchor_id, timefeature, feature,
	width = 600, height = 300, margins = None,
	xAxisLabel = "", yAxisLabel = "", cf_obj = "ndx", div_template=None):
	"""
	Timeseries distribution for one cateogorical variable
	anchor_id: id of div in html, e.g. "location-bar"
	timefeature: name of column that contains timestamp
	feature: categorical feature to be plotted in barchart
	cf_obj: cross_filter object variable, default to "ndx"
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
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
	return (div, jscode)

def categorical_pair_heatmap(anchor_id, 
	column_feature, index_feature, value_feature,
	aggfun = "count", tooltip_prefix = "Count",
	width = 600, height = 300, margins = None,
	color_scheme = "green",
	cf_obj = "ndx", div_template=None):
	"""
	Pivot table for a pair of categorical variables
	supported aggfun for value_feature: {"average", "sum", "count"}
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, column_feature: "%(column_feature)s"
		, index_feature: "%(index_feature)s"
		, value_feature: "%(value_feature)s"
		, tooltip_prefix: "%(tooltip_prefix)s"
		, aggfun: "%(aggfun)s"
		, width: %(width)d
		, height: %(height)d
		, margins: {top: %(top)d, right: %(right)d, bottom: %(bottom)d, left: %(left)d}
		, colorRange: colorRangeScheme["%(color_scheme)s"]
	};
	charts["%(anchor_id)s"] = dc.heatMap(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {
		return [d[options["%(anchor_id)s"].column_feature],
				d[options["%(anchor_id)s"].index_feature]];
	});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group().reduce(
		// reduce add
		aggfuns[options["%(anchor_id)s"].aggfun].add(options["%(anchor_id)s"].value_feature)
		// reduce remove
		, aggfuns[options["%(anchor_id)s"].aggfun].remove(options["%(anchor_id)s"].value_feature)
		// reduce init
		, aggfuns[options["%(anchor_id)s"].aggfun].init(options["%(anchor_id)s"].value_feature)
	);

	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width)
		.height(options["%(anchor_id)s"].height)
		.margins(options["%(anchor_id)s"].margins)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.keyAccessor(function (kv) {return kv.key[0];})
		.valueAccessor(function (kv) {return kv.key[1];})
		.colorAccessor(function (kv) {return kv.value.result;})
		.renderLabel(true)
		.colors(d3.scale.linear().domain(minmax_value(groups["%(anchor_id)s"])).range(options["%(anchor_id)s"].colorRange))
		.title(function(kv) {return options["%(anchor_id)s"].tooltip_prefix+kv.value.result;})  //tooltip
		;
	""" % dict(anchor_id = anchor_id, column_feature = column_feature, 
		index_feature = index_feature, value_feature = value_feature,
		aggfun = aggfun, tooltip_prefix = tooltip_prefix, 
		width = width, height = height, 
		top = default_margins["top"], left = default_margins["left"], 
		bottom = default_margins["bottom"], right = default_margins["right"],
		color_scheme = color_scheme, cf_obj = cf_obj)
	return (div, jscode)

def numerical_timeseries_line(anchor_id, timefeature, feature, 
	aggfun = "average", width = 600, height = 300, 
	xAxisLabel = "", yAxisLabel = "", cf_obj = "ndx", div_template=None):
	"""
	Timeseries for one numerical variable
	"""
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, timefeature: "%(timefeature)s"
		, feature: "%(feature)s"
		, aggfun: "%(aggfun)s" 
		, width: %(width)d
		, height: %(height)d
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: "%(yAxisLabel)s"
	};
	charts["%(anchor_id)s"] = dc.lineChart(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {
		return new Date(d[options["%(anchor_id)s"].timefeature]);
	});
	var minDate = new Date(dims["%(anchor_id)s"].bottom(1)[0][options["%(anchor_id)s"].timefeature]);
	var maxDate = new Date(dims["%(anchor_id)s"].top(1)[0][options["%(anchor_id)s"].timefeature]);
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group().reduce(
		// reduce add
		aggfuns[options["%(anchor_id)s"].aggfun].add(options["%(anchor_id)s"].feature)
		// reduce remove
		, aggfuns[options["%(anchor_id)s"].aggfun].remove(options["%(anchor_id)s"].feature)
		// reduce init
		, aggfuns[options["%(anchor_id)s"].aggfun].init(options["%(anchor_id)s"].feature)
	);
	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.valueAccessor(function (kv) {return kv.value.result || 0;})
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		;
	""" % dict(anchor_id = anchor_id, timefeature = timefeature,
			feature = feature, aggfun = aggfun, width = width, height = height,
			xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel, cf_obj = cf_obj)
	return (div, jscode)

def numerical_pair_scatter(anchor_id, x_feature, y_feature, 
	width = 500, height = 400, xAxisLabel = "", yAxisLabel = "",
	margins = None, cf_obj = "ndx", div_template=None):
	"""
	Scatterplot for a pair numerical variables
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, x_feature: "%(x_feature)s"
		, y_feature: "%(y_feature)s"
		, width: %(width)d
		, height: %(height)d
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: "%(yAxisLabel)s"
		, margins: {top: %(top)d, right: %(right)d, bottom: %(bottom)d, left: %(left)d}
	};
	charts["%(anchor_id)s"] = dc.scatterPlot(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {return [+d[options["%(anchor_id)s"].x_feature], +d[options["%(anchor_id)s"].y_feature]]});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group();
	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width).height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.x(d3.scale.linear().domain([0, 1]))
		.elasticX(true)
		.elasticY(true)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		.margins(options["%(anchor_id)s"].margins)
		;
	""" % dict(anchor_id = anchor_id, x_feature = x_feature, y_feature = y_feature,
		width = width, height = height, xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel,
		top = default_margins["top"], left = default_margins["left"], 
		bottom = default_margins["bottom"], right = default_margins["right"],
		cf_obj = cf_obj)
	return (div, jscode)


def numerical_pair_by_categorical_bubble(anchor_id, 
	group_feature, x_feature, y_feature, r_feature = "",
	x_aggfun = "average", y_aggfun = "average", r_aggfun = "count",
	width = 800, height = 600, max_bubble = 5000,
	xAxisLabel = "", yAxisLabel = "",
	margins = None, cf_obj = "ndx", div_template=None):
	"""
	Bubble: grouped by one categorcial, in each group, three numerical variables can be specified: x, y, radius
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, group_feature: "%(group_feature)s"
		, x_feature: "%(x_feature)s"
		, y_feature: "%(y_feature)s"
		, r_feature: "%(r_feature)s"
		, x_aggfun: "%(x_aggfun)s"
		, y_aggfun: "%(y_aggfun)s"
		, r_aggfun: "%(r_aggfun)s"
		, width: %(width)d
		, height: %(height)d
		, max_bubble: %(max_bubble)d
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: "%(yAxisLabel)s"
		, margins: {top: %(top)d, right: %(right)d, bottom: %(bottom)d, left: %(left)d}
	};
	charts["%(anchor_id)s"] = dc.bubbleChart(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {return d[options["%(anchor_id)s"].group_feature]});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group().reduce(
		// reduce add
		aggfuns["combine"].add([options["%(anchor_id)s"].x_feature, options["%(anchor_id)s"].y_feature, options["%(anchor_id)s"].r_feature],
							[options["%(anchor_id)s"].x_aggfun, options["%(anchor_id)s"].y_aggfun, options["%(anchor_id)s"].r_aggfun])
		// reduce remove
		, aggfuns["combine"].remove([options["%(anchor_id)s"].x_feature, options["%(anchor_id)s"].y_feature, options["%(anchor_id)s"].r_feature],
							[options["%(anchor_id)s"].x_aggfun, options["%(anchor_id)s"].y_aggfun, options["%(anchor_id)s"].r_aggfun])
		// reduce init
		, aggfuns["combine"].init([options["%(anchor_id)s"].x_feature, options["%(anchor_id)s"].y_feature, options["%(anchor_id)s"].r_feature],
							[options["%(anchor_id)s"].x_aggfun, options["%(anchor_id)s"].y_aggfun, options["%(anchor_id)s"].r_aggfun])
	);
	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width)
		.height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.keyAccessor(function (kv) {return kv.value[0].result;})
		.valueAccessor(function (kv) {return kv.value[1].result;})
		.radiusValueAccessor(function (kv) {return kv.value[2].result;})
		.x(d3.scale.linear().domain([0, 1]))
		.y(d3.scale.linear().domain([0, 1]))
		.r(d3.scale.linear().domain([0, options["%(anchor_id)s"].max_bubble]))
		.yAxisPadding(0.5)
    	.xAxisPadding(0.5)
		.elasticX(true)
		.elasticY(true)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		.renderLabel(true)
		.label(function (kv) {return kv.key;})
		.legend(dc.legend())
		;
	""" % dict(anchor_id = anchor_id, group_feature = group_feature, 
		x_feature = x_feature, y_feature = y_feature, r_feature = r_feature,
		x_aggfun = x_aggfun, y_aggfun = y_aggfun, r_aggfun = r_aggfun,
		width = width, height = height, max_bubble = max_bubble,
		xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel,
		top = default_margins["top"], left = default_margins["left"], 
		bottom = default_margins["bottom"], right = default_margins["right"],
		cf_obj = cf_obj)
	return (div, jscode)

def numerical_by_categorical_box(anchor_id, 
	group_feature, numerical_feature,
	width = 800, height = 600, 
	xAxisLabel = "", yAxisLabel = "",
	margins = None, cf_obj = "ndx", div_template=None):
	"""
	Boxplot of a numerical variable grouped by values of a categorical variable
	"""
	default_margins = {"top": 10, "right": 50, "bottom": 30, "left": 50}
	if margins is not None: default_margins.update(margins)
	if div_template is None: div_template = r'<div id="%s"></div>'
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
		anchor: "#%(anchor_id)s"
		, group_feature: "%(group_feature)s"
		, numerical_feature: "%(numerical_feature)s"
		, width: %(width)d
		, height: %(height)d
		, xAxisLabel: "%(xAxisLabel)s"
		, yAxisLabel: "%(yAxisLabel)s"
		, margins: {top: %(top)d, right: %(right)d, bottom: %(bottom)d, left: %(left)d}
	};
	charts["%(anchor_id)s"] = dc.boxPlot(options["%(anchor_id)s"].anchor);
	dims["%(anchor_id)s"] = %(cf_obj)s.dimension(function (d) {return d[options["%(anchor_id)s"].group_feature]});
	groups["%(anchor_id)s"] = dims["%(anchor_id)s"].group().reduce(
		//reduce add
		function (p, v) {
			p.push(v[options["%(anchor_id)s"].numerical_feature]);
			return p;
		}
		//reduce remove
		, function (p, v) {
			p.splice(p.indexOf(v[options["%(anchor_id)s"].numerical_feature]), 1);
			return p;
		}
		// reduce init
		, function () {return [];}
	);
	charts["%(anchor_id)s"]
		.width(options["%(anchor_id)s"].width)
		.height(options["%(anchor_id)s"].height)
		.dimension(dims["%(anchor_id)s"])
		.group(groups["%(anchor_id)s"])
		.elasticX(true)
		.elasticY(true)
		.margins(options["%(anchor_id)s"].margins)
		.xAxisLabel(options["%(anchor_id)s"].xAxisLabel)
		.yAxisLabel(options["%(anchor_id)s"].yAxisLabel)
		;
	""" % dict(anchor_id = anchor_id, group_feature = group_feature, 
		numerical_feature = numerical_feature,
		width = width, height = height, 
		xAxisLabel = xAxisLabel, yAxisLabel = yAxisLabel,
		top = default_margins["top"], left = default_margins["left"], 
		bottom = default_margins["bottom"], right = default_margins["right"],
		cf_obj = cf_obj)
	return (div, jscode)

def data_table(anchor_id, index, maxsize, columns, sortBy, 
	cf_obj="ndx", div_template=None):
	if div_template is None: div_template = r"""<div>
		<table id="%s" class="table table-hover dc-data-table">
		</table>
	</div>"""
	div = div_template % anchor_id
	jscode = r"""
	options["%(anchor_id)s"] = {
			anchor: "#%(anchor_id)s"
			, index: "%(index)s"
			, maxsize: %(maxsize)d //number of rows to display
			, columns: [%(columnstr)s]
			, sortBy: "%(sortBy)s"
		};

		charts["%(anchor_id)s"] = dc.dataTable(options["%(anchor_id)s"].anchor);

		dims["%(anchor_id)s"] = %(cf_obj)s.dimension(
			function (d) {
				return d[options["%(anchor_id)s"].index];
			});

		groups["%(anchor_id)s"] = function (d) {return "";};

		charts["%(anchor_id)s"]
			.dimension(dims["%(anchor_id)s"])
			.group(groups["%(anchor_id)s"])
			.size(options["%(anchor_id)s"].maxsize)
			.columns(options["%(anchor_id)s"].columns)
			.sortBy(function (d) {return d[options["%(anchor_id)s"].sortBy];})
			;
	""" % dict(anchor_id = anchor_id, index = index,
		maxsize = maxsize, columnstr = ", ".join(map(lambda c: '"%s"'%c, columns)), 
		sortBy = sortBy, cf_obj = cf_obj)
	return (div, jscode)

ALL_CHARTS = {
	"categorical_histogram_bar": categorical_histogram_bar
	, "categorical_histogram_row": categorical_histogram_row
	, "categorical_timeseries_area": categorical_timeseries_area
	, "categorical_pair_heatmap": categorical_pair_heatmap
	, "numerical_timeseries_line": numerical_timeseries_line
	, "numerical_pair_scatter": numerical_pair_scatter
	, "numerical_pair_by_categorical_bubble": numerical_pair_by_categorical_bubble
	, "numerical_by_categorical_box": numerical_by_categorical_box
	, "data_table": data_table
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

def embed_charts(data_url, charts_code, cf_obj = "ndx"):
	return r"""
	d3.json("%(data_url)s", function (err, data) {

		var %(cf_obj)s = crossfilter(data);

		// currently supported aggregation functions
		var aggfuns = {
			"average": {
				// reduce add
				"add": function (feature) {
					return function (p, v) {
						p.result = (p.result*p.count + v[feature]) / (p.count + 1);
						p.count += 1;
						return p;
					};
				}
				// reduce remove
				, "remove": function (feature) {
					return function (p, v) {
						if (p.count === 1) {
							p = {result: 0.0, count: 0};
						} else {
							p.result = (p.result*p.count - v[feature]) / (p.count - 1);
							p.count -= 1;}
						return p;
					};
				}
				// reduce init
				, "init": function (feature) {return function () {return {result: 0.0, count: 0};} }
			}
			, "sum": {
				// reduce add
				"add": function (feature) {
					return function (p, v) {
						p.result +=  v[feature];
						return p;
					};
				}
				// reduce remove
				, "remove": function (feature) {
					return function (p, v) {
						p.result -=  v[feature];
						return p;
					};
				}
				// reduce init
				, "init": function (feature) {return function () {return {result: 0.0};} }
			}
			, "count": {
				// reduce add
				"add": function (feature) {
					return function (p, v) {
						p.result +=  1;
						return p;
					};
				}
				// reduce remove
				, "remove": function (feature) {
					return function (p, v) {
						p.result -=  1;
						return p;
					};
				}
				// reduce init
				, "init": function (feature) {return function () {return {result: 0};} }
			}
			, "combine": {
				"add": function (features, aggs) {
					add_fns = [];
					for (var i = 0; i < features.length; ++i) {
						add_fns.push(aggfuns[aggs[i]]["add"](features[i]));
					}
					return function (p, v) {
						for (var i = 0; i < features.length; ++i) {
							p[i] = add_fns[i](p[i], v);
						}
						return p;
					};
				}
				, "remove": function (features, aggs) {
					remove_fns = [];
					for (var i = 0; i < features.length; ++i) {
						remove_fns.push(aggfuns[aggs[i]]["remove"](features[i]));
					}
					return function (p, v) {
						for (var i = 0; i < features.length; ++i) {
							p[i] = remove_fns[i](p[i], v);
						}
						return p;
					};
				}
				, "init": function (features, aggs) {
					init_fns = [];
					for (var i = 0; i < features.length; ++i) {
						init_fns.push(aggfuns[aggs[i]]["init"](features[i]));
					}
					return function () {
						p = []
						for (var i = 0; i < features.length; ++i) {
							p.push( init_fns[i]() );
						}
						return p;
					};
				}
			}
		};

		// color scheme for heatmap, obtained from http://colorbrewer2.org/
		var colorRangeScheme = {
			green: ["#c7e9c0", "#00441b"],
			organge: ["#fdd0a2", "#7f2704"],
			purple: ["#dadaeb", "#3f007d"],
			red: ["#fcbba1", "#67000d"],
			blue: ["#c6dbef", "#08306b"],
			yor: ["#ffffcc", "#800026"],
			bg: ["#ccece6", "#00441b"],
			yg: ["#f7fcb9", "#004529"],
			yob: ["#fff7bc", "#662506"],
			or: ["#fee8c8", "#7f0000"],
			pb: ["#d0d1e6", "#023858"]
		};

		var minmax_value = function (group) {
			// assume group is ordered by value
			var xs = group.order(function (p) {return p.result;}).top(Infinity);
			return [xs[xs.length - 1].value.result, xs[0].value.result];
		};

		var charts = {},
			dims = {},
			groups = {},
			options = {};

		%(charts_code)s

		dc.renderAll();
	});
	""" % dict(data_url = data_url, charts_code = charts_code, cf_obj = cf_obj)

## Crossfiltered chart dashboard for a dataset - main interface
def plot_dataset(data_url, charts, cf_obj="ndx"):
	"""
	data: url of JSON data
	charts: list of [(chartid : {charttype: ??, params: ??}), ...].
			the supported chart types are in ALL_CHARTS variable in plots module.
	RETURN: tuple of divs and all-in-script: ({chartid: div, ...}, script-snippet)
	"""
	divs, plots = {}, []
	for chartid, config in charts: 
		div, plot = ALL_CHARTS[config["charttype"]](chartid, cf_obj=cf_obj, **config["params"])
		divs[chartid] = div 
		plots.append(plot)
	return (divs, embed_charts(data_url, "\n".join(plots), cf_obj))
