"""
Module implementing the color palette page of the style-guide
"""
import dash_mantine_components as dmc
from dash import ALL
from dash import callback
from dash import ctx
from dash import dcc
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import logger_get
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import header_layout
from ecodev_front import INDEX
from ecodev_front import N_CLICKS
from ecodev_front import Page
from ecodev_front import TOKEN
from ecodev_front import TYPE

from app.pages.common.custom_callback import safe_callback
from app.pages.module_style_guide.page_colors import COLOR_PALETTE_CLIPBOARD
from app.pages.module_style_guide.page_colors import COLOR_PALETTE_HEX_BUTTON
from app.pages.module_style_guide.page_colors.common.color_box import CLAY_PALETTE
from app.pages.module_style_guide.page_colors.common.color_box import EARTH_PALETTE
from app.pages.module_style_guide.page_colors.common.color_box import GRAY_PALETTE
from app.pages.module_style_guide.page_colors.common.color_box import PLANT_PALETTE
from app.pages.module_style_guide.page_colors.common.color_box import PRIMARY_COLORS
from app.pages.module_style_guide.page_colors.common.color_box import SAND_PALETTE
from app.pages.module_style_guide.page_colors.common.color_box import SEA_PALETTE
from app.pages.module_style_guide.page_colors.common.how_to_text import HOW_TO_TEXT

log = logger_get(__name__)

PAGE_COLORS = Page(
    module=__name__,
    name='colors',
    icon='ic:round-color-lens',
    title='Colors',
    description='Our ecoact color palettes embedded into our Dash-Mantine theme',
    layout=header_layout
)


@safe_callback(Output(PAGE_COLORS.id, CHILDREN),
               Input(TOKEN, DATA))
def render_page(token: dict):
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    return dmc.Stack([
        HOW_TO_TEXT,
        dcc.Clipboard(id=COLOR_PALETTE_CLIPBOARD, style={'display': 'none'}),
        dmc.Group([
            PRIMARY_COLORS,
        ], align='center'),
        GRAY_PALETTE,
        SEA_PALETTE,
        PLANT_PALETTE,
        CLAY_PALETTE,
        SAND_PALETTE,
        EARTH_PALETTE,
    ], align='center', gap='xl', ml=50)


@callback(
    Output(COLOR_PALETTE_CLIPBOARD, 'content'),
    Output(COLOR_PALETTE_CLIPBOARD, N_CLICKS),
    Input({TYPE: COLOR_PALETTE_HEX_BUTTON, INDEX: ALL}, N_CLICKS),
    State(COLOR_PALETTE_CLIPBOARD, N_CLICKS),
)
def custom_copy(hexes, n_clicks):
    """
    Allows users to copy the color name from the color palette to the clipboard.
    """
    if not ctx.triggered_id:
        raise PreventUpdate
    return ctx.triggered_id[INDEX], (n_clicks or 0)+1
