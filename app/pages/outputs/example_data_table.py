"""
Module implementing an example of a data table (using Dash AgGrid).
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.pages.outputs import OUT_DATA_TABLE_PAGE_ID
from app.pages.outputs import OUT_DATA_TABLE_PAGE_URL
from app.pages.outputs.data_table_page.data_table import get_example_table

log = logger_get(__name__)
register_page(__name__, path=OUT_DATA_TABLE_PAGE_URL)

layout = [html.Div(id=OUT_DATA_TABLE_PAGE_ID, className='centered')]


@callback(Output(OUT_DATA_TABLE_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example usage of a data-table component (Dash AgGrid).
    Component includes some defaults which can be overridden.
    """
    page = html.Div([get_example_table()], style={'width': '90vw'})
    return generic_page(token, page)
