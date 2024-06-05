"""
Module implementing the example of a form input
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.pages.form_page.form import get_example_form

log = logger_get(__name__)
register_page(__name__, path='/inputs/forms')
PAGE_ID = 'input-example-form-page'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a input form using dmc_utils components.
    """
    return generic_page(token, get_example_form())
