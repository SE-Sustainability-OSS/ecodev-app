"""
Module implementing the module-1 page-1
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import Page
from ecodev_front import TOKEN

from app.pages.common.page_access import check_page_access


PAGE_COMPARISON = Page(
    module=__name__,
    name='comparison',
    icon='solar:graph-outline',
    title='Comparison',
    description='An example page of datasheet comparison',
    layout=basic_layout
)


@callback(Output(PAGE_COMPARISON.id, CHILDREN),
          Input(TOKEN, DATA),
          prevent_initial_call=True)
def render_page(token: dict):
    """
    Renders page component once token has been validated.
    """
    page = dmc.Stack(['Hello world!'], align='center', gap='xs')
    return check_page_access(token, page)
