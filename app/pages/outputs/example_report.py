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
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.pages.outputs import REPORT_PAGE_ID
from app.pages.outputs import REPORT_PAGE_URL
from app.pages.outputs.report_page.report import get_example_report

log = logger_get(__name__)
register_page(__name__, path=REPORT_PAGE_URL)

layout = [html.Div(id=REPORT_PAGE_ID, className='centered')]


@callback(Output(REPORT_PAGE_ID, 'children'), Input(TOKEN, 'data'))
def render_page(token):
    """
    Example of a output report using dmc_utils components.
    """
    PREVIOUS_BTN = dmc.Button('Previous', color='ecoact', size='lg')
    CONTINUE_BTN = dmc.Button('Continue', color='ecoact', size='lg')
    PAGE_TITLE = dmc.Title('Report example')
    page = dmc.Stack([
        dmc.Group([PREVIOUS_BTN, PAGE_TITLE, CONTINUE_BTN], justify='space-between'),
        dmc.ScrollArea([dmc.Stack([
            dmc.Title('First Section', fz=18, c='gray'),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),

            dmc.Title('Second Section', fz=18, c='gray'),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
            dmc.Space(h=20),
            get_example_report(),
        ])], type='hover', style={'height': '85vh'}, scrollbarSize=8)
    ])

    return generic_page(token, page)
