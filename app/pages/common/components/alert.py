"""
Module implementing the alert component
"""
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from ecodev_front import background_card
from ecodev_front import card_title
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.domain_model.color_utils import get_color

ALERT = 'alert'
ALERT_CLOSE_BUTTON_ID = 'alert-close-button-id'


def custom_alert(type: str,
                 title: str,
                 msg: str,
                 id: str | None = None,
                 withCloseButton: bool = True,
                 w: str | int | None = None) -> dmc.Alert:
    """
    Renders a stylised alert.

    Possible alert types are: 'info', 'success', 'error', and 'warning'.
    """
    type_color_mapping = {
        'error': get_color('red.6'),
        'success': get_color('green.6'),
        'info': get_color('blue.6'),
        'warning': get_color('yellow.6')
    }
    return background_card([
        card_title(title, background_color=type_color_mapping[type],
                   component=[dmc.ActionIcon(
                       DashIconify(icon='charm:cross', width=28),
                       id={TYPE: ALERT_CLOSE_BUTTON_ID, INDEX: id or type},
                       size='lg', color=type_color_mapping[type], mr=10)
            if withCloseButton else None],
        ),
        dmc.Text(msg, c='dimmed', fs='italic', mt=10, ta='left')
    ], style={'width': w or '100%', 'z-index': 1000}, card_id={TYPE: ALERT, INDEX: id or type})
