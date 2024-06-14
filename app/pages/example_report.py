"""
Module implementing the example of a form input
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get

from app.components.page_helpers import generic_page
from app.constants import TOKEN
from app.front_test import LEFT_ASIDE_EXAMPLE
from app.front_test import page_left_right_asides
from app.front_test import RIGHT_ASIDE_EXAMPLE
from app.pages.report_page.report import get_example_report

log = logger_get(__name__)
register_page(__name__, path='/outputs/reports')
PAGE_ID = 'output-example-report-page'
layout = [html.Div(id=PAGE_ID, className='centered')]


@callback(Output(PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a output report using dmc_utils components.
    """
    PREVIOUS_BTN = dmc.Button('Previous', color='ecoact', size='lg')
    CONTINUE_BTN = dmc.Button('Continue', color='ecoact', size='lg')
    PAGE_TITLE = dmc.Title('Input Checks')
    page_content = dmc.Stack([
        dmc.Group([PREVIOUS_BTN, PAGE_TITLE, CONTINUE_BTN], justify='space-between'),
        dmc.ScrollArea([
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
        ], type='hover', style={'height': '85vh'}, scrollbarSize=8),
        dmc.Space(h=50)
    ])

    page = page_left_right_asides(
        left_aside=LEFT_ASIDE_EXAMPLE,
        right_aside=RIGHT_ASIDE_EXAMPLE,
        page_content=page_content,

    )
    return generic_page(token, page)
