"""
Module implementing the page to manage app users and their AppRight module access.
NOTE: This page is only accessible to admin users.
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
from ecodev_front import PROJECT_HEADER_ID
from ecodev_front import ROW_DATA
from ecodev_front import ROW_ID
from ecodev_front import SELECT
from ecodev_front import send_notification
from ecodev_front import SEND_NOTIFICATIONS
from ecodev_front import TABLE
from ecodev_front import TEXT_INPUT
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import VALUE
from sqlmodel import Session

from app.constants import MODULE
from app.constants import USER_ID
from app.db_model.deleters import delete_user
from app.db_model.retrievers import get_user_by_email
from app.db_model.retrievers import get_user_by_id
from app.pages.common.custom_callback import safe_callback
from app.pages.common.stores import USER_DELETION_STORE
from app.pages.pages_account.page_manage_user import ADD_USER
from app.pages.pages_account.page_manage_user import ADD_USER_MODAL_CONFIRM
from app.pages.pages_account.page_manage_user import MANAGE_USERS
from app.pages.pages_account.page_manage_user import REMOVE_USER_CANCEL
from app.pages.pages_account.page_manage_user import REMOVE_USER_CONFIRM
from app.pages.pages_account.page_manage_user import UPDATE_USERS
from app.pages.pages_account.page_manage_user import USER_CLIENT
from app.pages.pages_account.page_manage_user import USER_EMAIL
from app.pages.pages_account.page_manage_user import USER_PERMISSION
from app.pages.pages_account.page_manage_user.add_user_modal.add_user_modal import manage_users_modal
from app.pages.pages_account.page_manage_user.common.buttons import manage_users_button
from app.pages.pages_account.page_manage_user.common.overview import manage_users_overview
from app.pages.pages_account.page_manage_user.common.table import PERMISSION
from app.pages.pages_account.page_manage_user.methodo.grant_app_rights import check_email_validity
from app.pages.pages_account.page_manage_user.methodo.grant_app_rights import grant_user_app_rights
from app.pages.registry import get_modules


log = logger_get(__name__)

PAGE_MANAGE_USERS = Page(
    module=__name__,
    name='manage-users',
    icon='mdi:user-add-outline',
    title='Manage Users',
    description='Add & remove users. Set app-wide module access.',
    admin=True,
    layout=header_layout,
)


@safe_callback(Output(PAGE_MANAGE_USERS.id, CHILDREN),
               Output({TYPE: PROJECT_HEADER_ID, INDEX: PAGE_MANAGE_USERS.id}, CHILDREN),
               Input(TOKEN, DATA),
               check_access=False)
def render_page(token: dict) -> dmc.Stack:
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator (admin=True in Page definition).
    """
    user = safe_get_user(token)
    if not user.permission == Permission.ADMIN:
        raise PreventUpdate

    with Session(engine) as session:
        page = dmc.Stack([
            manage_users_overview(session)
        ], w='100%', align='center', justify='center', mt=10)
        header = manage_users_button()
        return page, header


@safe_callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(NOTIFICATION, SEND_NOTIFICATIONS, allow_duplicate=True),
    State(TOKEN, DATA),
    Input({TYPE: BUTTON, INDEX: UPDATE_USERS}, N_CLICKS),
    State({TYPE: TABLE, INDEX: MANAGE_USERS}, ROW_DATA),
    prevent_initial_call=True,
    check_access=False
)
def update_users_callback(token: dict,
                          n_clicks: int,
                          row_data: list[dict]) -> tuple[dict, list[dict]]:
    """
    Updates app-wide user access rights based on table edits.
    Reads the module checkboxes from each row and updates the AppRight table accordingly.
    """
    if not n_clicks:
        raise PreventUpdate

    try:
        with Session(engine) as session:
            for row in row_data:
                user = get_user_by_id(row[USER_ID], session)
                permission = Permission(row[PERMISSION])
                checked_modules = [module.name for module in get_modules()
                                   if row.get(module.name, False)]
                grant_user_app_rights(user, checked_modules, session, permission)

        return token, send_notification('Success', 'User rights updated',
                                        autoClose=5000, with_close_button=True)
    except Exception as e:
        logger_get(__name__).error(f'Error updating user rights: {e}')
        return token, send_notification('Failure', f'Error updating user rights: {str(e)}',
                                        autoClose=False, with_close_button=True)


@safe_callback(
    Output({TYPE: MODAL, INDEX: ADD_USER}, OPENED),
    Output({TYPE: MODAL, INDEX: ADD_USER}, CHILDREN),
    State(TOKEN, DATA),
    Input({TYPE: BUTTON, INDEX: ADD_USER}, N_CLICKS),
    check_access=False
)
def open_add_user_modal(token: dict, n_clicks: int):
    """
    Opens the modal to add users and set their app-wide rights.
    """
    if not n_clicks:
        raise PreventUpdate

    with Session(engine) as session:
        all_modules = get_modules()
        return True, manage_users_modal(all_modules, session)


@safe_callback(Output(TOKEN, DATA, allow_duplicate=True),
               Output({TYPE: MODAL, INDEX: ADD_USER}, OPENED, allow_duplicate=True),
               Output(NOTIFICATION, SEND_NOTIFICATIONS, allow_duplicate=True),
               Output({TYPE: TEXT_INPUT, INDEX: USER_EMAIL}, ERROR),
               State(TOKEN, DATA),
               Input({TYPE: BUTTON, INDEX: ADD_USER_MODAL_CONFIRM}, N_CLICKS),
               State({TYPE: TEXT_INPUT, INDEX: USER_EMAIL}, VALUE),
               State({TYPE: SELECT, INDEX: USER_PERMISSION}, VALUE),
               State({TYPE: MULTI_SELECT, INDEX: USER_CLIENT}, VALUE),
               State({TYPE: MULTI_SELECT, INDEX: MODULE}, VALUE),
               prevent_initial_call=True,
               check_access=False,
               running=[(Output({TYPE: BUTTON, INDEX: ADD_USER_MODAL_CONFIRM}, LOADING), True, False)])
def add_user(token: dict,
             n_clicks: int,
             email: str,
             permission: str,
             client_list: list[str],
             modules: list[str],
             ) -> tuple[dict, bool, list[dict], str]:
    """
    Adds a user to the app and sets their AppRight module access.

    For existing users: Updates their AppRight entries with specified modules.
    For new users: Creates them in AppUser/AppRight tables with specified module rights and permission.
    """
    if not n_clicks:
        raise PreventUpdate

    if not email:
        no_email_notif = send_notification('Failure', 'Please enter a user email',
                                           autoClose=False, with_close_button=True)
        select_error_msg = 'Please enter a user email'
        return no_update, True, no_email_notif, select_error_msg

    if invalid_emails := check_email_validity([email]):
        invalid_emails_notif = send_notification('Invalid email:', invalid_emails,
                                                 autoClose=False, with_close_button=True)
        select_error_msg = 'Please enter a valid email address'
        return no_update, True, invalid_emails_notif, select_error_msg

    if not permission:
        no_permission_notif = send_notification('Failure', 'Please select a permission level',
                                                autoClose=False, with_close_button=True)
        return no_update, True, no_permission_notif, ''

    if not client_list or len(client_list) == 0:
        no_client_notif = send_notification('Failure', 'Please enter a client organization',
                                            autoClose=False, with_close_button=True)
        return no_update, True, no_client_notif, ''

    client = client_list[0]

    try:
        with Session(engine) as session:
            user = get_user_by_email(email, session)
            grant_user_app_rights(user, modules, session, Permission(permission), client, email)

        success_notif = send_notification('Success', 'User added successfully',
                                          autoClose=2000, with_close_button=True)
        return token, False, success_notif, no_update
    except Exception as e:
        error_notif = send_notification('Failure', f'Error adding user: {str(e)}',
                                        autoClose=False, with_close_button=True)
        return no_update, True, error_notif, no_update


@safe_callback(
    Output({TYPE: MODAL, INDEX: REMOVE_USER_CONFIRM}, OPENED),
    Output(USER_DELETION_STORE, DATA),
    State(TOKEN, DATA),
    Input({TYPE: TABLE, INDEX: MANAGE_USERS}, CELL_RENDERER_DATA),
    State({TYPE: TABLE, INDEX: MANAGE_USERS}, ROW_DATA),
    check_access=False
)
def open_remove_confirmation_modal(token: dict,
                                   button_click: dict,
                                   row_data: list[dict]
                                   ) -> tuple[bool, dict]:
    """
    Opens the removal confirmation modal for a user and stores the user info in a store
    """
    if button_click and button_click[COL_ID] == 'Remove':
        return True, row_data[int(button_click[ROW_ID])]
    raise PreventUpdate


@safe_callback(
    Output({TYPE: MODAL, INDEX: REMOVE_USER_CONFIRM}, OPENED, allow_duplicate=True),
    Output(TOKEN, DATA, allow_duplicate=True),
    State(TOKEN, DATA),
    Input({TYPE: BUTTON, INDEX: REMOVE_USER_CONFIRM}, N_CLICKS),
    Input({TYPE: BUTTON, INDEX: REMOVE_USER_CANCEL}, N_CLICKS),
    State(USER_DELETION_STORE, DATA),
    prevent_initial_call=True,
    check_access=False
)
def remove_user_callback(token: dict,
                         confirm_button: int,
                         cancel_button: int,
                         user_data: dict,
                         ) -> tuple[bool, dict]:
    """
    Callback to remove a user from the AppUser table
    """
    if not confirm_button and not cancel_button:
        raise PreventUpdate

    if confirm_button:
        with Session(engine) as session:
            user = get_user_by_id(user_data[USER_ID], session)
            delete_user(user, session)

    return False, token
