"""
This module renders the app user management page.
"""
import dash_mantine_components as dmc
from sqlmodel import Session

from app.pages.pages_account.page_manage_user.add_user_modal.add_user_modal import ADD_USER_MODAL
from app.pages.pages_account.page_manage_user.common.remove_user_modal import REMOVE_USER_MODAL
from app.pages.pages_account.page_manage_user.common.table import manage_users_table


def manage_users_overview(session: Session) -> dmc.Stack:
    """
    Renders a table with all the existing app users
    """
    return dmc.Stack([
        manage_users_table(session),
        ADD_USER_MODAL,
        REMOVE_USER_MODAL,
    ], mb=100, w='100%', align='center', justify='center')
