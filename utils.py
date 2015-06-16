from IPython.display import HTML, Javascript
import jinja2
import json

def _deprecated_ipython_plot_zing_data(plot_data, div_name, width = 600, height = 400):
    """
    plot_data: JSON format of data to be plot
    """
    #header = """<script src="http://cdn.zingchart.com/zingchart.min.js"></script>"""
    #module_header = """<script>zingchart.MODULESDIR="http://cdn.zingchart.com/modules/";</script>"""
    header = """<script src="zingchart_js/zingchart.min.js"></script>"""
    module_header = """<script>zingchart.MODULESDIR="zingchart_js/modules/";</script>"""
    plot_area = """<div id='%s'></div>""" % div_name
    plot_fn = """
        <script>
            zingchart.render({
            id:'%s',
            height:%i,
            width:%i,
            data:%s
          });
        </script>
    """ % (div_name, height, width, json.dumps(plot_data))

    return HTML(header+module_header+plot_area+plot_fn)


def iframe(stuff, width = None, height = None):
    width = width or "100%"
    height = height or "500px"
    stuff = stuff.replace('"', '&quot;')
    return HTML("""<iframe srcdoc="{srcdoc}" style='width:{width}; height: {height}; border: none'></iframe>"""
                .format(srcdoc = stuff, width = width, height = height))

def ipython_plot_zingchart(plot_data, div_id = None, width=None, height=None):
    div_id = div_id or "zingchart-plot"
    head = HTML("""
    <head>
        <script src="http://cdn.zingchart.com/zingchart.min.js"></script>
        <script>zingchart.MODULESDIR="http://cdn.zingchart.com/modules/";</script>
    </head>
    """)
    body = HTML("""<div id="%s"></div>""" % div_id)
    zc_template = """
    zingchart.render({
        "id": "%s"
        , "width": 600
        , "height": 400
        , "data": %s
    });
    """
    plot_js = Javascript(zc_template % (div_id, json.dumps(plot_data)))
    return iframe(head.data + body.data + "<script>" + plot_js.data + "</script>", width , height)

def ipython_plot_dcjs():
    pass
    return None 