from IPython.display import HTML
import json

def ipython_plot_zing_data(plot_data, div_name, width = 600, height = 400):
    """
    plot_data: JSON format of data to be plot
    """
    header = """<script src="http://cdn.zingchart.com/zingchart.min.js"></script>"""
    module_header = """<script>zingchart.MODULESDIR="http://cdn.zingchart.com/modules/";</script>"""
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