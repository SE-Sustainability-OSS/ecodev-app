"""
File containing the client input component for the add user modal.
"""
import dash_mantine_components as dmc
from ecodev_front import INDEX
from ecodev_front import MULTI_SELECT
from ecodev_front import section_title
from ecodev_front import subtext
from ecodev_front import TYPE
from sqlmodel import Session

from app.db_model.retrievers import get_all_clients
from app.pages.pages_account.page_manage_user import USER_CLIENT


def client_field(session: Session) -> dmc.Stack:
    """
    Renders the client field as a tags input with existing clients as suggestions.
    Allows selecting an existing client or entering a new one.
    """
    existing_clients = get_all_clients(session)

    return dmc.Stack([
        section_title('Client organization'),
        subtext('Select an existing client or enter a new one.'),
        dmc.TagsInput(
            id={TYPE: MULTI_SELECT, INDEX: USER_CLIENT},
            placeholder='Enter or select client name',
            data=existing_clients,
            maxTags=1,
            required=True,
            w='100%')
    ], gap=3, w='80%')
