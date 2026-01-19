"""
File containing the buttons of the add user modal.
"""
import dash_mantine_components as dmc
from ecodev_front import BUTTON
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.pages.pages_account.page_manage_user import ADD_USER_MODAL_CANCEL
from app.pages.pages_account.page_manage_user import ADD_USER_MODAL_CONFIRM

ADD_USER_MODAL_CONFIRM_BTN = dmc.Button('Add User',
                                        id={TYPE: BUTTON, INDEX: ADD_USER_MODAL_CONFIRM},
                                        color='blue')

ADD_USER_MODAL_CANCEL_BTN = dmc.Button('Cancel',
                                       id={TYPE: BUTTON, INDEX: ADD_USER_MODAL_CANCEL},
                                       color='red', variant='outline')

MODAL_BUTTONS = dmc.Stack([
    dmc.Divider(w='60%', mt=10, mb=10),
    dmc.Group([ADD_USER_MODAL_CONFIRM_BTN, ADD_USER_MODAL_CANCEL_BTN], w='60%', grow=True),
], w='100%', align='center')
