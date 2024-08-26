"""
Example of a page with a simple / no layouts.

Note: It still requires some boiler plate code to ensure that the page
can only be accessed by users who are authenticated.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from dash import State
from ecodev_core import safe_get_user
from ecodev_front import APPSHELL
from ecodev_front import ASIDE
from ecodev_front import NAVBAR
from ecodev_front import TOKEN
from ecodev_front import URL

from app.components.page_helpers import generic_page
from app.pages.layouts import LEFT_ASIDE_PAGE_URL
from app.pages.layouts import LEFT_RIGHT_ASIDE_PAGE_URL
from app.pages.layouts import RIGHT_ASIDE_PAGE_URL
from app.pages.layouts import SIMPLE_PAGE_ID
from app.pages.layouts import SIMPLE_PAGE_URL

register_page(__name__, path=SIMPLE_PAGE_URL)

layout = [html.Div(id=SIMPLE_PAGE_ID,
                   style={'display': 'flex', 'justifyContent': 'center'}
                   )]


@callback(Output(SIMPLE_PAGE_ID, 'children'),
          Input(TOKEN, 'data'))
def simple_page_layout_example(token: dict):
    """
    Example of a simple page
    """
    page = dmc.Container(['This is a simple page'])

    return generic_page(token, page)


@callback(Output(APPSHELL, NAVBAR),
          Output(APPSHELL, ASIDE),
          Input(URL, 'pathname'),
          State(TOKEN, 'data'))
def rendering_page_layouts(pathname: str, token: dict):
    """
    Callback rendering all pages layouts.

    Note: This should be the only callback controlling the aside.
    It should ideally be placed in the root file (dash_app.py).

    The content for each of these should be inserted through another callback
    """
    if safe_get_user(token):
        if pathname == LEFT_ASIDE_PAGE_URL:
            return {'width': '20%'}, {'width': 0}
        if pathname == RIGHT_ASIDE_PAGE_URL:
            return {'width': 0}, {'width': '15%'}
        if pathname == LEFT_RIGHT_ASIDE_PAGE_URL:
            return {'width': '20%'}, {'width': '15%'}
    return {'width': 0}, {'width': 0}
