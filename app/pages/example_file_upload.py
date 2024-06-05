"""
Module implementing the example of a form input
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components import generic_page
from app.constants import TOKEN
from app.pages.file_upload_page.file_upload import UPLOADERS

log = logger_get(__name__)
register_page(__name__, path='/inputs/file-upload')
PAGE_ID = 'input-example-upload-page'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a input upload box & template download button, using dmc_utils components.
    """

    return generic_page(token, UPLOADERS)
