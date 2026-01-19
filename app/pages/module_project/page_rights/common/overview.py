"""
This module renders the project rights management page.
"""
import dash_mantine_components as dmc
from ecodev_front import Module
from sqlmodel import Session

from app.pages.module_project.page_rights.add_user_modal.add_user_modal import ADD_USERS_MODAL
from app.pages.module_project.page_rights.common.buttons import delete_project_button
from app.pages.module_project.page_rights.common.buttons import manage_rights_button
from app.pages.module_project.page_rights.common.remove_user_modal import REMOVE_USER_MODAL
from app.pages.module_project.page_rights.common.table import manage_rights_table


def manage_rights_overview(project_id: int, modules: list[Module], session: Session) -> dmc.Stack:
    """
    Renders a table with all the existing users of the project
    """
    return dmc.Stack([
        manage_rights_table(project_id, modules, session),
        manage_rights_button(),
        ADD_USERS_MODAL,
        REMOVE_USER_MODAL,
        delete_project_button()
    ], mb=100)
