import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate
from ecodev_front import BUTTON
from ecodev_front import INDEX
from ecodev_front import MODAL
from ecodev_front import Module
from ecodev_front import N_CLICKS
from ecodev_front import OPENED
from ecodev_front import TYPE
from sqlmodel import Session

from app.pages.pages_account.page_manage_user import ADD_USER
from app.pages.pages_account.page_manage_user import ADD_USER_MODAL_CANCEL
from app.pages.pages_account.page_manage_user.add_user_modal.field_client import client_field
from app.pages.pages_account.page_manage_user.add_user_modal.field_email import email_field
from app.pages.pages_account.page_manage_user.add_user_modal.field_modules import module_access_field
from app.pages.pages_account.page_manage_user.add_user_modal.field_permission import permission_field
from app.pages.pages_account.page_manage_user.add_user_modal.modal_buttons import MODAL_BUTTONS
from app.pages.pages_account.page_manage_user.add_user_modal.modal_header import add_user_modal_header


ADD_USER_MODAL = dmc.Modal(
    id={TYPE: MODAL, INDEX: ADD_USER},
    size='80%', closeOnClickOutside=False,
)


def manage_users_modal(modules: list[Module], session: Session) -> dmc.Stack:
    """
    Renders the add user modal
    """
    return dmc.Stack([
        add_user_modal_header(),
        email_field(),
        permission_field(),
        client_field(session),
        module_access_field(modules),
        MODAL_BUTTONS
    ], align='center', gap='lg', w='100%', justify='center', mt=10, mb=20)


@callback(Output({TYPE: MODAL, INDEX: ADD_USER}, OPENED, allow_duplicate=True),
          Input({TYPE: BUTTON, INDEX: ADD_USER_MODAL_CANCEL}, N_CLICKS),
          prevent_initial_call=True)
def close_add_user_modal(n_clicks: int) -> bool:
    """
    Closes the add new user modal, if the cancel button is clicked
    """
    if not n_clicks:
        raise PreventUpdate
    return False
