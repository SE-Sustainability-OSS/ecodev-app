"""
File containing the project info save button
"""
import dash_mantine_components as dmc
from ecodev_front import BUTTON
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.pages.module_project.page_info import PROJECT_INFO_SAVE


SAVE_INFO_BUTTON = dmc.Button(
    'Save',
    id={TYPE: BUTTON, INDEX: PROJECT_INFO_SAVE},
    radius='sm',
    color='blue.7',
    size='md',
    miw='20%'
)
