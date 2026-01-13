"""
Module implementing the 404 page not found.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import Page
from ecodev_front import section_title
from ecodev_front import subtext
from ecodev_front import TOKEN


PAGE_404 = Page(
    module=__name__,
    name='404',
    icon='iconoir:file-not-found',
    title='Page Not Found',
    description='',
    layout=basic_layout,
)


@callback(Output(PAGE_404.id, CHILDREN),
          Input(TOKEN, DATA))
def render_404_page(token: dict) -> dmc.Stack:
    """
    Renders 404 page.
    """
    page = dmc.Stack([
        section_title('Page not found.', fz=28, mb=20),
        subtext("""If you think there is an issue with the app.
                 Please report it using the link in the footer.""")
    ], align='center', gap='xs')
    return page
