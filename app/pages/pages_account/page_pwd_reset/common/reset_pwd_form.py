"""
Module implementing the reset password form and callback
"""
import re
from typing import Any

import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import safe_get_user
from ecodev_core.authentication import _hash_password
from ecodev_core.authentication import attempt_to_log
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import ERROR
from ecodev_front import N_CLICKS
from ecodev_front import subtext
from ecodev_front import TOKEN
from ecodev_front import VALUE
from sqlmodel import Session

from app.pages.common.custom_callback import safe_callback


log = logger_get(__name__)

RESET_PWD_NEW_PWD_INPUT_ID = 'reset-pwd-new-pwd-input-id'
RESET_PWD_CONFIRM_NEW_PWD_INPUT_ID = 'reset-pwd-new-confirm-pwd-input-id'
RESET_PWD_SUBMIT_BTN = 'reset-user-submit-button'
RESET_PWD_NOTIFICATION = 'reset-user-notification'
CURRENT_PWD_FIELD_ID = 'reset-pwd-current-pwd-input-i'


CURRENT_PWD_FIELD = dmc.PasswordInput(
    id=CURRENT_PWD_FIELD_ID,
    label='Current password:',
    required=True,
    w='100%',
)

NEW_PWD_FIELD = dmc.PasswordInput(
    id=RESET_PWD_NEW_PWD_INPUT_ID,
    label='New password:',
    required=True,
    w='100%',
)

CONFIRM_PWD_FIELD = dmc.PasswordInput(
    id=RESET_PWD_CONFIRM_NEW_PWD_INPUT_ID,
    label='Confirm password:',
    required=True,
    w='100%',
)

RESET_PWD_INSTRUCTIONS = dmc.Stack([
    subtext("""Passwords must be at least 15 characters long, contain at least one uppercase letter,
            one lowercase letter, one number and one of the following special characters: """,
            ta='center'),
    subtext('! ? . , ; @ # ~ ] [ + = - / * ( ) & ^ % $ ', ta='center')
], gap=0, align='center', w=550, mb=10)


RESET_BUTTON = dmc.Button('Submit', id=RESET_PWD_SUBMIT_BTN, w=550)
RESET_NOTIF = dmc.Box(id=RESET_PWD_NOTIFICATION, w=550)


RESET_PWD_FORM = dmc.Stack([
    dmc.Stack([
        CURRENT_PWD_FIELD,
        NEW_PWD_FIELD,
        CONFIRM_PWD_FIELD
    ], w='40%', align='center', justify='center'),
    RESET_PWD_INSTRUCTIONS,
    RESET_BUTTON,
    RESET_NOTIF,
], w='100%', align='center', gap='xs', justify='center')


@safe_callback(
    Output(RESET_PWD_NOTIFICATION, CHILDREN),
    Output(CURRENT_PWD_FIELD_ID, ERROR),
    Output(RESET_PWD_NEW_PWD_INPUT_ID, ERROR),
    Output(RESET_PWD_CONFIRM_NEW_PWD_INPUT_ID, ERROR),
    State(TOKEN, DATA),
    Input(RESET_PWD_SUBMIT_BTN, N_CLICKS),
    State(CURRENT_PWD_FIELD_ID, VALUE),
    State(RESET_PWD_NEW_PWD_INPUT_ID, VALUE),
    State(RESET_PWD_CONFIRM_NEW_PWD_INPUT_ID, VALUE),
    prevent_initial_call=True,
)
def reset_passwd(token: dict,
                 n_clicks: int,
                 current_pwd,
                 new_pwd: str,
                 confirm_pwd: str) -> tuple[Any, bool, bool, bool]:
    """
    Upsert user to the database, based on their email address
    """
    if not n_clicks:
        raise PreventUpdate

    with (Session(engine) as session):
        user = safe_get_user(token)

        try:
            attempt_to_log(user.user, current_pwd, session)
        except Exception:
            return dmc.Alert('Please enter your valid current password', color='red'
                             ), True, False, False

        if not new_pwd:
            return dmc.Alert('Please enter a new password',  color='red'
                             ), False, True, False

        if not confirm_pwd or new_pwd != confirm_pwd:
            return dmc.Alert('New password and confirmation do not match.', color='red'
                             ), False, False, True

        if errors := check_pwd_requirements(new_pwd):
            return dmc.Alert([
                dmc.Text('Password does not meet the requirements:', fz=13, fw=700),
                *[dmc.Text(f' - {error}', fz=13) for error in errors]
            ], color='red'), False, False, False

        user.password = _hash_password(new_pwd)
        session.commit()

    return dmc.Alert('Your password has been updated!', color='green'), False, False, False


def check_pwd_requirements(password: str) -> dmc.Alert | None:
    """
    Helper function to check if the password meets the requirements:
    NOTE: Passwords must be at least 15 characters long, contain at least one uppercase letter, one
    lowercase letter, one number and one of the following special characters: !?.,;@#~][+=-/*()&^%$
    """
    errors = []
    allowed_specials = set('!?.,;@#~][+=-/*()&^%$')

    if len(password) < 15:
        errors.append(f'Password is only {len(password)} characters long.')

    if not re.search(r'[A-Z]', password):
        errors.append('Password is missing an upper case letter.')

    if not re.search(r'[a-z]', password):
        errors.append('Password is missing a lower case letter.')

    if not re.search(r'\d', password):
        errors.append('Password is missing a number.')

    if not any(char in allowed_specials for char in password):
        errors.append('Password is missing a special character.')

    for char in password:
        if not char.isalnum() and char not in allowed_specials:
            errors.append('Password includes a special character that is not allowed.')

    return errors
