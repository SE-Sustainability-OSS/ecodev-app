"""
Module implementing the create user page
NOTE: This page is only accessible to admin users.
NOTE: This only allows the creation of EXTERNAL users.
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core import safe_get_user
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import LOADING
from ecodev_front import N_CLICKS
from ecodev_front import Page
from ecodev_front import page_title
from ecodev_front import TOKEN
from ecodev_front import VALUE
from sqlmodel import Session

from app.db_model.inserters import upsert_user
from app.pages.common.custom_callback import safe_callback
from app.pages.module_project.page_rights.methodo.grant_access import validate_email
from app.pages.pages_account.page_create_user.common.create_user_form import CREATE_USER_EMAIL_INPUT_ID
from app.pages.pages_account.page_create_user.common.create_user_form import CREATE_USER_FORM
from app.pages.pages_account.page_create_user.common.create_user_form import CREATE_USER_MODULES_INPUT_ID
from app.pages.pages_account.page_create_user.common.create_user_form import CREATE_USER_NOTIFICATION_ID
from app.pages.pages_account.page_create_user.common.create_user_form import CREATE_USER_SUBMIT_BTN_ID


log = logger_get(__name__)

PAGE_CREATE_USER = Page(
    module=__name__,
    name='create-user',
    icon='mdi:user-add-outline',
    title='Create User',
    description='',
    layout=basic_layout,
)


@safe_callback(Output(PAGE_CREATE_USER.id, CHILDREN),
               Input(TOKEN, DATA),
               check_access=False)
def create_user_page(token: dict):
    """
    Renders the create user page, only if user is Admin
    """
    if not safe_get_user(token).permission == Permission.ADMIN:
        return dmc.Alert('You do not have permission to create users.',
                         title='Permission Error', color='red')

    return dmc.Stack([
        page_title('Create new external user'),
        CREATE_USER_FORM
    ], w='100%', align='center', justify='center', mt=20)


@safe_callback(
    Output(CREATE_USER_NOTIFICATION_ID, CHILDREN),
    State(TOKEN, DATA),
    Input(CREATE_USER_SUBMIT_BTN_ID, N_CLICKS),
    State(CREATE_USER_EMAIL_INPUT_ID, VALUE),
    State(CREATE_USER_MODULES_INPUT_ID, VALUE),
    check_access=False,
    prevent_initial_call=True,
    running=[(Output(CREATE_USER_SUBMIT_BTN_ID, LOADING), True, False)]
)
def add_client_and_module_rights(token: dict,
                                 n_clicks: int,
                                 email: str,
                                 modules: list[str],
                                 ) -> dmc.Alert:
    """
    Insert user to the database, based on their email address
    """
    if not n_clicks:
        raise PreventUpdate

    if not safe_get_user(token).permission == Permission.ADMIN:
        return dmc.Alert('You do not have permission to create users.',
                         title='Permission Error', color='red')

    if not email or not validate_email(email):
        return dmc.Alert('Please enter a valid email address.',
                         title='Email Error', color='red')

    with Session(engine) as session:
        try:
            upsert_user(email, modules, session)
            return dmc.Alert("""User should receive email with credentials shortly.
             Modules rights have been set successfully.""", title='Success', color='green')
        except Exception as e:
            return dmc.Alert(e, title='An error has occurred!', color='red')
