"""
Module implementing the example of a form input
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.front_test import page_left_right_asides

log = logger_get(__name__)


LAYOUT_LEFT_RIGHT_ASIDE_PAGE_ID = 'layout-left-right-asides-page'
LAYOUT_LEFT_RIGHT_ASIDE_PAGE_URL = '/layouts/left-right-asides'

register_page(__name__, path=LAYOUT_LEFT_RIGHT_ASIDE_PAGE_URL)

layout = [html.Div(id=LAYOUT_LEFT_RIGHT_ASIDE_PAGE_ID, className='centered')]


@callback(Output(LAYOUT_LEFT_RIGHT_ASIDE_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a output report using dmc_utils components.
    """
    page = page_left_right_asides(
        left_aside=dmc.Text('left-aside'),
        right_aside=dmc.Text('right-aside'),
        page_content=dmc.Text('main-content'),

    )
    return generic_page(token, page)
