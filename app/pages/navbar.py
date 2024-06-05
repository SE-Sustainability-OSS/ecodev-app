"""
Module implementing an example of customisable navbar components.
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_front import navbar_action_item
from ecodev_front import navbar_header
from ecodev_front import navbar_login
from ecodev_front import navbar_menu
from ecodev_front import navbar_menu_item

NAVBAR_DIVIDER = dmc.Divider(className='navbar-divider', orientation='vertical')


def navbar(is_admin: bool = False) -> html.Div:
    """
    Function which determines the display of the various navbar buttons.
    Only show certain additional buttons to admin users.
    """
    return html.Div([dmc.Grid(
        children=[navbar_header(), navbar_app_pages(), user_admin_settings(is_admin)],
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
        children=[navbar_header(), navbar_login()],
        justify='space-between',
        align='stretch',
        style={
            'backgroundColor': '#0066A1',
            'color': 'white',
        },
    )])


def navbar_app_pages() -> dmc.GridCol:
    """
    Example of how to create / assemble the navbar for the app specific pages.
    """
    inputs_example_menu = navbar_menu(
        label='INPUTS EXAMPLES',
        icon='clarity:form-line',
        menu_items=[
            navbar_menu_item(
                label='Forms', href='/inputs/forms', icon='solar:text-field-linear'
            ),
            navbar_menu_item(
                label='Search bar', href='/inputs/search-bar', icon='basil:search-solid'
            ),
            navbar_menu_item(
                label='Data table', href='/inputs/data-table', icon='uiw:table'
            ),
            navbar_menu_item(
                label='Upload box',
                href='/inputs/file-upload',
                icon='material-symbols:upload',
            ),
        ],
    )

    outputs_example_menu = navbar_menu(
        label='OUTPUTS EXAMPLES',
        icon='mdi:graph-box-outline',
        menu_items=[
            navbar_menu_item(label='Reports', href='/outputs/reports', icon='gg:notes'),
            navbar_menu_item(
                label='Graphs/Dashboards',
                href='/outputs/dashboards',
                icon='ic:round-dashboard',
            ),
            navbar_menu_item(
                label='Tabular', href='/outputs/data-table', icon='ph:table-bold'
            ),
            navbar_menu_item(label='Map', href='/outputs/map', icon='tabler:map-pin-2'),
        ],
    )

    return dmc.GridCol(
        [
            dmc.Group(
                [
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
    logout_btn = navbar_action_item(
        id='logout-button', label='LOGOUT', icon='ic:baseline-logout', href='/'
    )

    doc_btn = navbar_action_item(
        id='documentation',
        label='DOCUMENTATION',
        icon='bxs:book',
        href='https://ecosia.com',
        in_new_tab=True,
    )

    admin_menu = navbar_menu(
        label='ADMIN',
        icon='eos-icons:admin-outlined',
        menu_items=[
            navbar_menu_item(
                label='Add user', href='/create-user', icon='mingcute:user-add-fill'
            ),
            navbar_menu_item(
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
