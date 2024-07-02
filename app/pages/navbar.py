"""
Module implementing an example of customisable navbar components.
"""
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from ecodev_front.components import action_item
from ecodev_front.components import app_header
from ecodev_front.components import app_logo
from ecodev_front.components import app_title
from ecodev_front.components import login
from ecodev_front.components import menu_item
# from ecodev_front.components import menu

NAVBAR_DIVIDER = dmc.Divider(className='navbar-divider', orientation='vertical')
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
        style={
            'backgroundColor': '#0066A1',
            'color': 'white',
        },
    )])


def navbar_login_header() -> html.Div:
    """
    Example of navbar header grid
    """

    return html.Div([dmc.Grid(
        children=[app_header(APP_TITLE, APP_LOGO), login()],
        justify='space-between',
        align='stretch',
        style={
            'backgroundColor': '#0066A1',
            'color': 'white',
        },
    )])


def menu(label: str,
         icon: str,
         menu_items: list[dmc.MenuItem],
         icon_color: str = 'white') -> html.Div:
    """
    Component to create a navbar menu.
    The menu items must be created beforehand & passed to this component.
    """
    return html.Div(children=[
        dmc.Menu([
            dmc.MenuTarget(dmc.ActionIcon(
                DashIconify(icon=icon,
                            color=icon_color, width=30),
                size='xl',
                variant='transparent',
                id='action-icon',
                n_clicks=0,
            )),
            dmc.MenuDropdown([dmc.MenuLabel(label.upper(), style={'textAlign': 'center'}),
                              html.Div([item for item in menu_items])
                              ])
        ], offset=9, trigger='hover')
    ], style={'display': 'flex',
              'justifyContent': 'center',
              'alignItems': 'center',
              'textAlign': 'center'})


def navbar_app_pages() -> dmc.GridCol:
    """
    Example of how to create / assemble the navbar for the app specific pages.
    """
    layout_examples_menu = menu(
        label='LAYOUT EXAMPLES',
        icon='ph:layout',
        menu_items=[
            menu_item(
                label='Simple page', href='/layouts/simple', icon='bi:square'
            ),
            menu_item(
                label='Left navbar', href='/layouts/left-aside', icon='bi:layout-sidebar'
            ),
            menu_item(
                label='Right aside', href='/layouts/right-aside', icon='bi:layout-sidebar-reverse'
            ),
            menu_item(
                label='Left-right asides', href='/inputs/left-right-aside', icon='bi:layout-three-columns',
            ),
        ],
    )

    inputs_example_menu = menu(
        label='INPUTS EXAMPLES',
        icon='clarity:form-line',
        menu_items=[
            menu_item(
                label='Forms', href='/inputs/forms', icon='solar:text-field-linear'
            ),
            menu_item(
                label='Search bar', href='/inputs/search-bar', icon='basil:search-solid'
            ),
            menu_item(
                label='Data table', href='/inputs/data-table', icon='uiw:table'
            ),
            menu_item(
                label='Upload box',
                href='/inputs/file-upload',
                icon='material-symbols:upload',
            ),
        ],
    )

    outputs_example_menu = menu(
        label='OUTPUTS EXAMPLES',
        icon='mdi:graph-box-outline',
        menu_items=[
            menu_item(label='Reports', href='/outputs/reports', icon='gg:notes'),
            menu_item(
                label='Graphs/Dashboards',
                href='/outputs/dashboards',
                icon='ic:round-dashboard',
            ),
            menu_item(
                label='Tabular', href='/outputs/data-table', icon='ph:table-bold'
            ),
            menu_item(label='Map', href='/outputs/map', icon='tabler:map-pin-2'),
        ],
    )

    return dmc.GridCol(
        [
            dmc.Group(
                [
                    NAVBAR_DIVIDER,
                    layout_examples_menu,
                    NAVBAR_DIVIDER,
                    inputs_example_menu,
                    NAVBAR_DIVIDER,
                    outputs_example_menu,
                    NAVBAR_DIVIDER,
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
                    NAVBAR_DIVIDER,
                    doc_btn,
                    NAVBAR_DIVIDER,
                    logout_btn,
                ],
                justify='flex-end',
                style={'margin-right': '20px'},
            ),
        ],
        span='auto',
    )
