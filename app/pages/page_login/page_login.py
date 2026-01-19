"""
Module implementing the main page
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from ecodev_core import logger_get
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import login_card
from ecodev_front import Page
from ecodev_front import section_title
from ecodev_front import TOKEN

from app.constants import APP_NAME

log = logger_get(__name__)


PAGE_LOGIN = Page(
    module=__name__,
    name='login',
    icon='hugeicons:login-method',
    title='Login Page',
    description='',
    layout=basic_layout,
)


@callback(Output(PAGE_LOGIN.id, CHILDREN),
          Input(TOKEN, DATA))
def get_login_page(token: dict) -> dmc.Stack:
    """
    Renders main page.
    """
    page = dmc.Stack([
        section_title(f'Welcome to {APP_NAME}'),
        dmc.Text('Please login to access the app.'),
        login_card()
    ], w='100%', align='center')
    return page
