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

from app.components import generic_page
from app.pages.inputs import FILE_UPLOAD_PAGE_ID
from app.pages.inputs import FILE_UPLOAD_PAGE_URL
from app.pages.inputs.file_upload_page.file_upload import UPLOADERS

log = logger_get(__name__)
register_page(__name__, path=FILE_UPLOAD_PAGE_URL)

layout = [html.Div(id=FILE_UPLOAD_PAGE_ID, className='centered')]


@callback(Output(FILE_UPLOAD_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a input upload box using dmc_utils components.

    Note: The callback triggered by the box is found under ./file_upload_page/file_upload.py
    """
    return generic_page(token, UPLOADERS)
