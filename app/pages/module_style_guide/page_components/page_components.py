"""
Module implementing the buttons components page of the style-guide
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from dash import State
from ecodev_core import logger_get
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import Page
from ecodev_front import section_title
from ecodev_front import TOKEN

from app.constants import PROJECT_ID_STORE
from app.pages.common.components.alert import custom_alert
from app.pages.common.custom_callback import safe_callback

log = logger_get(__name__)

PAGE_COMPONENTS = Page(
    module=__name__,
    name='components',
    icon='uiw:component',
    title='Components',
    description='Example of components using our custom colors & theme.',
    layout=header_layout
)


@safe_callback(Output(PAGE_COMPONENTS.id, CHILDREN),
               Input(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA))
def render_page(token: dict, project_id: int):
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    return dmc.Stack([
        buttons_section(),
        alert_section()
    ], align='flext-start', gap='30px', w='95%', m='auto')


def buttons_section() -> dmc.Stack:
    """
    Renders a section with the various button types.
    """
    return dmc.Stack([
        section_title('Buttons'),
        dmc.Group([
            dmc.Button('Primary button', w='300px'),
            dmc.Button('Secondary button', variant='outline', w='300px'),
            dmc.Button('Success button', variant='outline', color='green', w='300px'),
            dmc.Button('Warning button', variant='outline', color='red', w='300px')
        ], grow=True, gap='lg')
    ])


def alert_section() -> dmc.Stack:
    """
    Renders a section with the various button types.
    """
    return dmc.Stack([
        section_title('Alerts'),
        dmc.Stack([
            custom_alert(type='info', title='Info', msg='This is an information message',
                         withCloseButton=True),
            custom_alert(type='error', title='Error', msg='This is an error message'),
            custom_alert(type='success', title='Success', msg='This is a success message'),
            custom_alert(type='warning', title='Warning', msg='This is a warning message'),
        ], gap='lg', align='flex-start')
    ])
