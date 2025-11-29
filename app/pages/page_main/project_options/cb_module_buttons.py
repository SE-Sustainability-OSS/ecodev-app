"""
File containing the main page button leading to the various app module pages
"""
import dash_mantine_components as dmc
from dash import ALL
from dash import callback
from dash import ctx
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_front import DATA
from ecodev_front import INDEX
from ecodev_front import N_CLICKS
from ecodev_front import PATHNAME
from ecodev_front import STYLE
from ecodev_front import TOKEN
from ecodev_front import TYPE
from ecodev_front import URL
from ecodev_front import VALUE
from ecodev_front.constants import MAIN_PAGE_URL
from ecodev_front.ids import MODULE_BUTTON
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.db_model.retrievers.access_retrievers import get_accessible_modules
from app.pages.module_project.m_project import MODULE_PROJECT
from app.pages.modules import MODULES
from app.pages.page_main.project_options import NEW_PROJECT_BUTTON_ID
from app.pages.page_main.project_options import PROJECT_BUTTONS_PLACEHOLER_ID
from app.pages.page_main.project_options import PROJECT_SELECT_ID


def module_buttons(token: dict, project_id: int | None, session: Session) -> dmc.Stack:
    """
    Renders the various user options when a project is selected
    """
    return dmc.Stack(
        id=PROJECT_BUTTONS_PLACEHOLER_ID,
        children=[
            dmc.Group([
                module.render_main_page_button()
                for module in get_accessible_modules(token, project_id, MODULES, session)
            ], justify='center', grow=True, w='100%'),
        ], style={'display': 'none'})


@callback(Output(URL, PATHNAME, allow_duplicate=True),
          Output(PROJECT_ID_STORE, DATA, allow_duplicate=True),
          Input({TYPE: MODULE_BUTTON, INDEX: ALL}, N_CLICKS),
          State(URL, PATHNAME),
          State(PROJECT_ID_STORE, DATA),
          prevent_initial_call=True)
def reroute_to_project_page(n_clicks: list[int], pathname: str, project_id: int):
    """
    Reroutes users to the correct module page when clicking on a main page button.
    """
    if not any(n_clicks) or pathname != MAIN_PAGE_URL:
        raise PreventUpdate

    if (module_id := ctx.triggered_id[INDEX]) == NEW_PROJECT_BUTTON_ID:
        return MODULE_PROJECT.pages[0].url, None

    url_mapping = {
        module.id: module.pages[0].url
        for module in MODULES
    }

    return url_mapping.get(module_id), project_id


@callback(Output(PROJECT_BUTTONS_PLACEHOLER_ID, STYLE),
          Input(TOKEN, DATA),
          Input(PROJECT_SELECT_ID, VALUE))
def display_options(token: dict, project_id: str) -> dmc.Stack:
    """
    Callback to display report options, once a report is selected
    """
    return {'display': 'block' if project_id else 'none'}
