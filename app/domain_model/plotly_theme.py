"""
File containing the ecoapp plotly graphing template and setting it as default.
Also declares the PLOTLY_TOOLS (as this file needs to be imported), which can be customized for
specific usage.
"""
import plotly.graph_objects as go
import plotly.io as pio

from app.domain_model.color_utils import color_scale
from app.domain_model.color_utils import color_way
from app.domain_model.color_utils import diverging_scale
from app.domain_model.color_utils import get_color


PLOTLY_TOOLS = [
    'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
    'hoverCompareCartesian', 'zoom3d', 'pan3d', 'resetCameraDefault3d',
    'resetCameraLastSave3d', 'hoverClosest3d', 'orbitRotation', 'tableRotation',
    'hoverClosestGeo', 'toImage', 'sendDataToCloud',
    'hoverClosestGl2d', 'hoverClosestPie', 'toggleHover',
    'resetViews', 'toggleSpikelines', 'resetViewMapbox'
]


pio.templates['ecoapp'] = go.layout.Template(
    layout={
        'colorway': color_way(),
        'coloraxis': {
            'colorbar': {
                'outlinewidth': 0,
                'tickcolor': get_color('gray.3'),
                'ticklen': 6,
                'ticks': 'inside'
            }
        },
        'colorscale': {
            'diverging': diverging_scale(),
            'sequential': color_scale(),
            'sequentialminus': color_scale(reversed=True),
        },

        'polar': {'angularaxis': {'gridcolor': get_color('gray.3'),
                                  'linecolor': get_color('gray.3'),
                                  'showgrid': True,
                                  'tickcolor': get_color('gray.9'),
                                  'ticks': 'outside'},
                  'bgcolor': get_color('gray.2'),
                  'radialaxis': {'gridcolor': get_color('gray.3'),
                                 'linecolor': get_color('gray.3'),
                                 'showgrid': True,
                                 'tickcolor': get_color('gray.9'),
                                 'ticks': 'outside'}},
        'shapedefaults': {'fillcolor': 'black', 'line': {'width': 0}, 'opacity': 0.3, },

        'xaxis': {'automargin': True,
                  'gridcolor': get_color('gray.3'),
                  'linecolor': get_color('gray.3'),
                  'showgrid': False,
                  'tickcolor': get_color('gray.9'),
                  'ticks': 'outside',
                  'title': {'standoff': 15},
                  'zerolinecolor': get_color('gray.3')},

        'yaxis': {'automargin': True,
                  'gridcolor': get_color('gray.3'),
                  'linecolor': get_color('gray.3'),
                  'showgrid': True,
                  'tickcolor': get_color('gray.9'),
                  'ticks': 'outside',
                  'title': {'standoff': 15},
                  'zerolinecolor': get_color('gray.3')},


        'title': {'xanchor': 'left',
                  'x': 0.05,
                  'font': {'family': 'Averta',
                           'size': 20,
                           'weight': 700}},

        'font': {'family': 'Averta',
                 'color': get_color('gray.9'),
                 'size': 12,
                 'textcase': 'word caps'},
        'uniformtext': {'minsize': 12,
                        'mode': 'hide'},


        'hoverlabel': {'align': 'left'},
        'hovermode': 'closest',

        'dragmode': False,
        'autotypenumbers': 'convert types',


        'paper_bgcolor': get_color('gray.1'),
        'plot_bgcolor': get_color('gray.1'),
    }
)

pio.templates.default = 'ecoapp'
