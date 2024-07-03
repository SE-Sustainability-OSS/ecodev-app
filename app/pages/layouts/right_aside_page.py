"""
Example of a page with a right-aside.

Note: The right-aside is called 'aside' in dash-mantine.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from dash import State
from ecodev_core import safe_get_user
from ecodev_front import RIGHT_ASIDE_ID
from ecodev_front import TOKEN
from ecodev_front import URL

from app.components.page_helpers import generic_page
from app.pages.layouts import RIGHT_ASIDE_PAGE_ID
from app.pages.layouts import RIGHT_ASIDE_PAGE_URL


register_page(__name__, path=RIGHT_ASIDE_PAGE_URL)

layout = [html.Div(id=RIGHT_ASIDE_PAGE_ID)]


@callback(Output(RIGHT_ASIDE_ID, 'children'),
          Input(URL, 'pathname'),
          State(TOKEN, 'data'))
def enable_right_aside(pathname: str, token: dict):
    """
    Callback rendering the left aside (setting width and content)
    """
    right_aside_content = dmc.Text('Example of right aside content',
                                   fz=24, style={'padding': '20px'})
    if safe_get_user(token) and pathname == RIGHT_ASIDE_PAGE_URL:
        return right_aside_content


@callback(Output(RIGHT_ASIDE_PAGE_ID, 'children'),
          Input(TOKEN, 'data'))
def render_page(token: dict):
    """
    Callback rendering the page's main content.
    """
    page = dmc.Container(['This content is offset by the right aside'])

    return generic_page(token, page)
