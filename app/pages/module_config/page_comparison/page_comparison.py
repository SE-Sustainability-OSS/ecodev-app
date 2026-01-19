"""
Module implementing the module-1 page-1
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import Page
from ecodev_front import TOKEN

from app.constants import PROJECT_ID_STORE
from app.pages.common.custom_callback import safe_callback
from app.pages.common.custom_checks import verify_project_access


PAGE_COMPARISON = Page(
    module=__name__,
    name='comparison',
    icon='solar:graph-outline',
    title='Comparison',
    description='An example page of datasheet comparison',
    layout=basic_layout
)


@safe_callback(Output(PAGE_COMPARISON.id, CHILDREN),
               Input(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA),
               checks=[verify_project_access])
def render_page(token: dict, project_id: int):
    """
    Renders page's initial layout / content.
    """
    return dmc.Stack(['Hello world!'], align='center', gap='xs')
