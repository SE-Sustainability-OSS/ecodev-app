"""
Module implementing the example of a form input
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.pages.inputs import FORMS_PAGE_ID
from app.pages.inputs import FORMS_PAGE_URL
from app.pages.inputs.form_page.form import get_example_form

log = logger_get(__name__)
register_page(__name__, path=FORMS_PAGE_URL)

layout = [html.Div(id=FORMS_PAGE_ID, className='centered')]


@callback(Output(FORMS_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a input form using dmc_utils components.
    """
    return generic_page(token, get_example_form())
