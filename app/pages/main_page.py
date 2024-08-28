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
from ecodev_front import centered_div
from ecodev_front import URL

from app.components.intro import CREDENTIALS_SECTION
from app.components.intro import INTRO_SECTION

log = logger_get(__name__)
register_page(__name__, path='/')

PAGE_ID = 'main-page'
layout = [html.Div(id=PAGE_ID)]


@callback(Output(PAGE_ID, 'children'),
          Input(URL, 'pathname'))
def get_main_page(pathname):
    """
    Renders main page.
    Note - This page is visible without user login.

    """
    return dmc.Container(
        size='md',
        children=[
            INTRO_SECTION,
            centered_div(dmc.Divider(w='100%', mt=50, mb=50)),
            CREDENTIALS_SECTION,
        ])
