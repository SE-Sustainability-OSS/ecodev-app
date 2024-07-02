"""
TODO: To remove - only to test out front components
"""

import dash_mantine_components as dmc
from dash import dcc, dash
from ecodev_front.components import report_value
from app.components import app_footer
from dash import html
from dash_iconify import DashIconify

URL = 'url'
TOKEN = 'token'
NAVBAR = 'navbar-id'
FOOTER = 'footer-id'
LEFT_ASIDE = 'left-aside-id'
RIGHT_ASIDE = 'right-aside-id'

def dash_base_layout(stores: list[tuple[str, str]],
                     colors: dict[str, list[str]] | None = None) -> dmc.MantineProvider:
    """
    Returns a base layout for any Dash application
    """
    return dmc.MantineProvider(
        forceColorScheme='light',
        theme={'colors': colors} if colors else None,
        children=dmc.AppShell([
            dcc.Location(id=URL, refresh=True),
            dcc.Store(id=TOKEN, data={TOKEN: None}, storage_type='local'),
            *[dcc.Store(id=store_id, storage_type=storage_type) 
                for store_id, storage_type in stores],
            dmc.AppShellHeader(id=NAVBAR, children=[], style={'background-color': '#0066A1'}, zIndex=100),
            dmc.AppShellMain(dash.page_container, style={'position':'absolute', 'padding-top':'75px', 'padding-bottom':'75px',
                                                            'background-color': '#f2f2f2', 'width': '100%', 'height':'60%',}),
            dmc.AppShellFooter(id=FOOTER, children=[], zIndex=100)],
        style={'padding-inline': '0px', 'background-color': '#f2f2f2'},
        header={'height': 55},
        footer={'height': 40})
    )

def page_aside(left_aside: html.Div, page_content: html.Div) -> html.Div:
    """
    TODO
    """



def page_left_aside(aside_content: html.Div, page_content: html.Div) -> html.Div:
    """
    TODO
    """
    left_aside = dmc.AppShellNavbar(id='left-aside', children=aside_content, 
                           zIndex=100, 
                           style={'padding-inline': '0px', 'width':'16vw', 'padding':'20px'}, 
                           withBorder=True, visibleFrom='md')
    main_page = dmc.Stack([
        dmc.Group([
            dmc.Space(visibleFrom='md', style={'margin-left':'15vw'}),
            html.Div(page_content, style={'width': '80vw', 'height':'82vh'})
        ]), dmc.Space(h=50)])
    return html.Div([left_aside, main_page])


def page_right_aside(aside_content: html.Div, page_content: html.Div) -> html.Div:
    """
    TODO
    """
    right_aside = dmc.AppShellAside(id='right-aside', children=aside_content, 
                           zIndex=100, 
                           style={'padding-inline': '0px', 'width':'16vw', 'padding':'20px'}, 
                           withBorder=True, visibleFrom='md')
    main_page = dmc.Stack([
        dmc.Group([
            html.Div(page_content, style={'width': '80vw', 'height':'82vh'}),
            dmc.Space(visibleFrom='md', style={'margin-right':'15vw'}),
        ]), dmc.Space(h=50)])
    return html.Div([right_aside, main_page])


def page_left_right_asides(left_aside: html.Div, page_content: html.Div, right_aside: html.Div) -> html.Div:
    """
    TODO
    """
    left_aside = dmc.AppShellNavbar(
        id='left-aside', 
        children=left_aside, 
        zIndex=100, 
        style={'padding-inline': '0px', 'width':'16vw', 'padding':'20px'}, 
        withBorder=True, visibleFrom='md')
    right_aside = dmc.AppShellAside(
        id='right-aside', 
        children=right_aside, 
        zIndex=100, 
        style={'padding-inline': '0px', 'width':'16vw', 'padding':'20px'}, 
        withBorder=True, visibleFrom='md')
    main_page = dmc.Stack([
        dmc.Group([
            dmc.Space(visibleFrom='md', style={'margin-left':'15vw'}),
            html.Div(page_content, style={'width': '65vw', 'height':'82vh'}),
            dmc.Space(visibleFrom='md', style={'margin-right':'15vw'}),
        ]), dmc.Space(h=50)], style={'backgroundColor': '#f2f2f2'})
    return html.Div([left_aside, main_page, right_aside])

    # return dmc.Grid([
    #     dmc.GridCol(span=1.5),
    #     dmc.GridCol(span=1.5, children=left_aside, visibleFrom='md', 
    #                 style={'position':'fixed', 'left': 20, 'display':'flex', 'flex-direction':'column', 'height':'100%'}),
    #     dmc.GridCol(span=0.1, children=dmc.Divider(orientation="vertical", style={'position':'fixed', 'display':'flex', 'flex-direction':'column', 'height':'100%'}), visibleFrom='md', 
    #                 style={'display':'flex','justifyContent':'center', 'max-width':'50px'}),
    #     dmc.GridCol(span=8, children=html.Div([page_content, dmc.Space(h=50)]), style={'height':'85%'}),
    #     dmc.GridCol(span=0.1, children=dmc.Divider(orientation="vertical", style={'position':'fixed', 'display':'flex', 'flex-direction':'column', 'height':'100%'}), visibleFrom='md', 
    #                 style={'display':'flex','justifyContent':'center', 'max-width':'50px'}),
    #     dmc.GridCol(span=1.5, children=right_aside, visibleFrom='md', style={'position':'fixed', 'right':20, 'display':'block', 'flex-direction':'column', 'height':'100%'}),
    #     dmc.GridCol(span=1.5),
    # ], gutter='xs', grow=True, style={'width':'100%', 'height':'100%', 'background-color': '#f2f2f2'})

from ecodev_front.components import vertical_stepper, stepper_step

LEFT_ASIDE_EXAMPLE = dmc.Stack([
    dmc.Space(h=10),
    dmc.Select(label='Entity',
                data=['Group', 'GPNA', 'GP Antilles', 'GParis'],
                value='Group'),
    dmc.Select(label='Year',
                data=['2020', '2021', '2022', '2023', '2024'],
                value='2024'),
    dmc.Space(h=30),
    vertical_stepper(
        id='nav-stepper-id',
        color='ecoact',
        steps=[
            stepper_step(label='Upload', description="Upload your file", icon='material-symbols:upload', href='/'),
            stepper_step(label='Checks', description="Verify inputs", icon='typcn:input-checked', href='/'),
            stepper_step(label='Match', description="Match suppliers in database", icon='mdi:table-search', href='/'),
            stepper_step(label='Configure', description="Configure methodology", icon='gala:settings', href='/'),
            stepper_step(label='Results', description="Download results", icon='material-symbols:download', href='/'),
        ]
    )
])

RIGHT_ASIDE_EXAMPLE = dmc.Stack([
    dmc.Space(h=10),
    report_value('Scope 1', 15_000, 'kgCO2e'),
    report_value('Scope 2', 32_000, 'kgCO2e'),
    dmc.Space(h=30),
    dmc.Text('Scope 3'),
    report_value('Cat 1', 15_000_000, 'kgCO2e'),
    report_value('Cat 2', 15_000_000_000, 'kgCO2e'),
    report_value('Cat 3', 15_000, 'kgCO2e'),
    report_value('Cat 4', 15_000, 'kgCO2e'),
    report_value('Cat 5', 15_000, 'kgCO2e'),
    report_value('Cat 6', 15_000, 'kgCO2e'),
    report_value('Cat 7', 15_000, 'kgCO2e'),
    report_value('Cat 8', 15_000, 'kgCO2e'),
])