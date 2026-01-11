"""
Module implementing the page to manage project and module access rights
"""
import dash_mantine_components as dmc
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import AppUser
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core import safe_get_user
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
from ecodev_front import NOTIFICATION
from ecodev_front import OPENED
from ecodev_front import Page
from ecodev_front import page_project_header
from ecodev_front import PROJECT_HEADER_ID
from ecodev_front import ROW_DATA
from ecodev_front import ROW_ID
from ecodev_front import send_notification
from ecodev_front import SEND_NOTIFICATIONS
from ecodev_front import TABLE
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import MODULE
from app.constants import PROJECT_ID_STORE
from app.constants import ROLE
from app.constants import USER_ID
from app.db_model.deleters import delete_project_access
from app.db_model.retrievers import get_project_by_id
from app.db_model.retrievers import get_user_by_id
from app.db_model.retrievers import verify_project_module_access
from app.domain_model import Role
from app.pages.common.custom_callback import safe_callback
from app.pages.common.stores import USER_DELETION_STORE
from app.pages.module_project.page_rights import ADD_PROJECT_RIGHTS_MODAL_CONFIRM
from app.pages.module_project.page_rights import ADD_PROJECT_USER_RIGHTS
from app.pages.module_project.page_rights import MANAGE_PROJECT_RIGHTS
from app.pages.module_project.page_rights import PROJECT_USERS
from app.pages.module_project.page_rights import REMOVE_PROJECT_USER_CANCEL
from app.pages.module_project.page_rights import REMOVE_PROJECT_USER_CONFIRM
from app.pages.module_project.page_rights import UPDATE_PROJECT_RIGHTS
from app.pages.module_project.page_rights.add_user_modal.add_user_modal import manage_rights_modal
from app.pages.module_project.page_rights.common.overview import manage_rights_overview
from app.pages.module_project.page_rights.methodo.grant_access import check_email_validity
from app.pages.module_project.page_rights.methodo.grant_access import get_new_project_users
from app.pages.module_project.page_rights.methodo.grant_access import grant_user_project_access
from app.pages.module_registry import get_registered_modules


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
def render_page(token: dict, project_id: int) -> tuple[dmc.Stack, dmc.Stack]:
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    with Session(engine) as session:
        project = get_project_by_id(token, project_id, session)
        all_modules = get_registered_modules()
        modules = verify_project_module_access(token, project_id, all_modules, session)
    page = manage_rights_overview(project_id, modules, session)
    header = page_project_header(project.name, project.year) if project else None
    return page, header


@safe_callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(NOTIFICATION, SEND_NOTIFICATIONS),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: UPDATE_PROJECT_RIGHTS}, N_CLICKS),
    State({TYPE: TABLE, INDEX: MANAGE_PROJECT_RIGHTS}, ROW_DATA),
    prevent_initial_call=True
)
def update_rights_callback(token: dict,
                           project_id: int,
                           n_clicks: int,
                           row_data: list[dict]) -> tuple[dict, list[dict]]:
    """
    Updates project access and module accesses for existing users based on table edits.
    Reads the role and module checkboxes from each row and updates the database accordingly.
    """
    if not n_clicks:
        raise PreventUpdate

    try:
        with Session(engine) as session:
            inviting_user = safe_get_user(token)

            for row in row_data:
                user = get_user_by_id(row[USER_ID], session)
                role = Role(row[ROLE]) if row[ROLE] else _assign_project_role(user)
                checked_modules = [module.name for module in get_registered_modules()
                                   if row.get(module.name, False)]
                grant_user_project_access(user, project_id, checked_modules,
                                          role, session, inviting_user)

        return token, send_notification('Success', 'Rights updated',
                                        autoClose=5000, with_close_button=True)
    except Exception as e:
        logger_get(__name__).error(f'Error updating rights: {e}')
        return token, send_notification('Failure', f'Error updating rights: {str(e)}',
                                        autoClose=False, with_close_button=True)


def _assign_project_role(user: AppUser, role: Role | None = None) -> Role:
    """
    Assigns a project role to a user.
    If no role is provided, the role is assigned based on the user's permission.
    """
    if not role:
        return Role.CLIENT if user.permission == Permission.Client else Role.COLLABORATOR
    return Role(role)


@safe_callback(
    Output({TYPE: MODAL, INDEX: ADD_PROJECT_USER_RIGHTS}, OPENED),
    Output({TYPE: MODAL, INDEX: ADD_PROJECT_USER_RIGHTS}, CHILDREN),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: ADD_PROJECT_USER_RIGHTS}, N_CLICKS)
)
def open_rights_modal(token: dict, project_id: int, n_clicks: int):
    """
    Opens the modal to add users and set their rights.
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        user = safe_get_user(token)
        all_modules = get_registered_modules()
        modules = verify_project_module_access(token, project_id, all_modules, session)
        return True, manage_rights_modal(user, modules, session)


@safe_callback(Output(TOKEN, DATA, allow_duplicate=True),
               Output({TYPE: MODAL, INDEX: ADD_PROJECT_USER_RIGHTS}, OPENED, allow_duplicate=True),
               Output(NOTIFICATION, SEND_NOTIFICATIONS, allow_duplicate=True),
               Output({TYPE: MULTI_SELECT, INDEX: PROJECT_USERS}, ERROR),
               State(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA),
               Input({TYPE: BUTTON, INDEX: ADD_PROJECT_RIGHTS_MODAL_CONFIRM}, N_CLICKS),
               State({TYPE: MULTI_SELECT, INDEX: PROJECT_USERS}, VALUE),
               State({TYPE: MULTI_SELECT, INDEX: MODULE}, VALUE),
               prevent_initial_call=True,
               running=[(Output({TYPE: BUTTON, INDEX: ADD_PROJECT_RIGHTS_MODAL_CONFIRM}, LOADING), True, False)])
def add_rights(token: dict,
               project_id: int,
               n_clicks: int,
               emails: list[str],
               modules: list[str],
               ) -> tuple[dict, bool, list[dict], str]:
    """
    Adds users to a project and sets their rights.

    For existing users: Adds them to the project with specified modules.
    For new users: Creates them in AppUser/AppRight tables with app-wide license rights
    restricted to the inviting user's modules, then adds them to the project.

    NOTE: If Role is set to None, it will be auto-assigned: first user becomes OWNER, subsequent users
    become COLLABORATOR or CLIENT.
    """
    if not n_clicks:
        raise PreventUpdate

    if not emails:
        no_email_notif = send_notification('Failure', 'Please enter at least one user',
                                           autoClose=False, with_close_button=True)
        select_error_msg = 'Please enter at least one user'
        return no_update, True, no_email_notif, select_error_msg

    inviting_user = safe_get_user(token)
    if invalid_emails := check_email_validity(emails):
        invalid_emails_notif = send_notification('Invalid emails:', invalid_emails,
                                                 autoClose=False, with_close_button=True)
        select_error_msg = 'Please enter a valid email address'
        return no_update, True, invalid_emails_notif, select_error_msg

    try:
        with Session(engine) as session:
            for user in get_new_project_users(inviting_user, emails, session):
                grant_user_project_access(user, project_id, modules, None, session, inviting_user)

        success_notif = send_notification('Success', 'Users added successfully',
                                          autoClose=2000, with_close_button=True)
        return token, False, success_notif, no_update
    except Exception as e:
        error_notif = send_notification('Failure', f'Error adding users: {str(e)}',
                                        autoClose=False, with_close_button=True)
        return no_update, True, error_notif, no_update


@safe_callback(
    Output({TYPE: MODAL, INDEX: REMOVE_PROJECT_USER_CONFIRM}, OPENED),
    Output(USER_DELETION_STORE, DATA, allow_duplicate=True),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: TABLE, INDEX: MANAGE_PROJECT_RIGHTS}, CELL_RENDERER_DATA),
    State({TYPE: TABLE, INDEX: MANAGE_PROJECT_RIGHTS}, ROW_DATA),
    prevent_initial_call=True,
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
    Output({TYPE: MODAL, INDEX: REMOVE_PROJECT_USER_CONFIRM}, OPENED, allow_duplicate=True),
    Output(TOKEN, DATA, allow_duplicate=True),
    State(TOKEN, DATA),
    State(PROJECT_ID_STORE, DATA),
    Input({TYPE: BUTTON, INDEX: REMOVE_PROJECT_USER_CONFIRM}, N_CLICKS),
    Input({TYPE: BUTTON, INDEX: REMOVE_PROJECT_USER_CANCEL}, N_CLICKS),
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
