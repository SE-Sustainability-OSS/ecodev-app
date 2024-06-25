"""
Module implementing the user creation page.

"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front.components import background_card

from app.components import USER_COMPONENTS
from app.components.page_helpers import generic_page
from app.constants import TOKEN


log = logger_get(__name__)

register_page(__name__, path='/create-user')
CREATE_USER_PAGE_ID = 'create-user-page'
layout = [html.Div(id=CREATE_USER_PAGE_ID)]


@callback(Output(CREATE_USER_PAGE_ID,
                 'children'),
          Input(TOKEN, 'data'))
def create_user_page(token: dict):
    """
    User creation page
    """
    page = dmc.Container([background_card(USER_COMPONENTS)])
    return generic_page(token, page, admin=True)
