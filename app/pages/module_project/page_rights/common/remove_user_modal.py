import dash_mantine_components as dmc
from ecodev_front import BUTTON
from ecodev_front import dash_icon
from ecodev_front import INDEX
from ecodev_front import MODAL
from ecodev_front import TYPE

from app.pages.module_project.page_rights import REMOVE_USER_CANCEL
from app.pages.module_project.page_rights import REMOVE_USER_CONFIRM

REMOVE_CONFIRMATION_BUTTON = dmc.Button('Yes', id={TYPE: BUTTON, INDEX: REMOVE_USER_CONFIRM},
                                        leftSection=dash_icon('lsicon:submit-outline'),
                                        variant='outline', color='blue',
                                        w=100)
REMOVE_CANCELLATION_BUTTON = dmc.Button('No', id={TYPE: BUTTON, INDEX: REMOVE_USER_CANCEL},
                                        leftSection=dash_icon('nonicons:not-found-16'),
                                        variant='outline', color='red',
                                        w=100)

REMOVE_USER_MODAL = dmc.Modal(
    children=dmc.Alert(color='red', title='Are you sure you want to remove this user?',
                       children=dmc.Group([REMOVE_CONFIRMATION_BUTTON, REMOVE_CANCELLATION_BUTTON],
                                          justify='center')),
    id={TYPE: MODAL, INDEX: REMOVE_USER_CONFIRM},
    withCloseButton=False,
    padding=0,
    centered=True)
