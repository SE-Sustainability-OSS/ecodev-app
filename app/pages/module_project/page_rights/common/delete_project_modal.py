"""
File containing project deletion confirmation modal.
Requires the user to confirm by entering the name of the project to delete.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from ecodev_core import engine
from ecodev_front import BUTTON
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import INDEX
from ecodev_front import LOADING
from ecodev_front import MODAL
from ecodev_front import N_CLICKS
from ecodev_front import OPENED
from ecodev_front import PATHNAME
from ecodev_front import TEXT_INPUT
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import URL
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import MAIN_PAGE_URL
from app.constants import PROJECT_ID_STORE
from app.db_model import Project
from app.db_model.deleters import delete_project
from app.db_model.retrievers import get_project_by_id
from app.pages.module_project.page_rights import DELETE_PROJECT
from app.pages.module_project.page_rights import DELETE_PROJECT_CONFIRM
from app.pages.module_project.page_rights import DELETE_PROJECT_CONFIRMATION
from app.pages.module_project.page_rights import PROJECT_NAME


DELETE_CONFIRMATION_MODAL = dmc.Modal(
    id={TYPE: MODAL, INDEX: DELETE_PROJECT_CONFIRMATION},
    title='Confirm project deletion',
    size='lg',
)


def delete_project_modal_content(project: Project) -> dmc.Stack:
    """
    Renders the project delete confirmation modal
    """
    return dmc.Stack([
        dmc.Text("""You are about to delete this entire project and any
                    associated assets, KPIs, dashboard and reporting.""",
                 fw=900, c='red'),
        dmc.Text("""Please confirm by entering the project's name:""", c='red'),
        dmc.Text(f'{project.name}', fw=800, c='red', ta='center'),
        dmc.TextInput(
            id={TYPE: TEXT_INPUT, INDEX: PROJECT_NAME},
            placeholder='Project name'
        ),
        dmc.Button(
            'Delete this project',
            id={TYPE: BUTTON, INDEX: DELETE_PROJECT_CONFIRM},
            leftSection=DashIconify(icon='solar:trash-bin-trash-outline', width=24),
            size='md',
            radius='md',
            color='red',
        )
    ])


@callback(Output({TYPE: MODAL, INDEX: DELETE_PROJECT_CONFIRMATION}, OPENED),
          Output({TYPE: MODAL, INDEX: DELETE_PROJECT_CONFIRMATION}, CHILDREN),
          Input({TYPE: BUTTON, INDEX: DELETE_PROJECT}, N_CLICKS),
          State(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA))
def open_delete_confirmation_modal(n_click: int,
                                   token: dict,
                                   project_id: int
                                   ) -> tuple[bool, dmc.Stack]:
    """
    Method opening a model to possibly delete a project
    """
    if not n_click:
        raise PreventUpdate

    with Session(engine) as session:
        if not (project := get_project_by_id(token, project_id, session)):
            raise PreventUpdate

    return True, delete_project_modal_content(project)


@callback(Output(URL, PATHNAME, allow_duplicate=True),
          Input({TYPE: BUTTON, INDEX: DELETE_PROJECT_CONFIRM}, N_CLICKS),
          State({TYPE: TEXT_INPUT, INDEX: PROJECT_NAME}, VALUE),
          State(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          running=((Output({TYPE: BUTTON, INDEX: DELETE_PROJECT_CONFIRM}, LOADING), True, False)),
          prevent_initial_call=True)
def delete_project_confirmed(n_click: int,
                             confirmation_val: str,
                             token: dict,
                             project_id: int
                             ) -> str:
    """
    Method to confirm the deletion of a project
    """
    if not n_click:
        raise PreventUpdate

    with Session(engine) as session:
        if (project := get_project_by_id(token, project_id, session)) and \
                confirmation_val == project.name:
            delete_project(token, project, session)  # type: ignore[arg-type]
            return MAIN_PAGE_URL
    raise PreventUpdate
