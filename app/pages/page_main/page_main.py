"""
Module implementing the main page
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import FOOTER_ID
from ecodev_front import HEADER_ID
from ecodev_front import HREF
from ecodev_front import Page
from ecodev_front import PATHNAME
from ecodev_front import URL

from app.constants import MAIN_PAGE_URL
from app.pages.common import display_app_header
from app.pages.common import main_footer


PAGE_MAIN = Page(
    module=__name__,
    name='main',
    icon='raphael:home',
    title='Main Page',
    description='',
    layout=basic_layout,
)


@callback(Output(PAGE_MAIN.id, CHILDREN),
          Output(HEADER_ID, CHILDREN),
          Output(FOOTER_ID, CHILDREN),
          Input(URL, PATHNAME),
          Input(URL, HREF))
def get_main_page(url_pathname: str, href: str) -> tuple[list[dmc.Box], list[dmc.Box], list[dmc.Box]]:
    """
    Renders the main page.
    """
    if not url_pathname == MAIN_PAGE_URL:
        return [], [], []

    page = dmc.Stack([
        dmc.Text("""Hello World""", ta='center', fz=13, mb=10, fs='italic', c='green.4'),

    ])
    return page, display_app_header(), main_footer()
