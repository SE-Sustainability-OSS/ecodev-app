"""
Module implementing the dashboard's module report page
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import INDEX
from ecodev_front import Page
from ecodev_front import page_project_header
from ecodev_front import PROJECT_HEADER_ID
from ecodev_front import TOKEN
from ecodev_front import TYPE
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.db_model.retrievers.project_retrievers import get_project_by_id
from app.pages.common.custom_callback import safe_callback
from app.pages.module_dashboard.common.aside import dashboard_aside_layout

log = logger_get(__name__)


PAGE_REPORT = Page(
    module=__name__,
    name='reports',
    icon='dashicons:text-page',
    title='Project Report',
    description='An example page displaying a report',
    layout=header_layout,
    aside=dashboard_aside_layout,
)


@safe_callback(Output(PAGE_REPORT.id, CHILDREN),
               Output({TYPE: PROJECT_HEADER_ID, INDEX: PAGE_REPORT.id}, CHILDREN),
               Input(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA))
def render_page(token: dict, project_id: int):
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    with Session(engine) as session:
        project = get_project_by_id(token, project_id, session)

    page = dmc.Stack(align='center', gap='xs')
    header = page_project_header(project.name, project.year) if project else None
    return page, header
