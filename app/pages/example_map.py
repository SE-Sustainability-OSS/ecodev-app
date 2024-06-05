"""
Module implementing an example of map (using plotly)
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import background_card

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.pages.map_page.map import MAP_GRAPH

log = logger_get(__name__)
register_page(__name__, path='/outputs/map')
PAGE_ID = 'outputs-example-map'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example usage of a map component (using plotly).
    Component includes some defaults which can be overridden.
    """
    page = background_card([MAP_GRAPH], style={'width': '80vw'})
    return generic_page(token, page)
