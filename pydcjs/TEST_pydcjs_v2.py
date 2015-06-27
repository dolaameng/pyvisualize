from flask import Flask, render_template
from dcjs import plots 

app = Flask("pydcjs test v2")

@app.route("/test-pydcjs/snacks-iris")
def snacks_iris():
    snacks_data_url = "/static/data/modified_snacks.json"
    snacks_charts = [
    ("location-bar-plot", {"charttype": "categorical_histogram_bar"
                    , "params": {"feature": "location"
                                , "width": 600
                                , "height": 300
                                , "xAxisLabel": "Location"
                                , "yAxisLabel": "Frequency"}})
    # , ("neighborhood-row-plot", {"charttype": "categorical_histogram_row"
    #                             , "params": {"feature": "neighborhood"
    #                                         , "width": 600
    #                                         , "height": 600}})
    , ("withwho-area-daily-plot", {"charttype": "categorical_timeseries_area"
                                   , "params": {"timefeature": "date"
                                                , "feature": "withwho"
                                                , "width": 800
                                                , "height": 300
                                                , "margins": dict(top=10, right=50, bottom=30, left=100)
                                                , "xAxisLabel": "Daily"
                                                , "yAxisLabel": "Withwho Dist"}})
    # , ("location-period-hm-plot", {"charttype": "categorical_pair_heatmap"
    #                                 , "params": {"column_feature": "location"
    #                                             , "index_feature": "period"
    #                                             , "value_feature": ""
    #                                             , "tooltip_prefix": "count:"
    #                                             , "aggfun": "count"
    #                                             , "width": 500
    #                                             , "height": 300
    #                                             , "margins": dict(top=10,right=50,bottom=30,left=100)
    #                                             , "color_scheme": "red"}})
    , ("avghealth-location-period-hm-plot", {"charttype": "categorical_pair_heatmap"
                                    , "params": {"column_feature": "location"
                                                , "index_feature": "period"
                                                , "value_feature": "healthlevel"
                                                , "tooltip_prefix": "avg healthlevel:"
                                                , "aggfun": "average"
                                                , "width": 500
                                                , "height": 300
                                                , "margins": dict(top=10,right=50,bottom=30,left=100)
                                                , "color_scheme": "green"}})
    # , ("healthlevel-daily-plot", {"charttype": "numerical_timeseries_line"
    #                                , "params": {"timefeature": "date"
    #                                             , "feature": "healthlevel"
    #                                             , "aggfun": "average"
    #                                             , "width": 600
    #                                             , "height": 300
    #                                             , "xAxisLabel": "Daily"
    #                                             , "yAxisLabel": "Avg healthlevel"}})
    , ("lat-lon-scatter-plot", {"charttype": "numerical_pair_scatter"
                                   , "params": {"x_feature": "latitude"
                                                , "y_feature": "longitude"
                                                , "width": 500
                                                , "height": 400
                                                , "xAxisLabel": "Latitude"
                                                , "yAxisLabel": "Longitude"
                                                , "margins": dict(bottom = 50)}})
    # , ("health-hour-scatter-plot", {"charttype": "numerical_pair_scatter"
    #                                , "params": {"x_feature": "hour"
    #                                             , "y_feature": "healthlevel"
    #                                             , "width": 500
    #                                             , "height": 400
    #                                             , "xAxisLabel": "Hour"
    #                                             , "yAxisLabel": "Healthlevel"
    #                                             , "margins": dict(bottom = 50)}})
    , ("cost-lat-lon-bubble-plot", {"charttype": "numerical_pair_by_categorical_bubble"
                                   , "params": {"group_feature": "cost"
                                                , "x_feature": "what_wordlen"
                                                , "y_feature": "why_wordlen"
                                                , "r_feature": None
                                                , "x_aggfun": "average"
                                                , "y_aggfun": "average"
                                                , "r_aggfun": "count"
                                                , "width": 800
                                                , "height": 600
                                                , "max_bubble": 5000
                                                , "xAxisLabel": "avg what desc"
                                                , "yAxisLabel": "avg why desc"
                                                , "margins": dict(bottom = 50)}})
    # , ("healthlevel-withwho-box-plot", {"charttype": "numerical_by_categorical_box"
    #                                , "params": {"group_feature": "withwho"
    #                                             , "numerical_feature": "healthlevel"
    #                                             , "width": 400
    #                                             , "height": 200
    #                                             , "xAxisLabel": "withwho"
    #                                             , "yAxisLabel": "healthlevel"
    #                                             , "margins": dict(bottom = 50)}})
    , ("snacks-data-table", {"charttype": "data_table"
                            , "params": {"index": "timestamp"
                                        , "maxsize": 10
                                        , "columns": ["timestamp","snacks", "healthlevel", "period", "withwho", "why"]
                                        , "sortBy": "timestamp"}})]
    
    
    iris_data_url = "/static/data/iris.json"
    iris_charts = [("iris-sepal-scatter-plot", {"charttype": "numerical_pair_scatter"
                                                , "params": {"x_feature": "sepallen"
                                                            , "y_feature": "sepalwdh"
                                                            , "xAxisLabel": "sepal len"
                                                            , "yAxisLabel": "sepal width"}})
        , ("iris-petal-scatter-plot", {"charttype": "numerical_pair_scatter"
                                                , "params": {"x_feature": "petallen"
                                                            , "y_feature": "petalwdh"
                                                            , "xAxisLabel": "petal len"
                                                            , "yAxisLabel": "petal width"}})
        , ("iris-sepallen-sepalwdh-bubble-plot", {"charttype": "numerical_pair_by_categorical_bubble"
                                   , "params": {"group_feature": "flower"
                                                , "x_feature": "sepallen"
                                                , "y_feature": "sepalwdh"
                                                , "r_feature": ""
                                                , "x_aggfun": "average"
                                                , "y_aggfun": "average"
                                                , "r_aggfun": "count"
                                                , "width": 800
                                                , "height": 600
                                                , "max_bubble": 5000
                                                , "xAxisLabel": "avg sepal len"
                                                , "yAxisLabel": "avg sepal width"
                                                , "margins": dict(bottom = 50)}})
        , ("iris-data-table", {"charttype": "data_table"
                                        , "params": {"index": "id"
                                                    , "maxsize": 10
                                                    , "columns": ["id", "flower", "sepallen", "sepalwdh", "petallen", "petalwdh"]
                                                    , "sortBy": "id"}})]

    css_header = plots.cdn_css()
    js_header = plots.cdn_script()
    
    snacks_html_divs, snacks_js_plot = plots.plot_dataset(snacks_data_url, snacks_charts, cf_obj="ndx_snacks")
    iris_html_divs, iris_js_plot = plots.plot_dataset(iris_data_url, iris_charts, cf_obj="ndx_iris")

    print 'run'

    return render_template("snacks-iris.html",
        css_header = css_header,
        js_header = js_header,
        snacks_html_divs = snacks_html_divs,
        snacks_js_plot = snacks_js_plot,
        iris_html_divs = iris_html_divs,
        iris_js_plot = iris_js_plot)


@app.route("/test-pydcjs/iris")
def iris():
    iris_data_url = "/static/data/iris.json"
    iris_charts = [("iris-sepal-scatter-plot", {"charttype": "numerical_pair_scatter"
                                                , "params": {"x_feature": "sepallen"
                                                            , "y_feature": "sepalwdh"
                                                            , "xAxisLabel": "sepal len"
                                                            , "yAxisLabel": "sepal width"}})
        , ("iris-petal-scatter-plot", {"charttype": "numerical_pair_scatter"
                                                , "params": {"x_feature": "petallen"
                                                            , "y_feature": "petalwdh"
                                                            , "xAxisLabel": "petal len"
                                                            , "yAxisLabel": "petal width"}})
        , ("iris-sepallen-sepalwdh-bubble-plot", {"charttype": "numerical_pair_by_categorical_bubble"
                                   , "params": {"group_feature": "flower"
                                                , "x_feature": "sepallen"
                                                , "y_feature": "sepalwdh"
                                                , "r_feature": ""
                                                , "x_aggfun": "average"
                                                , "y_aggfun": "average"
                                                , "r_aggfun": "count"
                                                , "width": 800
                                                , "height": 600
                                                , "max_bubble": 5000
                                                , "xAxisLabel": "avg sepal len"
                                                , "yAxisLabel": "avg sepal width"
                                                , "margins": dict(bottom = 50)}})
        , ("iris-data-table", {"charttype": "data_table"
                                        , "params": {"index": "id"
                                                    , "maxsize": 10
                                                    , "columns": ["id", "flower", "sepallen", "sepalwdh", "petallen", "petalwdh"]
                                                    , "sortBy": "id"}})]
    css_header = plots.cdn_css()
    js_header = plots.cdn_script()
    iris_html_divs, iris_js_plot = plots.plot_dataset(iris_data_url, iris_charts, cf_obj="ndx_iris")
    return render_template("iris.html",
        css_header = css_header,
        js_header = js_header,
        iris_html_divs = iris_html_divs,
        iris_js_plot = iris_js_plot)

app.run(debug = True, port = 8080)

