import dash_mantine_components as dmc
from dash import callback
from dash import ctx
from dash import html
from dash import Input
from dash import no_update
from dash import Output
from dash import register_page
from dash import State
from dash_iconify import DashIconify
from ecodev_core import logger_get
from ecodev_core import safe_get_user
from ecodev_front import APPSHELL
from ecodev_front import DATA
from ecodev_front import NAVBAR
from ecodev_front import TOKEN

from app.components.page_helpers import generic_page
from app.constants import APP_COLORS
from app.constants import COLORS_ID
from app.pages.layouts import ASIDE_BUTTON_ID
from app.pages.layouts import CLOSE_ASIDE_BUTTON_ID
from app.pages.layouts import COLLAPSIBLE_ASIDE_PAGE_ID
from app.pages.layouts import COLLAPSIBLE_ASIDE_PAGE_URL
from app.pages.layouts import OPEN_ASIDE_BUTTON_ID

log = logger_get(__name__)
register_page(__name__, path=COLLAPSIBLE_ASIDE_PAGE_URL)


SHOW = {'display': 'block'}
HIDE = {'display': 'none'}
ASIDE_WIDTH = 17

OPEN_ASIDE_BUTTON = dmc.Affix(dmc.ActionIcon(
    DashIconify(icon='ant-design:right-outlined', width=25),
    variant='default', size=40,  c='white',
    style={'backgroundColor': APP_COLORS[COLORS_ID][6]},
    id={'type': ASIDE_BUTTON_ID, 'index': 'open'}),
    position={'top': 63, 'left': -5}, zIndex=91,
    id=OPEN_ASIDE_BUTTON_ID, style=HIDE
)

CLOSE_ASIDE_BUTTON = dmc.Affix(dmc.ActionIcon(
    DashIconify(icon='oui:cross', width=25),
    variant='default', size=40, c='white',
    style={'backgroundColor': APP_COLORS[COLORS_ID][6]},
    id={'type': ASIDE_BUTTON_ID, 'index': 'close'}),
    position={'top': 63, 'left': f'{ASIDE_WIDTH-0.3}%'}, zIndex=89,
    id=CLOSE_ASIDE_BUTTON_ID
)

ASIDE_BUTTONS = html.Div([CLOSE_ASIDE_BUTTON, OPEN_ASIDE_BUTTON])


layout = [html.Div(id=COLLAPSIBLE_ASIDE_PAGE_ID,
                   style={'display': 'flex', 'justifyContent': 'center'}
                   )]


@callback(Output(COLLAPSIBLE_ASIDE_PAGE_ID, 'children'),
          Input(TOKEN, 'data'))
def render_page(token: dict):
    """
    Callback rendering the collapsible page's main content.
    The aside buttons must displayed upon app instantiation.
    """
    page = [ASIDE_BUTTONS, dmc.Container(['Main content example'])]

    return generic_page(token, page)


@callback(Output(APPSHELL, NAVBAR, allow_duplicate=True),
          Output(NAVBAR, 'children', allow_duplicate=True),
          Output(NAVBAR, 'style'),
          Output(CLOSE_ASIDE_BUTTON_ID, 'style'),
          Output(OPEN_ASIDE_BUTTON_ID, 'style'),
          Input({'type': ASIDE_BUTTON_ID, 'index': 'close'}, 'n_clicks'),
          Input({'type': ASIDE_BUTTON_ID, 'index': 'open'}, 'n_clicks'),
          State(TOKEN, DATA),
          prevent_initial_call=True)
def show_hide_aside(close_aside_btn: int, open_aside_btn: int, token: dict):
    """
    Displays / collapse the left-sidebar.
    """
    if not safe_get_user(token):
        return {'width': '0%'}, [], HIDE, HIDE, HIDE
    if open_aside_btn and ctx.triggered_id['index'] == 'open':
        return {'width': f'{ASIDE_WIDTH}%'}, no_update, SHOW, SHOW, HIDE
    if close_aside_btn and ctx.triggered_id['index'] == 'close':
        return {'width': '0%'}, no_update, HIDE, HIDE, SHOW

    return {'width': f'{ASIDE_WIDTH}%'}, ['Aside content example'], SHOW, SHOW, HIDE
