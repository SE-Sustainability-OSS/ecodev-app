"""
Module implementing an example of data table (using Dash AgGrid).
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import data_table
from ecodev_front import TOKEN
from plotly.data import iris

from app.components.page_helpers import generic_page
from app.pages.inputs import IN_DATA_TABLE_PAGE_ID
from app.pages.inputs import IN_DATA_TABLE_PAGE_URL


log = logger_get(__name__)
register_page(__name__, path=IN_DATA_TABLE_PAGE_URL)

DATA_TABLE = 'data-table'

layout = [html.Div(id=IN_DATA_TABLE_PAGE_ID, className='centered')]


@callback(Output(IN_DATA_TABLE_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example usage of a data-table component (Dash AgGrid).
    Component includes some defaults which can be overridden.
    """
    page = html.Div(
        [data_table(id=DATA_TABLE, df=iris(), style={'height': '80vh'})],
        style={'width': '90vw'},
    )
    return generic_page(token, page)
