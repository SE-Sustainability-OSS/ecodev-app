"""
Add/update user buttons
"""
import dash_mantine_components as dmc
from ecodev_front import BUTTON
from ecodev_front import dash_icon
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.pages.pages_account.page_manage_user import ADD_USER
from app.pages.pages_account.page_manage_user import UPDATE_USERS

ADD_USER_BTN = dmc.Button('Add Users', id={TYPE: BUTTON, INDEX: ADD_USER},
                          color='blue',
                          leftSection=dash_icon('material-symbols-light:group-add-rounded'))

UPDATE_USERS_BTN = dmc.Button('Update Users', id={TYPE: BUTTON, INDEX: UPDATE_USERS},
                              color='blue', variant='outline',
                              leftSection=dash_icon('hugeicons:location-update-01'))


def manage_users_button():
    """
    Renders the manage users buttons
    """
    return dmc.Group([
        ADD_USER_BTN,
        dmc.Divider(h=35, orientation='vertical', size='sm'),
        UPDATE_USERS_BTN
    ], mr=30)
