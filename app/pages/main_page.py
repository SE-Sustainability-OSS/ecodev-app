"""
Module implementing the main page

NB: try to keep your pages as small as this one, isolating components/plots in dedicated modules.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page

log = logger_get(__name__)
register_page(__name__, path='/')
PAGE_ID = 'main-page'
layout = [html.Div(id=PAGE_ID)]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def get_main_page(token):
    """
    Renders main page.
    """
    page = dmc.Text('Main page')
    return generic_page(token, page)
