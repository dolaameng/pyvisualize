import numpy as np 
import pandas as pd 
from itertools import cycle


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
    #                   for i, (c, lower, upper) in enumerate(zip(colnames, lowers, uppers))]
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


def scatterplot(data, xname, yname, markers = None, colors = None, plot_options = None):
    """
    data: pd.DataFrame OR dict of {class1: dataframe1, ...}
    xname, yname: both are string, column names in data frame 
    markers: a string (see zingchart marker type) or a dict of string (with same keys if data is a dictionary), optional
    colors: a string (see zingchart color type) or a dict of string (with same keys if data is a dictionary), optional
    plot_options: other options to zing chart, e.g. , 'ScaleX' and etc.

    return plot_data: json for zingchart plot data 
    """
    if type(data) != dict:
        data = {"data": data}

    markers = ["circle"] if markers is None else ([markers] if type(markers) == str else markers)
    colors = ["blue"] if colors is None else ([colors] if type(colors) == str else colors)

    series = [{
                  "marker": {"type": m, "background-color": c}
                , "text": dname 
                , "values": df.loc[:, [xname, yname]].get_values().tolist()
                } for (dname, df), m, c in zip(data.items(), cycle(markers), cycle(colors))]

    plot_data = {
          "type": "scatter"
        , "scale-x": {"label": {"text": xname}}
        , "scale-y": {"label": {"text": yname}}
        , "legend": {}
        , "series": series 
    }
    if plot_options:
        plot_data.update(plot_options)
    return plot_data

def histogram(data, bins=10, plot_options=None):
    """
    data: array_like. E.g. pd.series or list; 
          OR pd.DataFrame (for tabular data) 
          OR dict of {seriesName: seriesData} (for irregular shape data)
    bins: int or sequence of scalars, optional
    plot_options: other options to zing chart

    return plot_data: json for zingchart plot data 
    """
    if isinstance(data, (list, np.ndarray, pd.Series)): 
        hists = {"Histogram": np.histogram(data, bins=bins)}

    elif isinstance(data, pd.DataFrame):
        hists = data._get_numeric_data().apply(np.histogram, axis=0, bins=bins)

    elif isinstance(data, dict):
        hists = dict((k, np.histogram(v, bins=bins)) for k, v in data.iteritems())
    
    plot_data = {
        "background-color": "#3F5666",
        "graphset": []
    }
    for name in hists.keys():
        sub_plot_data = {
            "type": "bar", 
            "series": [{"values": hists[name][0].tolist()}],
            "scale-x": {"values": np.around(hists[name][1], decimals=2).tolist()}, 
            "tooltip": {
                "text": "<b>Value: %k</b><br><b>Count: %v</b>",
                "font-size": "12px",
                "text-align": "left",
                "border-radius": "8px",
                "padding": "5px 5px",
                # "background-color": "#212339",
                "alpha": 0.9
            },
            "title": {
                "text": name, 
                "background-color":"none",
                "font-color":"#000000"
            }
        }
        plot_data["graphset"].append(sub_plot_data)

    if plot_options:
        plot_data.update(plot_options)
    return plot_data