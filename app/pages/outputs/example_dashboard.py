"""
Module implementing the example of a dashboard output
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.pages.outputs import DASHBOARD_PAGE_ID
from app.pages.outputs import DASHBOARD_PAGE_URL
from app.pages.outputs.dashboard_page.dashboard import DASHBOARD

log = logger_get(__name__)
register_page(__name__, path=DASHBOARD_PAGE_URL)

layout = [html.Div(id=DASHBOARD_PAGE_ID, className='centered')]


@callback(Output(DASHBOARD_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a output dashboard using card and dashmantine components.
    """
    return generic_page(token, DASHBOARD)
