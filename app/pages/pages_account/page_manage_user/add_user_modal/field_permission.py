"""
File containing the user permission selection component for the add user modal.
"""
import dash_mantine_components as dmc
from ecodev_core import Permission
from ecodev_front import INDEX
from ecodev_front import section_title
from ecodev_front import SELECT
from ecodev_front import TYPE

from app.pages.pages_account.page_manage_user import USER_PERMISSION


def permission_field() -> dmc.Stack:
    """
    Renders the permission field as a select dropdown for choosing user permission level.
    """
    permission_options = [
        {'value': p.value, 'label': p.value.capitalize()}
        for p in Permission
    ]

    return dmc.Stack([
        section_title('User permission'),
        dmc.Select(
            id={TYPE: SELECT, INDEX: USER_PERMISSION},
            data=permission_options,
            placeholder='Select permission level',
            required=True,
            w='100%')
    ], gap=3, w='80%')
