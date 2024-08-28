"""
Module containing the intro / main page components
"""
import dash_mantine_components as dmc
from ecodev_front import action_item

from app.constants import MAIN_COLOR


DOCUMENTATION_SECTION = dmc.Group([
    action_item(
        id='doc-link-id',
        label='Documentation',
        icon='bxs:book',
        icon_color=MAIN_COLOR,
        href='https://ecodev-doc.lcabox.com/',
        in_new_tab=True,
    ),
    action_item(
        id='source-code-link-id',
        label='Source code',
        icon='streamline:code-monitor-1-solid',
        icon_color=MAIN_COLOR,
        href='https://github.com/SE-Sustainability-OSS/ecodev-app/',
        in_new_tab=True,
    )
], gap='xl')


INTRO_SECTION = dmc.Stack([
    dmc.Title('EcoDev App', fz=64),
    dmc.Space(h=15),
    dmc.Text(['This application aims to showcase the ',
              dmc.Mark('EcoDev Open Source libraries', color='blue'),
              """. Within, you will find some basic web-app functionalities such as user login,
             protected pages, adding users to database, displaying navbars, graphs, etc."""],
             c='dimmed', fz=18),
    DOCUMENTATION_SECTION,
    dmc.Text('We hope it will also add some velocity to your python web-apps.',
             c='dimmed', fz=18),
], align='center')
