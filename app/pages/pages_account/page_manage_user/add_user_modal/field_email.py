"""
File containing the user email input component for the add user modal.
"""
import dash_mantine_components as dmc
from ecodev_front import INDEX
from ecodev_front import section_title
from ecodev_front import TEXT_INPUT
from ecodev_front import TYPE

from app.pages.pages_account.page_manage_user import USER_EMAIL


def email_field() -> dmc.Stack:
    """
    Renders the email field as a text input for adding a single user.
    """
    return dmc.Stack([
        section_title('User email address'),
        dmc.TextInput(
            id={TYPE: TEXT_INPUT, INDEX: USER_EMAIL},
            placeholder='Enter email address',
            required=True,
            w='100%')
    ], gap=3, w='80%')
