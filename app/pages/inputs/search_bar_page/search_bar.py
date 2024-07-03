"""
Module implementing a search bar example page
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from ecodev_front import background_card
from ecodev_front import search_bar

from app.pages.inputs.search_bar_page import SEARCH_BAR_ID
from app.pages.inputs.search_bar_page import SEARCH_OUTPUT_ID

SEARCH = search_bar(id=SEARCH_BAR_ID, label='Search something',
                    helper="This search bar isn't really useful. Neither is this helper.")
SEARCH_OUTPUT = html.Div(id=SEARCH_OUTPUT_ID, style={'width': '100%'})
SEARCH_COMPONENTS = dmc.Stack([dmc.Space(h=10), SEARCH, dmc.Space(h=20),  SEARCH_OUTPUT],
                              className='centered')


@callback(Output(SEARCH_OUTPUT, 'children'), Input(SEARCH_BAR_ID, 'value'))
def search(search_term: str) -> dmc.Card:
    """
    Search bar example page
    """
    if search_term.lower() == 'something' or search_term == '42':
        return background_card([dmc.Text('You beautiful soul <3', italic=True)])
    return background_card([dmc.Text(search_term)]) if search_term else None
