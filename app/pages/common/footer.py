"""
Module implementing an example of customisable footer components.
"""
import dash_mantine_components as dmc
from ecodev_front import app_logo


def main_footer() -> dmc.Group:
    """
    Render's the app's main footer
    """
    return dmc.Group([
        dmc.Affix(app_logo(ratio=300/91, width='70px'),
                  position={'bottom': 12, 'left': '50%'}, style={'transform': 'translateX(-50%)'}),
    ], justify='center', align='center', pt=5, mt=20)
