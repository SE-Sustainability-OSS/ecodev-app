"""
Module implementing the app authentication / access callbacks.
NB: These callbacks must be imported in the common init file in order to be registered /created upon
app initialization
"""
from urllib.parse import parse_qs
from urllib.parse import urlparse

from dash import callback
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import attempt_to_log
from ecodev_core import ban_token
from ecodev_core import engine
from ecodev_core import get_access_token
from ecodev_core import is_banned
from ecodev_core import log_critical
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core import safe_get_user
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import FOOTER_ID
from ecodev_front import HEADER_ID
from ecodev_front import HREF
from ecodev_front import LOGIN_BTN_ID
from ecodev_front import LOGIN_PASSWORD_INPUT_ID
from ecodev_front import LOGIN_USERNAME_INPUT_ID
from ecodev_front import LOGOUT_BTN_ID
from ecodev_front import N_CLICKS
from ecodev_front import PATHNAME
from ecodev_front import TOKEN
from ecodev_front import URL
from ecodev_front import VALUE
from ecodev_front.constants import LOGIN_PAGE_URL
from ecodev_front.constants import MAIN_PAGE_URL
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.db_model.retrievers.access_retrievers import get_project_accessible_modules
from app.pages.common.footer import main_footer
from app.pages.common.header import display_app_header
from app.pages.common.header import header_login_section
from app.pages.module_project.m_project import MODULE_PROJECT
from app.pages.modules import MODULES
from app.pages.page_forbidden.not_forbidden_403 import PAGE_403
from app.pages.page_login.page_login import PAGE_LOGIN
from app.pages.page_main.page_main import PAGE_MAIN

log = logger_get(__name__)


@callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(URL, PATHNAME, allow_duplicate=True),
    Input(LOGIN_BTN_ID, N_CLICKS),
    State(LOGIN_USERNAME_INPUT_ID, VALUE),
    State(LOGIN_PASSWORD_INPUT_ID, VALUE),
    prevent_initial_call=True,
)
def user_login(n_clicks: int, username: str, password: str):
    """
    Callback when user presses the login button.
    Checks if user entered valid credentials, through my eco-auth
    """
    if not n_clicks:
        raise PreventUpdate
    try:
        with Session(engine) as session:
            if token := attempt_to_log(username, password, session):
                return {TOKEN: token}, MAIN_PAGE_URL
    except Exception as e:
        log_critical(f'{e} happened while trying to login', log)
        return {TOKEN: {}}, LOGIN_PAGE_URL


@callback(
    Output(HEADER_ID, CHILDREN),
    Output(FOOTER_ID, CHILDREN),
    Output(TOKEN, DATA, allow_duplicate=True),
    Input(TOKEN, DATA),
    Input(URL, HREF),
    Input(URL, PATHNAME),
    Input(PROJECT_ID_STORE, DATA),
    prevent_initial_call=True,
)
def update_header_footer_components(token: dict,
                                    href: str,
                                    pathname: str,
                                    project_id: int | None):
    """
    Header and footer update. If no valid token is present in the store, return only navbar header.
    Otherwise, return the full navbar with all the page app.
    """
    try:
        if safe_get_user(token):
            return display_app_header(pathname, token, project_id), main_footer(), token

        if not (token := parse_qs(urlparse(href).query).get(TOKEN)) or is_banned(token[0]):
            return header_login_section(), None, {TOKEN: None}

        # response = requests.get(
        #     USER_URL, headers={'Authorization': f'Bearer {token[0]}'}
        # )
        # upsert_new_user(token[0], response.json())  # type: ignore[dict-item]
        token = {TOKEN: {'access_token': token[0], 'token_type': 'bearer'}}
        return display_app_header(pathname, token, project_id), main_footer(), token

    except Exception as error:
        log_critical(str(error), log)
        return header_login_section(), None, {TOKEN: None}


@callback(
    Output(TOKEN, DATA, allow_duplicate=True),
    Output(URL, PATHNAME, allow_duplicate=True),
    Input(LOGOUT_BTN_ID, N_CLICKS),
    State(TOKEN, DATA),
    prevent_initial_call=True,
)
def user_logout(n_clicks: int, token: dict):
    """
    Resets token value when user logs out.
    """
    if not n_clicks:
        raise PreventUpdate
    with Session(engine) as session:
        ban_token(get_access_token(token), session)
    return {TOKEN: None}, LOGIN_PAGE_URL


@callback(Output(URL, PATHNAME),
          Input(URL, PATHNAME),
          Input(TOKEN, DATA),
          Input(PROJECT_ID_STORE, DATA))
def verify_page_access(pathname: str, token: dict, project_id: int):
    """
    Ensure that the user has access to the page, else reroute to page 403 (access forbidden)
    Add an exception if user has clicked on create new project for which
    """
    if not (user := safe_get_user(token)):
        return PAGE_LOGIN.url

    if pathname == PAGE_MAIN.url or user.permission == Permission.ADMIN:
        return no_update

    if pathname == MODULE_PROJECT.pages[0].url and project_id is None:
        return no_update

    with Session(engine) as session:
        for module in get_project_accessible_modules(user, project_id, MODULES, session):
            if pathname in [page.url for page in module.pages]:
                return no_update
    return PAGE_403.url
