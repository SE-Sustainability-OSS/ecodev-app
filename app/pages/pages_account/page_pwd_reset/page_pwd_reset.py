"""
Module implementing the user password reset page
"""
import dash_mantine_components as dmc
from dash import Input
from dash import Output
from ecodev_front import basic_layout
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import Page
from ecodev_front import page_title
from ecodev_front import TOKEN

from app.pages.common.custom_callback import safe_callback
from app.pages.pages_account.page_pwd_reset.common.reset_pwd_form import RESET_PWD_FORM


PAGE_RESET_PWD = Page(
    module=__name__,
    name='reset-pwd',
    icon='mdi:password-reset',
    title='Reset Password',
    description='',
    layout=basic_layout,
)


@safe_callback(Output(PAGE_RESET_PWD.id, CHILDREN),
               Input(TOKEN, DATA),
               check_access=False)
def create_user_page(token: dict):
    """
    Reset user password page
    """
    return dmc.Stack([
        page_title('Reset your password'),
        RESET_PWD_FORM
    ], w='100%', align='center', justify='center',  mt=20)
