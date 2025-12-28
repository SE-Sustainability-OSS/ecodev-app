"""
Module implementing the app's header components.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_front import action_item
from ecodev_front import app_header_name
from ecodev_front import app_logo
from ecodev_front import dash_icon
from ecodev_front import login
from ecodev_front import LOGOUT_BTN_ID
from ecodev_front import menu
from ecodev_front import N_CLICKS
from ecodev_front import PATHNAME
from ecodev_front import URL
from ecodev_front.constants import LOGIN_PAGE_URL
from ecodev_front.constants import MAIN_PAGE_URL
from ecodev_front.ids import HOME_BUTTON
from sqlmodel import Session

from app.constants import APP_NAME
from app.constants import DOCUMENTATION_URL
from app.db_model.retrievers.access_retrievers import verify_project_module_access
from app.domain_model import AppModule
from app.pages.modules import MODULES

log = logger_get(__name__)

HEADER_DIVIDER = dmc.Divider(orientation='vertical', color='gray.2', mt=10, mb=10, ml=30, mr=30)
MAIN_PAGE = action_item(id='main-nav-button', label='main',
                        icon='grommet-icons:domain', href=MAIN_PAGE_URL)

HEADER_BUTTON_ID = 'header-button-id'


@callback(
    Output(URL, PATHNAME, allow_duplicate=True),
    Input(HOME_BUTTON, N_CLICKS),
    prevent_initial_call=True
)
def return_home(n_clicks: int):
    """
    Go to home page if button is clicked
    """
    if not n_clicks:
        raise PreventUpdate
    return MAIN_PAGE_URL


def display_app_header(pathname: str, token: dict, project_id: int | None) -> html.Div:
    """
    Function which determines the display of the various navbar buttons.
    I.e. Only show navbar to users, and only show certain additional buttons to admin users.
    """
    is_main_page = pathname == MAIN_PAGE_URL
    return html.Div([
        dmc.Group(justify='space-between',
                  align='stretch',
                  children=[
                      dmc.Group([
                          dmc.ActionIcon([
                                dash_icon('mdi:chevron-left', color='white', width=80),
                                dash_icon('ic:round-home', color='white', width=80)
                                ], variant='transparent', size='xl', id=HOME_BUTTON, ml=5, mr=5) if
                          not is_main_page else None,
                        app_header_name(APP_NAME)
                      ], mt='5px', ml='1%' if is_main_page else 5, align='center'),
                      header_app_pages(token, project_id),
                      header_generic_section(is_admin=True),
                  ])
    ])


def header_login_section() -> html.Div:
    """
    Login navbar components
    """
    return html.Div([
        dmc.Group(children=[app_logo(width='120px'), login()],
                  justify='space-between',
                  align='center',
                  c='white',
                  bg='blue.7'
                  )
    ])


def header_app_pages(token: dict, project_id: int | None) -> dmc.Group:
    """
    Header buttons for each app module
    """
    if not project_id:
        return dmc.Group(justify='space-around', gap=0)

    with Session(engine) as session:
        modules = verify_project_module_access(token, project_id, MODULES, session)

    if header_icons := [divider_icon
                        for module in modules if module.name != AppModule.PROJECT.value
                        for divider_icon in (HEADER_DIVIDER, module.header_icon)]:
        header_icons.append(HEADER_DIVIDER)

    return dmc.Group(header_icons, justify='space-around', gap=0)


def header_generic_section(is_admin: bool) -> dmc.Group:
    """
    Menu items for the user/admin specific pages.
    """
    logout_btn = action_item(
        id=LOGOUT_BTN_ID, label='LOGOUT', icon='ic:baseline-logout', href=LOGIN_PAGE_URL
    )

    doc_btn = action_item(id='documentation', label='DOCUMENTATION', icon='bxs:book',
                          href=DOCUMENTATION_URL, in_new_tab=True)

    admin_options = []  # type: ignore[var-annotated]
    admin_menu = menu(label='ADMIN', icon='eos-icons:admin-outlined',
                      menu_items=admin_options if is_admin else [])
    admin_comps = [admin_menu] if is_admin else []

    return dmc.Group([
        doc_btn,
        *admin_comps,
        logout_btn
    ], justify='right', mr='20px')
