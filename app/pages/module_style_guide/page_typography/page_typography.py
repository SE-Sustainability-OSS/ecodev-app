"""
Module implementing the typography page of the style-guide
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash import State
from ecodev_core import logger_get
from ecodev_front import app_title
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import Page
from ecodev_front import page_title
from ecodev_front import section_title
from ecodev_front import subtext
from ecodev_front import subtitle
from ecodev_front import text_title
from ecodev_front import TOKEN

from app.constants import PROJECT_ID_STORE
from app.pages.common.page_access import check_page_access

log = logger_get(__name__)

PAGE_TYPO = Page(
    module=__name__,
    name='typography',
    icon='octicon:typography-16',
    title='Typography',
    description='Our ecoact typograpghy embedded into our Dash-Mantine theme',
    layout=header_layout
)


@callback(Output(PAGE_TYPO.id, CHILDREN),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          prevent_initial_call=True)
def render_page(token: dict, project_id: int):
    """
    Renders page component once token has been validated.
    """
    page = dmc.Group([
        dmc.Stack([
            section_title('Default headers'),
            dmc.Text('The following header typographies are embedded into our dmc.Theme:', mb=20),
            dmc.Title('Title h1', order=1, ta='left'),
            dmc.Title('Title h2', order=2, ta='left'),
            dmc.Title('Title h3', order=3, ta='left'),
            dmc.Title('Title h4', order=4, ta='left'),
            dmc.Title('Title h5', order=5, ta='left'),
            dmc.Title('Title h6', order=6, ta='left'),
            dmc.Text('Text', ta='left')
        ], justify='flex-start', align='flext-start', gap=0, ml=50),
        dmc.Stack([
            section_title('Ecodev-front text helpers (recommended)'),
            dmc.Text('The following header typographies can be imported from ecodev-front:', mb=20),
            app_title('App title'),
            page_title('Page title'),
            subtitle('Subtitle'),
            section_title('Section title', mt=20),
            subtitle('Subtitle'),
            text_title('Text title', mt=20),
            dmc.Text('Normal text'),
            subtext('Subtext', mb=20),
        ], justify='flex-start', align='flext-start', gap=0)
    ], grow=True, w='90%', align='flext-start',)
    return check_page_access(token, page)
