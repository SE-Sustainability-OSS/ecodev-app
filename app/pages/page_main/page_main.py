"""
Module implementing the main page
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import State
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import Page
from ecodev_front import TOKEN
from sqlmodel import Session

from app.constants import ALERT_STORE
from app.constants import PROJECT_ID_STORE
from app.pages.common.page_access import check_page_access
from app.pages.page_main.common.c_intro_text import INTRO_TEXT
from app.pages.page_main.common.cb_documentation_popup import DOCUMENTATION
from app.pages.page_main.common.cb_documentation_popup import documentation_popup
from app.pages.page_main.project_options.cb_module_buttons import module_buttons
from app.pages.page_main.project_options.cb_project_loader import project_loader

log = logger_get(__name__)


PAGE_MAIN = Page(
    module=__name__,
    name='main',
    icon='raphael:home',
    title='Main Page',
    description='',
    layout=basic_layout,
)


@callback(Output(PAGE_MAIN.id, CHILDREN),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          State(ALERT_STORE, DATA),)
def get_main_page(token: dict, project_id: int | None, alert_store: dict[str, bool]) -> html.Div:
    """
    Renders the main / landing page, on which user either create an new project,
    or select a previous project which displays module buttons.
    """
    with Session(engine) as session:
        page = html.Div([
            dmc.Container([
                dmc.Stack([
                    INTRO_TEXT,
                    documentation_popup() if alert_store.get(DOCUMENTATION, True) else None,
                    project_loader(token, project_id, session),
                    module_buttons(token, project_id, session),
                ], gap='xs', w='100%'),
            ], w='80%', fluid=True)
        ])
        return check_page_access(token, page)
