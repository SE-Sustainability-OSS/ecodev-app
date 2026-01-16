"""
Module implementing the 403 page forbidden.
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


PAGE_403 = Page(
    module=__name__,
    name='403',
    icon='solar:forbidden-circle-linear',
    title='Forbidden Access',
    description='',
    layout=basic_layout,
)


@callback(Output(PAGE_403.id, CHILDREN),
          Input(TOKEN, DATA))
def render_403_page(token: dict) -> dmc.Stack:
    """
    Renders 403 page.
    """
    page = dmc.Stack([
        section_title('Forbidden.', fz=28, mb=20),
        subtext("""You do not have access to this page or module.
                   Please return to the home page.""")
    ], align='center', gap='xs')
    return page
