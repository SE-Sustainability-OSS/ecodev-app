"""
Module implementing the project information page
"""
from functools import partial

import dash_mantine_components as dmc
from dash import ALL
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_front import BUTTON
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import ID
from ecodev_front import INDEX
from ecodev_front import N_CLICKS
from ecodev_front import Page
from ecodev_front import PATHNAME
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import URL
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.db_model.inserters import upsert_project
from app.db_model.retrievers import get_project_by_id
from app.pages.common.custom_callback import safe_callback
from app.pages.module_project.page_info import PROJECT_INFO_INPUT
from app.pages.module_project.page_info import PROJECT_INFO_SAVE
from app.pages.module_project.page_info.common.general_info import general_info_section
from app.pages.module_project.page_info.common.save_button import SAVE_INFO_BUTTON
from app.pages.module_project.page_rights.page_rights import PAGE_RIGHTS


PAGE_INFO = Page(
    module=__name__,
    name='information',
    icon='material-symbols:info-outline',
    title='Information',
    description='Edit basic and financial project information',
    layout=partial(header_layout, with_icon=False),
)


@safe_callback(Output(PAGE_INFO.id, CHILDREN),
               Input(TOKEN, DATA),
               Input(PROJECT_ID_STORE, DATA),
               check_access=False)
def render_project_info_page(token: dict, project_id: int) -> dmc.Stack:
    """
    Renders project information page.
    NOTE: Page access is granted by default, to allow for project creation
    (& no project ID is available during this step).
    """
    with Session(engine) as session:
        project = get_project_by_id(token, project_id, session)
        return dmc.Stack(
            children=[
                general_info_section(project),
                SAVE_INFO_BUTTON
            ], w='100%', gap='ls', align='center', mb=50)


@safe_callback(Output(PROJECT_ID_STORE, DATA, allow_duplicate=True),
               Output(URL, PATHNAME, allow_duplicate=True),
               State(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA),
               Input({TYPE: BUTTON, INDEX: PROJECT_INFO_SAVE}, N_CLICKS),
               State({TYPE: PROJECT_INFO_INPUT, INDEX: ALL}, VALUE),
               State({TYPE: PROJECT_INFO_INPUT, INDEX: ALL}, ID),
               check_access=False,
               prevent_initial_call=True)
def save_basic_info(token: dict,
                    project_id: int,
                    save_basic_info_btn: int,
                    info_values: list,
                    info_ids: list,
                    ) -> tuple[int, str]:
    """
    Callback which saves new or edited project information fields
    """
    if not save_basic_info_btn:
        raise PreventUpdate

    info_dict = {id[INDEX]: value for id, value in zip(info_ids, info_values)}
    with Session(engine) as session:
        project = upsert_project(token, project_id, info_dict, session)
        return project.id, PAGE_RIGHTS.url  # type: ignore[return-value]
