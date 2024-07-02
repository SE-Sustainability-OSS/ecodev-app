"""
Module implementing an example of customisable navbar components.
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_front.components import action_item
from ecodev_front.components import app_header
from ecodev_front.components import app_logo
from ecodev_front.components import app_title
from ecodev_front.components import login
from ecodev_front.components import menu
from ecodev_front.components import menu_item
from ecodev_front.components import navbar_divider

from app.pages.inputs import FILE_UPLOAD_PAGE_URL
from app.pages.inputs import FORMS_PAGE_URL
from app.pages.inputs import IN_DATA_TABLE_PAGE_URL
from app.pages.inputs import SEARCH_BAR_PAGE_URL
from app.pages.layouts import LEFT_ASIDE_PAGE_URL
from app.pages.layouts import LEFT_RIGHT_ASIDE_PAGE_URL
from app.pages.layouts import RIGHT_ASIDE_PAGE_URL
from app.pages.layouts import SIMPLE_PAGE_URL
from app.pages.outputs import DASHBOARD_PAGE_URL
from app.pages.outputs import MAP_PAGE_URL
from app.pages.outputs import OUT_DATA_TABLE_PAGE_URL
from app.pages.outputs import REPORT_PAGE_URL

APP_TITLE = app_title()
APP_LOGO = app_logo()


def navbar(is_admin: bool = False) -> html.Div:
    """
    Function which determines the display of the various navbar buttons.
    Only show certain additional buttons to admin users.
    """
    return html.Div([dmc.Grid(
        children=[app_header(APP_TITLE, APP_LOGO), navbar_app_pages(),
                  user_admin_settings(is_admin)],
        justify='space-between',
        align='stretch',
    )])


def navbar_login_header() -> html.Div:
    """
    Example of navbar header grid
    """

    return html.Div([dmc.Grid(
        children=[app_header(APP_TITLE, APP_LOGO), login()],
        justify='space-between',
        align='stretch'
    )])


def navbar_app_pages() -> dmc.GridCol:
    """
    Example of how to create / assemble the navbar for the app specific pages.
    """
    layout_examples_menu = menu(
        label='LAYOUT EXAMPLES',
        icon='ph:layout',
        menu_items=[
            menu_item(
                label='Basic Page',
                href=SIMPLE_PAGE_URL,
                icon='bi:square'
            ),
            menu_item(
                label='Left Aside',
                href=LEFT_ASIDE_PAGE_URL,
                icon='bi:layout-sidebar'
            ),
            menu_item(
                label='Right Aside',
                href=RIGHT_ASIDE_PAGE_URL,
                icon='bi:layout-sidebar-reverse'
            ),
            menu_item(
                label='Left-right Asides',
                href=LEFT_RIGHT_ASIDE_PAGE_URL,
                icon='bi:layout-three-columns',
            ),
        ],
    )

    inputs_example_menu = menu(
        label='INPUTS EXAMPLES',
        icon='clarity:form-line',
        menu_items=[
            menu_item(
                label='Forms',
                href=FORMS_PAGE_URL,
                icon='solar:text-field-linear'
            ),
            menu_item(
                label='Search Bar',
                href=SEARCH_BAR_PAGE_URL,
                icon='basil:search-solid'
            ),
            menu_item(
                label='Data Table',
                href=IN_DATA_TABLE_PAGE_URL,
                icon='uiw:table'
            ),
            menu_item(
                label='Upload Box',
                href=FILE_UPLOAD_PAGE_URL,
                icon='material-symbols:upload',
            ),
        ],
    )

    outputs_example_menu = menu(
        label='OUTPUTS EXAMPLES',
        icon='mdi:graph-box-outline',
        menu_items=[
            menu_item(label='Reports',
                      href=REPORT_PAGE_URL,
                      icon='gg:notes'),
            menu_item(
                label='Graphs/Dashboards',
                href=DASHBOARD_PAGE_URL,
                icon='ic:round-dashboard',
            ),
            menu_item(
                label='Tabular',
                href=OUT_DATA_TABLE_PAGE_URL,
                icon='ph:table-bold'
            ),
            menu_item(label='Map',
                      href=MAP_PAGE_URL,
                      icon='tabler:map-pin-2'),
        ],
    )

    return dmc.GridCol(
        [
            dmc.Group(
                [
                    navbar_divider(),
                    layout_examples_menu,
                    navbar_divider(),
                    inputs_example_menu,
                    navbar_divider(),
                    outputs_example_menu,
                    navbar_divider(),
                ],
                justify='space-around',
            ),
        ],
        span='auto',
    )


def user_admin_settings(is_admin: bool) -> dmc.GridCol:
    """
    Example of how to create / assemble the navbar for the user/admin specific pages.
    """
    logout_btn = action_item(
        id='logout-button', label='LOGOUT', icon='ic:baseline-logout', href='/'
    )

    doc_btn = action_item(
        id='documentation',
        label='DOCUMENTATION',
        icon='bxs:book',
        href='https://ecosia.com',
        in_new_tab=True,
    )

    admin_menu = menu(
        label='ADMIN',
        icon='eos-icons:admin-outlined',
        menu_items=[
            menu_item(
                label='Add user', href='/create-user', icon='mingcute:user-add-fill'
            ),
            menu_item(
                label='Edit database', href='http://127.0.0.1:8021/admin/login',
                icon='octicon:database-16'
            ),
        ],
    )

    return dmc.GridCol(
        [
            dmc.Group(
                [
                    admin_menu if is_admin else None,
                    navbar_divider(),
                    doc_btn,
                    navbar_divider(),
                    logout_btn,
                ],
                justify='flex-end',
                style={'margin-right': '20px'},
            ),
        ],
        span='auto',
    )
