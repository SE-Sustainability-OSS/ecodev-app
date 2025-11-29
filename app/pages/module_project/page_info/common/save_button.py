"""
File containing the project info save button
"""
import dash_mantine_components as dmc

from app.pages.module_project.page_info.common import PROJECT_INFO_SAVE_BTN_ID


SAVE_INFO_BUTTON = dmc.Button(
    'Save',
    id=PROJECT_INFO_SAVE_BTN_ID,
    radius='sm',
    color='blue.7',
    size='md',
    miw='20%'
)
