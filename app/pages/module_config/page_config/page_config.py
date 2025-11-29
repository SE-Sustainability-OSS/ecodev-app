"""
Module implementing the module-1 page-1
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash import State
from ecodev_core import engine
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

PAGE_CONFIG = Page(
    module=__name__,
    name='configuration',
    icon='dashicons:text-page',
    title='Configuration',
    description='Configuration of the first page of module 1',
    layout=header_layout
)


@callback(Output(PAGE_CONFIG.id, CHILDREN),
          Output({TYPE: PROJECT_HEADER_ID, INDEX: PAGE_CONFIG.id}, CHILDREN),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          prevent_initial_call=True)
def render_page(token: dict, project_id: int):
    """
    Renders page component once token has been validated.
    """
    with Session(engine) as session:
        project = retrieve_project_by_id(token, project_id, session)

    project_header = page_project_header(project.name, project.year) if project else None

    page = dmc.Stack(align='center', gap='xs')

    return page, project_header
