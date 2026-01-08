"""
Module implementing the add user components
"""
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from app.pages.module_registry import get_registered_modules

CREATE_USER_EMAIL_INPUT_ID = 'create-user-email-input-id'
CREATE_USER_MODULES_INPUT_ID = 'create-user-modules-input-id'
CREATE_USER_SUBMIT_BTN_ID = 'create-user-submit-button-id'
CREATE_USER_NOTIFICATION_ID = 'create-user-notification-id'

USER_EMAIL = dmc.TextInput(
    id=CREATE_USER_EMAIL_INPUT_ID,
    label="User's email:",
    required=True,
    leftSection=DashIconify(icon='ic:round-alternate-email'),
    w='50%'
)


def display_accessible_modules() -> dmc.MultiSelect:
    """
    Renders the accessible modules selection component, prefilled with all modules.
    """
    data = [{'value': module.name, 'label': module.name.capitalize()}
            for module in get_registered_modules()]
    return dmc.MultiSelect(
        label='Accessible modules',
        data=data,
        value=[modules['value'] for modules in data],
        id=CREATE_USER_MODULES_INPUT_ID,
        w=350,
    )


USER_BUTTON = dmc.Button('Submit', id=CREATE_USER_SUBMIT_BTN_ID, w='50%')

USER_NOTIF = dmc.Box(id=CREATE_USER_NOTIFICATION_ID, w='100%')

CREATE_USER_FORM = dmc.Stack([
    USER_EMAIL,
    display_accessible_modules(),
    USER_BUTTON,
    USER_NOTIF
], w=550, align='center', justify='center')
