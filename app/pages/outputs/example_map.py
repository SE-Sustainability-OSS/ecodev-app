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
from ecodev_front import card_title
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.pages.outputs import MAP_PAGE_ID
from app.pages.outputs import MAP_PAGE_URL
from app.pages.outputs.map_page.map import MAP_GRAPH

log = logger_get(__name__)
register_page(__name__, path=MAP_PAGE_URL)

layout = [html.Div(id=MAP_PAGE_ID, className='centered')]


@callback(Output(MAP_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example usage of a map component (using plotly).
    Component includes some defaults which can be overridden.
    """
    page = background_card([card_title('Example of map component'), MAP_GRAPH])
    return generic_page(token, page)
