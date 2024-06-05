"""
Module implementing a main search bar on a page.
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.pages.search_bar_page.search_bar import SEARCH_COMPONENTS

log = logger_get(__name__)
register_page(__name__, path='/inputs/search-bar')
PAGE_ID = 'input-example-search-bar'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example usage of a search-bar component
    """
    return generic_page(token, SEARCH_COMPONENTS)
