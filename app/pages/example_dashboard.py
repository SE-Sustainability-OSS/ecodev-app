"""
Module implementing the example of a dashboard output
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.pages.dashboard_page.dashboard import DASHBOARD

log = logger_get(__name__)
register_page(__name__, path='/outputs/dashboards')
PAGE_ID = 'output-example-dashboard-page'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a output dashboard using card and dashmantine components.
    """
    return generic_page(token, DASHBOARD)
