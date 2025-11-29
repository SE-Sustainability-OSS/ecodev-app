import dash_mantine_components as dmc
from ecodev_front import dash_icon

from app.pages.module_project.page_rights import REMOVE_USER_CANCELLATION_BUTTON_ID
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRMATION_BUTTON_ID
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRMATION_MODAL_ID

REMOVE_CONFIRMATION_BUTTON = dmc.Button('Yes', id=REMOVE_USER_CONFIRMATION_BUTTON_ID,
                                        leftSection=dash_icon('lsicon:submit-outline'),
                                        variant='outline', color='blue',
                                        w=100)
REMOVE_CANCELLATION_BUTTON = dmc.Button('No', id=REMOVE_USER_CANCELLATION_BUTTON_ID,
                                        leftSection=dash_icon('nonicons:not-found-16'),
                                        variant='outline', color='red',
                                        w=100)

REMOVE_USER_MODAL = dmc.Modal(
    children=dmc.Alert(color='red', title='Are you sure you want to remove this user?',
                       children=dmc.Group([REMOVE_CONFIRMATION_BUTTON, REMOVE_CANCELLATION_BUTTON],
                                          justify='center')),
    id=REMOVE_USER_CONFIRMATION_MODAL_ID,
    withCloseButton=False,
    padding=0,
    centered=True)
