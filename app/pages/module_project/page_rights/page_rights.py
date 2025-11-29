"""
Module implementing the page to manage project and module access rights

NB: All internal roles have access to all modules by default.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_core import logger_get
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

from app.constants import PROJECT_ID
from app.constants import PROJECT_ID_STORE
from app.constants import USER_ID
from app.db_model.inserters.project_access_inserters import delete_project_access
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.retrievers.access_retrievers import get_accessible_modules
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_id
from app.db_model.retrievers.project_retrievers import retrieve_project_by_id
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
from app.pages.module_project.page_rights.methodo.grant_access import MODULES

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


@callback(Output(PAGE_RIGHTS.id, CHILDREN),
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
        modules = get_accessible_modules(token, MODULES, session)
    page = manage_rights_overview(project_id, modules, session)
    return (check_page_access(token, page),
            page_project_header(project.name, project.description) if project else None)


@callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(UPDATE_RIGHTS_ALERT_ID, CHILDREN),
    State(TOKEN, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: UPDATE_BTN}, N_CLICKS),
    State({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, ROW_DATA),
    State(PROJECT_ID_STORE, DATA),
    prevent_initial_call=True
)
def update_rights_callback(token: dict,
                           n_clicks: int,
                           row_data: list[dict],
                           project_id: int):
    """
    Upserts both the project access and module accesses
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        for row in row_data:
            user = retrieve_user_by_id(row[USER_ID], session)
            modules = get_accessible_modules(user, MODULES, session)
            upsert_project_access(project_id, row, modules, session)

    return token, dmc.Alert('Rights updated', title='Success', color='green')


@callback(
    Output(ADD_RIGHTS_MODAL_ID, OPENED),
    Output(ADD_RIGHTS_MODAL_ID, CHILDREN),
    State(TOKEN, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: ADD_BTN}, N_CLICKS)
)
def open_rights_modal(token: dict, n_clicks: int):
    """
    Opens the modal to add users and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        user = safe_get_user(token)
        modules = get_accessible_modules(token, MODULES, session)
        return True, manage_rights_modal(user, modules, session)


@callback(Output(TOKEN, DATA),
          Output(ADD_RIGHTS_MODAL_ID, OPENED, allow_duplicate=True),
          Output(ADD_RIGHTS_MODAL_ERROR_ID, CHILDREN),
          Output(USERS_MULTISELECT_ID, ERROR),
          Input(ADD_RIGHTS_MODAL_CONFIRM_BTN_ID, N_CLICKS),
          State(USERS_MULTISELECT_ID, VALUE),
          State(MODULE_MULTISELECT_ID, VALUE),
          State(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          prevent_initial_call=True,
          running=[(Output(ADD_RIGHTS_MODAL_CONFIRM_BTN_ID, LOADING), True, False)]
          )
def add_rights(n_clicks: int,
               emails: list[str],
               modules: list[str],
               token: dict,
               project_id: int):
    """
    Callback used to add (in batch) users to a project, and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    if not emails:
        return no_update, True, no_update, 'Please enter at least one user'

    user = safe_get_user(token)
    if invalid_emails := check_email_validity(emails, user):
        return no_update, True, invalid_emails, no_update

    with Session(engine) as session:
        for new_user in get_new_project_users(user, emails, session):
            grant_user_project_access(new_user, project_id, modules, session)

    return token, False, no_update, no_update


@callback(
    Output(REMOVE_USER_CONFIRMATION_MODAL_ID, OPENED),
    Output(USER_DELETION_STORE, DATA),
    Input({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, CELL_RENDERER_DATA),
    State({TYPE: MANAGE_RIGHTS, INDEX: TABLE}, ROW_DATA),
)
def open_remove_confirmation_modal(button_click: dict, row_data: list[dict]):
    """
    Opens the removal confirmation modal for a user and stores the infos linked to the user in a
    store
    """
    if button_click and button_click[COL_ID] == 'Remove':
        return True, row_data[int(button_click[ROW_ID])]
    raise PreventUpdate


@callback(
    Output(REMOVE_USER_CONFIRMATION_MODAL_ID, OPENED, allow_duplicate=True),
    Output(TOKEN, DATA, allow_duplicate=True),
    Input(REMOVE_USER_CONFIRMATION_BUTTON_ID, N_CLICKS),
    Input(REMOVE_USER_CANCELLATION_BUTTON_ID, N_CLICKS),
    State(USER_DELETION_STORE, DATA),
    State(TOKEN, DATA),
    prevent_initial_call=True
)
def remove_consultant(confirm_button: int,
                      cancel_button: int,
                      user_data: dict,
                      token: dict):
    """
    Callback to edit a project, populating the main fields with the selected project info
    """
    if not confirm_button and not cancel_button:
        raise PreventUpdate

    if confirm_button:
        with Session(engine) as session:
            delete_project_access(user_data[USER_ID], user_data[PROJECT_ID], session)

    return False, token
