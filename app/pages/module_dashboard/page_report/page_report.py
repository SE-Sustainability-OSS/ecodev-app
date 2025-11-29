"""
Module implementing the module-1 page-1
"""
import dash_mantine_components as dmc
from dash import callback
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
from app.db_model.retrievers.project_retrievers import retrieve_project_by_id
from app.pages.common.page_access import check_page_access

log = logger_get(__name__)


PAGE_REPORT = Page(
    module=__name__,
    name='reports',
    icon='dashicons:text-page',
    title='Project Report',
    description='An example page displaying a report',
    layout=header_layout
)


@callback(Output(PAGE_REPORT.id, CHILDREN),
          Output({TYPE: PROJECT_HEADER_ID, INDEX: PAGE_REPORT.id}, CHILDREN),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          prevent_initial_call=True)
def render_page(token: dict, project_id: int):
    """
    Renders page component once token has been validated.
    """
    with Session(engine) as session:
        project = retrieve_project_by_id(token, project_id, session)

    page = dmc.Stack(align='center', gap='xs')
    return (check_page_access(token, page),
            page_project_header(project.name, project.year) if project else None)
