import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate
from ecodev_core import AppUser
from ecodev_front import ALERT
from ecodev_front import BUTTON
from ecodev_front import INDEX
from ecodev_front import MODAL
from ecodev_front import Module
from ecodev_front import N_CLICKS
from ecodev_front import OPENED
from ecodev_front import TYPE
from sqlmodel import Session

from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_CANCEL
from app.pages.module_project.page_rights import ADD_RIGHTS_MODAL_ERROR
from app.pages.module_project.page_rights import ADD_USER_RIGHTS
from app.pages.module_project.page_rights.add_user_modal.field_email import email_field
from app.pages.module_project.page_rights.add_user_modal.field_modules import module_access_field
from app.pages.module_project.page_rights.add_user_modal.modal_buttons import MODAL_BUTTONS
from app.pages.module_project.page_rights.add_user_modal.modal_header import add_user_modal_header


ADD_USERS_MODAL = dmc.Modal(
    id={TYPE: MODAL, INDEX: ADD_USER_RIGHTS},
    size='80%', closeOnClickOutside=False,
)


def manage_rights_modal(user: AppUser, modules: list[Module], session: Session) -> dmc.Stack:
    """
    Renders the add rights modal
    """
    return dmc.Stack([
        add_user_modal_header(user),
        dmc.Box(id={TYPE: ALERT, INDEX: ADD_RIGHTS_MODAL_ERROR}),
        email_field(user, session),
        module_access_field(modules),
        MODAL_BUTTONS
    ], align='center', gap='lg', w='100%', justify='center', mt=10, mb=20)


@callback(Output({TYPE: MODAL, INDEX: ADD_USER_RIGHTS}, OPENED, allow_duplicate=True),
          Input({TYPE: BUTTON, INDEX: ADD_RIGHTS_MODAL_CANCEL}, N_CLICKS),
          prevent_initial_call=True)
def close_add_user_modal(n_clicks: int) -> bool:
    """
    Closes the add new project users modal, if the cancel button is clicked
    """
    if not n_clicks:
        raise PreventUpdate
    return False
