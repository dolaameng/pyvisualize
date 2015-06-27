from flask import Flask, render_template
from dcjs import plots 

app = Flask("pydcjs test v2")

@app.route("/test-pydcjs/snacks")
def snacks():
    data_url = "/static/data/modified_snacks.json"
    charts = [
    ("location-bar-plot", {"charttype": "categorical_histogram_bar"
                    , "params": {"feature": "location"
                                , "width": 600
                                , "height": 300
                                , "xAxisLabel": "Location"
                                , "yAxisLabel": "Frequency"}})
    , ("neighborhood-row-plot", {"charttype": "categorical_histogram_row"
                                , "params": {"feature": "neighborhood"
                                            , "width": 600
                                            , "height": 600}})
    , ("withwho-area-daily-plot", {"charttype": "categorical_timeseries_area"
                                   , "params": {"timefeature": "date"
                                                , "feature": "withwho"
                                                , "width": 800
                                                , "height": 300
                                                , "margins": dict(top=10, right=50, bottom=30, left=100)
                                                , "xAxisLabel": "Daily"
                                                , "yAxisLabel": "Withwho Dist"}})
    , ("location-period-hm-plot", {"charttype": "categorical_pair_heatmap"
                                    , "params": {"column_feature": "location"
                                                , "index_feature": "period"
                                                , "value_feature": ""
                                                , "tooltip_prefix": "count:"
                                                , "aggfun": "count"
                                                , "width": 500
                                                , "height": 300
                                                , "margins": dict(top=10,right=50,bottom=30,left=100)
                                                , "color_scheme": "red"}})
    , ("avghealth-location-period-hm-plot", {"charttype": "categorical_pair_heatmap"
                                    , "params": {"column_feature": "location"
                                                , "index_feature": "period"
                                                , "value_feature": "healthlevel"
                                                , "tooltip_prefix": "avg healthlevel:"
                                                , "aggfun": "average"
                                                , "width": 500
                                                , "height": 300
                                                , "margins": dict(top=10,right=50,bottom=30,left=100)
                                                , "color_scheme": "green"}})]
    pydcjs_css_header = plots.cdn_css()
    pydcjs_js_header = plots.cdn_script()
    pydcjs_html_divs, pydcjs_js_plot = plots.plot_dataset(data_url, charts)
    return render_template("snacks.html",
        pydcjs_css_header = pydcjs_css_header,
        pydcjs_js_header = pydcjs_js_header,
        pydcjs_html_divs = pydcjs_html_divs,
        pydcjs_js_plot = pydcjs_js_plot)

app.run(debug = True, port = 8080)
