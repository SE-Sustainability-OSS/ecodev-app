"""
Module implementing the page to manage project and module access rights

NB: All internal roles have access to all modules by default.
"""
import dash_mantine_components as dmc
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core import safe_get_user
from ecodev_front import ALERT
from ecodev_front import BUTTON
from ecodev_front import CELL_RENDERER_DATA
from ecodev_front import CHILDREN
from ecodev_front import COL_ID
from ecodev_front import DATA
from ecodev_front import ERROR
from ecodev_front import header_layout
from ecodev_front import INDEX
from ecodev_front import LOADING
from ecodev_front import MODAL
from ecodev_front import MULTI_SELECT
from ecodev_front import N_CLICKS
from ecodev_front import OPENED
from ecodev_front import Page
from ecodev_front import page_project_header
from ecodev_front import PROJECT_HEADER_ID
from ecodev_front import ROW_DATA
from ecodev_front import ROW_ID
from ecodev_front import TABLE
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import MODULE
from app.constants import PROJECT_ID_STORE
from app.constants import USER_ID
from app.db_model.inserters.project_access_inserters import delete_project_access
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.retrievers.access_retrievers import get_app_rights
from app.db_model.retrievers.access_retrievers import verify_project_module_access
from app.db_model.retrievers.app_user_retrievers import get_user_by_id
from app.db_model.retrievers.project_retrievers import get_project_by_id
from app.domain_model import AppModule
from app.domain_model import ProjectAccessData
from app.domain_model import Role
from app.pages.common.custom_callback import safe_callback
from app.pages.common.stores import USER_DELETION_STORE
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_CONFIRM
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_ERROR
from app.pages.module_project.page_rights import ADD_USER_RIGHTS
from app.pages.module_project.page_rights import MANAGE_RIGHTS
from app.pages.module_project.page_rights import REMOVE_USER_CANCEL
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRM
from app.pages.module_project.page_rights import UPDATE_RIGHTS
from app.pages.module_project.page_rights import USERS
from app.pages.module_project.page_rights.add_user_modal.add_user_modal import manage_rights_modal
from app.pages.module_project.page_rights.common.overview import manage_rights_overview
from app.pages.module_project.page_rights.methodo.grant_access import check_email_validity
from app.pages.module_project.page_rights.methodo.grant_access import get_new_project_users
from app.pages.module_project.page_rights.methodo.grant_access import grant_user_project_access


log = logger_get(__name__)

PAGE_RIGHTS = Page(
    module=__name__,
    name='rights',
    icon='hugeicons:access',
    title='Manage Portfolio',
    description='Add & remove users. Delete project.',
    admin=True,
    layout=header_layout
)


@safe_callback(Output(PAGE_RIGHTS.id, CHILDREN),
               Output({TYPE: PROJECT_HEADER_ID, INDEX: PAGE_RIGHTS.id}, CHILDREN),
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
        user_modules = get_app_rights(safe_get_user(token), session)
        modules = verify_project_module_access(token, project_id, user_modules, session)
    page = manage_rights_overview(project_id, modules, session)
    header = page_project_header(project.name, project.year) if project else None
    return page, header


@safe_callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output({TYPE: ALERT, INDEX: MANAGE_RIGHTS}, CHILDREN),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: UPDATE_RIGHTS}, N_CLICKS),
    State({TYPE: TABLE, INDEX: MANAGE_RIGHTS}, ROW_DATA),
    prevent_initial_call=True
)
def update_rights_callback(token: dict,
                           project_id: int,
                           n_clicks: int,
                           row_data: list[dict]) -> tuple[dict, dmc.Alert]:
    """
    Upserts both the project access and module accesses
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        for row in row_data:
            user = get_user_by_id(row[USER_ID], session)
            user_modules = get_app_rights(user, session)
            modules = verify_project_module_access(user, project_id, user_modules, session)
            access_data = ProjectAccessData(
                user_id=user.id,
                role=Role.CLIENT if user.permission == Permission.Client else Role.COLLABORATOR,
                project_id=project_id,
                module_access={module: bool(module in modules) for module in AppModule}
            )
            upsert_project_access(project_id, access_data, session)

    return token, dmc.Alert('Rights updated', title='Success', color='green')


@safe_callback(
    Output({TYPE: MODAL, INDEX: ADD_USER_RIGHTS}, OPENED),
    Output({TYPE: MODAL, INDEX: ADD_USER_RIGHTS}, CHILDREN),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: ADD_USER_RIGHTS}, N_CLICKS)
)
def open_rights_modal(token: dict, project_id: int, n_clicks: int):
    """
    Opens the modal to add users and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        user = safe_get_user(token)
        user_modules = get_app_rights(safe_get_user(token), session)
        modules = verify_project_module_access(token, project_id, user_modules, session)
        return True, manage_rights_modal(user, modules, session)


@safe_callback(Output(TOKEN, DATA),
               Output({TYPE: MODAL, INDEX: ADD_USER_RIGHTS}, OPENED, allow_duplicate=True),
               Output({TYPE: ALERT, INDEX: ADD_RIGHTS_MODAL_ERROR}, CHILDREN),
               Output({TYPE: MULTI_SELECT, INDEX: USERS}, ERROR),
               State(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA),
               Input({TYPE: BUTTON, INDEX: ADD_RIGHTS_MODAL_CONFIRM}, N_CLICKS),
               State({TYPE: MULTI_SELECT, INDEX: USERS}, VALUE),
               State({TYPE: MULTI_SELECT, INDEX: MODULE}, VALUE),
               prevent_initial_call=True,
               running=[(Output({TYPE: BUTTON, INDEX: ADD_RIGHTS_MODAL_CONFIRM}, LOADING), True, False)])
def add_rights(token: dict,
               project_id: int,
               n_clicks: int,
               emails: list[str],
               modules: list[str],
               ) -> tuple[dict, bool, str, str]:
    """
    Callback used to add (in batch) users to a project, and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    if not emails:
        return no_update, True, no_update, 'Please enter at least one user'

    user = safe_get_user(token)
    if invalid_emails := check_email_validity(emails):
        return no_update, True, invalid_emails, no_update

    with Session(engine) as session:
        for new_user in get_new_project_users(user, emails, session):
            role = Role.CLIENT if user.permission == Permission.Client else Role.COLLABORATOR
            grant_user_project_access(new_user, project_id, modules, role, session)

    return token, False, no_update, no_update


@safe_callback(
    Output({TYPE: MODAL, INDEX: REMOVE_USER_CONFIRM}, OPENED),
    Output(USER_DELETION_STORE, DATA),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: TABLE, INDEX: MANAGE_RIGHTS}, CELL_RENDERER_DATA),
    State({TYPE: TABLE, INDEX: MANAGE_RIGHTS}, ROW_DATA),
)
def open_remove_confirmation_modal(token: dict,
                                   project_id: int,
                                   button_click: dict,
                                   row_data: list[dict]
                                   ) -> tuple[bool, dict]:
    """
    Opens the removal confirmation modal for a user and stores the infos linked to the user in a
    store
    """
    if button_click and button_click[COL_ID] == 'Remove':
        return True, row_data[int(button_click[ROW_ID])]
    raise PreventUpdate


@safe_callback(
    Output({TYPE: MODAL, INDEX: REMOVE_USER_CONFIRM}, OPENED, allow_duplicate=True),
    Output(TOKEN, DATA, allow_duplicate=True),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: REMOVE_USER_CONFIRM}, N_CLICKS),
    Input({TYPE: BUTTON, INDEX: REMOVE_USER_CANCEL}, N_CLICKS),
    State(USER_DELETION_STORE, DATA),
    prevent_initial_call=True
)
def remove_consultant(token: dict,
                      project_id: int,
                      confirm_button: int,
                      cancel_button: int,
                      user_data: dict,
                      ) -> tuple[bool, dict]:
    """
    Callback to edit a project, populating the main fields with the selected project info
    """
    if not confirm_button and not cancel_button:
        raise PreventUpdate

    if confirm_button:
        with Session(engine) as session:
            user = get_user_by_id(user_data[USER_ID], session)
            delete_project_access(user, project_id, session)

    return False, token
