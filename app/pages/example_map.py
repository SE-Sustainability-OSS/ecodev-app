"""
Module implementing an example of map (using plotly)
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front.components import background_card

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.front_test import LEFT_ASIDE_EXAMPLE
from app.front_test import page_left_aside
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
    page = page_left_aside(
        aside_content=LEFT_ASIDE_EXAMPLE,
        page_content=background_card([MAP_GRAPH]))
    return generic_page(token, page)
