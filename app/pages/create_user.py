"""
Module implementing the user creation page.
"""
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import register_page
from ecodev_core import logger_get
from ecodev_front import TOKEN

from app.components import USER_COMPONENTS
from app.components.page_helpers import generic_page

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
    return generic_page(token, USER_COMPONENTS, admin=True)
