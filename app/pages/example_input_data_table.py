"""
Module implementing an example of data table (using Dash AgGrid).
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front.components import data_table
from plotly.data import iris

from app.components.page_helpers import generic_page
from app.constants import TOKEN


log = logger_get(__name__)
register_page(__name__, path='/inputs/data-table')

PAGE_ID = 'inputs-example-data-table'
DATA_TABLE = 'data-table'

layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
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
