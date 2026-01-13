"""
Add/update rights buttons
"""
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from ecodev_core import logger_get
from ecodev_front import BUTTON
from ecodev_front import centered_div
from ecodev_front import dash_icon
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.pages.module_project.page_rights import ADD_USER_RIGHTS
from app.pages.module_project.page_rights import DELETE_PROJECT
from app.pages.module_project.page_rights import UPDATE_RIGHTS
from app.pages.module_project.page_rights.common.delete_project_modal import DELETE_CONFIRMATION_MODAL

log = logger_get(__name__)

ADD_USERS_BTN = dmc.Button('Add Users', id={TYPE: BUTTON, INDEX: ADD_USER_RIGHTS},
                           color='blue',
                           leftSection=dash_icon('material-symbols-light:group-add-rounded'))

UPDATE_RIGHTS_BTN = dmc.Button('Update Rights', id={TYPE: BUTTON, INDEX: UPDATE_RIGHTS},
                               color='green', variant='outline',
                               leftSection=dash_icon('hugeicons:location-update-01'))


def manage_rights_button():
    """
    Renders the manage rights buttons
    """
    return dmc.Group([ADD_USERS_BTN, UPDATE_RIGHTS_BTN], grow=True)


DELETE_PROJECT_BUTTON = dmc.Button(
    'Delete project',
    id={TYPE: BUTTON, INDEX: DELETE_PROJECT},
    leftSection=DashIconify(icon='solar:trash-bin-trash-outline', width=24),
    size='md',
    radius='md',
    variant='outline',
    color='red',
    style={'width': '200px'}
)


def delete_project_button() -> html.Div:
    """
    Renders project delete button & its confirmation modal
    """
    return centered_div(dmc.Stack([
        dmc.Divider(w='60%'),
        DELETE_PROJECT_BUTTON,
        DELETE_CONFIRMATION_MODAL
    ], align='center', style={'width': '80%'}))
