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
from ecodev_front import CELL_RENDERER_DATA
from ecodev_front import CHILDREN
from ecodev_front import COL_ID
from ecodev_front import DATA
from ecodev_front import ERROR
from ecodev_front import header_layout
from ecodev_front import INDEX
from ecodev_front import LOADING
from ecodev_front import N_CLICKS
from ecodev_front import OPENED
from ecodev_front import Page
from ecodev_front import page_project_header
from ecodev_front import PROJECT_HEADER_ID
from ecodev_front import ROW_DATA
from ecodev_front import ROW_ID
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.constants import USER_ID
from app.db_model.inserters.project_access_inserters import delete_project_access
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.retrievers.access_retrievers import get_project_accessible_modules
from app.db_model.retrievers.access_retrievers import retrieve_license_rights
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_id
from app.db_model.retrievers.project_retrievers import retrieve_project_by_id
from app.domain_model import ALL_MODULE_NAMES
from app.domain_model import ProjectAccessData
from app.domain_model import Role
from app.pages.common.custom_callback import safe_callback
from app.pages.common.page_access import check_page_access
from app.pages.common.stores import USER_DELETION_STORE
from app.pages.module_project.page_rights import ADD_BTN
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_CONFIRM_BTN_ID
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_ERROR_ID
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_ID
from app.pages.module_project.page_rights import MANAGE_RIGHTS
from app.pages.module_project.page_rights import MODULE_MULTISELECT_ID
from app.pages.module_project.page_rights import REMOVE_USER_CANCELLATION_BUTTON_ID
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRMATION_BUTTON_ID
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRMATION_MODAL_ID
from app.pages.module_project.page_rights import TABLE
from app.pages.module_project.page_rights import UPDATE_BTN
from app.pages.module_project.page_rights import UPDATE_RIGHTS_ALERT_ID
from app.pages.module_project.page_rights import USERS_MULTISELECT_ID
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
               State(PROJECT_ID_STORE, DATA),
               prevent_initial_call=True)
def render_page(token: dict, project_id: int):
    """
    Renders page component once token has been validated.
    """
    with Session(engine) as session:
        project = retrieve_project_by_id(token, project_id, session)
        user_modules = retrieve_license_rights(safe_get_user(token), session)
        modules = get_project_accessible_modules(token, project_id, user_modules, session)
    page = manage_rights_overview(project_id, modules, session)
    return (check_page_access(token, page),
            page_project_header(project.name, project.description) if project else None)


@safe_callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(UPDATE_RIGHTS_ALERT_ID, CHILDREN),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: UPDATE_BTN}, N_CLICKS),
    State({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, ROW_DATA),
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
            user = retrieve_user_by_id(row[USER_ID], session)
            user_modules = retrieve_license_rights(user, session)
            modules = get_project_accessible_modules(user, project_id, user_modules, session)
            access_data = ProjectAccessData(
                user_id=user.id,
                role=Role.CLIENT if user.permission == Permission.CLIENT else Role.COLLABORATOR,
                project_id=project_id,
                module_access={module: bool(module in modules) for module in ALL_MODULE_NAMES}
            )
            upsert_project_access(project_id, access_data, session)

    return token, dmc.Alert('Rights updated', title='Success', color='green')


@safe_callback(
    Output(ADD_RIGHTS_MODAL_ID, OPENED),
    Output(ADD_RIGHTS_MODAL_ID, CHILDREN),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: ADD_BTN}, N_CLICKS)
)
def open_rights_modal(token: dict, project_id: int, n_clicks: int):
    """
    Opens the modal to add users and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        user = safe_get_user(token)
        user_modules = retrieve_license_rights(safe_get_user(token), session)
        modules = get_project_accessible_modules(token, project_id, user_modules, session)
        return True, manage_rights_modal(user, modules, session)


@safe_callback(Output(TOKEN, DATA),
               Output(ADD_RIGHTS_MODAL_ID, OPENED, allow_duplicate=True),
               Output(ADD_RIGHTS_MODAL_ERROR_ID, CHILDREN),
               Output(USERS_MULTISELECT_ID, ERROR),
               State(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA),
               Input(ADD_RIGHTS_MODAL_CONFIRM_BTN_ID, N_CLICKS),
               State(USERS_MULTISELECT_ID, VALUE),
               State(MODULE_MULTISELECT_ID, VALUE),
               prevent_initial_call=True,
               running=[(Output(ADD_RIGHTS_MODAL_CONFIRM_BTN_ID, LOADING), True, False)])
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
            grant_user_project_access(new_user, project_id, modules, session)

    return token, False, no_update, no_update


@safe_callback(
    Output(REMOVE_USER_CONFIRMATION_MODAL_ID, OPENED),
    Output(USER_DELETION_STORE, DATA),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, CELL_RENDERER_DATA),
    State({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, ROW_DATA),
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
    Output(REMOVE_USER_CONFIRMATION_MODAL_ID, OPENED, allow_duplicate=True),
    Output(TOKEN, DATA, allow_duplicate=True),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input(REMOVE_USER_CONFIRMATION_BUTTON_ID, N_CLICKS),
    Input(REMOVE_USER_CANCELLATION_BUTTON_ID, N_CLICKS),
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
            delete_project_access(user_data[USER_ID], project_id, session)

    return False, token
