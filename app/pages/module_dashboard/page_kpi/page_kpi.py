"""
Module implementing the module-2 page-2
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import Page
from ecodev_front import TOKEN

from app.constants import PROJECT_ID_STORE
from app.pages.common.custom_callback import safe_callback
from app.pages.module_dashboard.common.aside import dashboard_aside_layout


PAGE_KPI = Page(
    module=__name__,
    name='kpis',
    icon='solar:graph-outline',
    title='Project KPIs',
    description='An example page displaying KPIs',
    layout=header_layout,
    aside=dashboard_aside_layout,
)


@safe_callback(Output(PAGE_KPI.id, CHILDREN),
               Input(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA))
def render_page(token: dict, project_id: int):
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    return dmc.Stack(['Hello world !'], align='center', gap='xs')
