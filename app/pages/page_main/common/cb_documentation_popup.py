"""
Module implementing the documentation popup on main page.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from ecodev_front import DATA
from ecodev_front import INDEX
from ecodev_front import N_CLICKS
from ecodev_front import STYLE
from ecodev_front import TYPE

from app.constants import ALERT_STORE
from app.constants import DOCUMENTATION_URL
from app.domain_model.color_utils import get_color
from app.pages.common.components.alert import ALERT
from app.pages.common.components.alert import ALERT_CLOSE_BUTTON_ID
from app.pages.common.components.alert import custom_alert


DOCUMENTATION_ICON_LINK = dmc.Tooltip([
    dmc.Anchor([
        dmc.ActionIcon(DashIconify(icon='bxs:book',
                                   color=get_color('blue.3'),
                                   width=50),
                       size='xl',
                       variant='transparent',
                       n_clicks=0,
                       )
    ], href=DOCUMENTATION_URL, target='_blank')
], label='Documentation', fz=16, color=get_color('blue.3'),
    position='bottom', withArrow=True
)
DOCUMENTATION_TEXT = dmc.Group([
    dmc.Text("""If this is your first time using this tool, we
                    recommend you read through the documentation, which
                    will always remain accessible through the book icon at
                    top-right of the page.""",
             c='gray', fs='italic', fz=15, ta='left', w='80%'),
    DOCUMENTATION_ICON_LINK
], justify='space-around')

DOCUMENTATION = 'documentation'


def documentation_popup() -> dmc.Container:
    """
    Renders the documentation popup.
    """
    return custom_alert(id=DOCUMENTATION,
                        type='info',
                        title='Info',
                        msg=DOCUMENTATION_TEXT,
                        withCloseButton=True)


@callback(Output({TYPE: ALERT, INDEX: DOCUMENTATION}, STYLE),
          Output(ALERT_STORE, DATA),
          Input({TYPE: ALERT_CLOSE_BUTTON_ID, INDEX: DOCUMENTATION}, N_CLICKS),
          prevent_initial_call=True)
def close_documentation_popup(n_clicks: int) -> tuple[dict[str, str], dict[str, bool]]:
    """
    Closes the documentation popup.
    """
    if not n_clicks:
        raise PreventUpdate

    return {'display': 'none'}, {DOCUMENTATION: False}
