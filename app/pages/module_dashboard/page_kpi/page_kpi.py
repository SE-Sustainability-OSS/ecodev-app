"""
Module implementing the module-2 page-2
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import Page
from ecodev_front import TOKEN

from app.pages.common.page_access import check_page_access


PAGE_KPI = Page(
    module=__name__,
    name='kpis',
    icon='solar:graph-outline',
    title='Project KPIs',
    description='An example page displaying KPIs',
    layout=header_layout,
    aside=lambda: 'hello world',
)


@callback(Output(PAGE_KPI.id, CHILDREN),
          Input(TOKEN, DATA),
          prevent_initial_call=True)
def render_page(token: dict):
    """
    Renders page component once token has been validated.
    """
    page = dmc.Stack(['Hello world !'], align='center', gap='xs')
    return check_page_access(token, page)
