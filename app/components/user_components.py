"""
Module implementing all needed components for the user page
"""
import random
import re

import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from ecodev_core import engine
from ecodev_core import Permission
from ecodev_core.app_user import USER_INSERTOR
from ecodev_core.authentication import _hash_password
from ecodev_core.db_insertion import create_or_update
from ecodev_front import background_card
from ecodev_front import card_title
from ecodev_front import TOKEN
from sqlmodel import Session

from app.constants import COLORS_ID
from app.constants import PASSWORD_LENGTH
from app.constants import PWD_CHAR_CHOICES
from app.db_model import AppUser
from app.methodo import send_credentials


CREATE_USER_EMAIL = 'create-user-email'
CREATE_USER_PERMISSION = 'create-user-permission'
CREATE_USER_SUBMIT_BTN = 'create-user-submit-button'
CREATE_USER_NOTIFICATION = 'create-user-notification'
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

USER_TEXT = dmc.TextInput(
    id=CREATE_USER_EMAIL,
    label="User's email:",
    required=True,
    leftSection=DashIconify(icon='ic:round-alternate-email'),
)
USER_PERMISSION = dmc.Select(
    id=CREATE_USER_PERMISSION,
    label='Permissions level',
    value='Consultant',
    data=['Consultant', 'Admin', 'Client'],
)
USER_BUTTON = dmc.Button('Submit', id=CREATE_USER_SUBMIT_BTN, color=COLORS_ID)
USER_NOTIF = html.Div(id=CREATE_USER_NOTIFICATION)

USER_COMPONENTS = background_card([
    dmc.Stack(
        [
            card_title('Create a new user', align='left'),
            USER_TEXT,
            USER_PERMISSION,
            dmc.Space(h=10),
            USER_BUTTON,
            dmc.Space(h=10),
            USER_NOTIF,
        ]
    )]
)


@callback(
    Output(CREATE_USER_NOTIFICATION, 'children'),
    Output(CREATE_USER_EMAIL, 'error'),
    State(TOKEN, 'data'),
    Input(CREATE_USER_SUBMIT_BTN, 'n_clicks'),
    State(CREATE_USER_EMAIL, 'value'),
    State(CREATE_USER_PERMISSION, 'value'),
    prevent_initial_call=True,
)
def add_user(token, n_clicks, email, permission) -> tuple[dmc.Alert, bool]:
    """
    Upsert user to the database, based on their email address
    """
    if not n_clicks:
        raise PreventUpdate

    try:
        if _validate_email(email) is False:
            return _error_alert(
                'Please make sure email is valid', title='Invalid Email'
            ), True
        user, password = _create_user_credentials(email, permission)
        _upsert_user(user)
        send_credentials(email, user, password)
    except Exception as e:
        return _error_alert(
            f'Could not add new user. Contact dev / support team. {e}',
            title='Function / Database Error',
        ), False
    return dmc.Alert(
        'User should receive email with credentials shortly.',
        title='Success',
        color='green',
    ), False


def _error_alert(message: str, title='Permission Error') -> dmc.Alert:
    """
    Format error message
    """
    return dmc.Alert(message, title, color='red')


def _validate_email(email: str) -> bool:
    """
    Simple email validator
    """
    return re.match(EMAIL_REGEX, email) is not None


def _create_user_credentials(email: str, permission: Permission) -> tuple[AppUser, str]:
    """
    Auto-generated password and hashed-password.
    """
    password = ''.join(random.choice(PWD_CHAR_CHOICES) for i in range(PASSWORD_LENGTH))
    user = AppUser(user=email, password=_hash_password(password), permission=permission)
    return user, password


def _upsert_user(user: AppUser) -> None:
    """
    Upsert new user into DB.
    """
    with Session(engine) as session:
        session.add(create_or_update(session, user.dict(), USER_INSERTOR))
        session.commit()
