from collections import namedtuple

from bokeh.charts import Line
from bokeh.embed import components
from bokeh.io import hplot
from bokeh.resources import CDN, INLINE

RESOURCE = CDN
Plot = namedtuple("Plot", "bokehjs css script div")
empty_plot = Plot("", "", "", "")


def loss_accuracy_plot(df, x, y):
    df = df.fillna(0)
    plot = hplot(*[Line(df, x, y, legend=True) for y in y])
    script, div = components(plot, INLINE)
    js_resources = RESOURCE.render_js()
    css_resources = RESOURCE.render_css()
    return Plot(js_resources, css_resources, script, div)
