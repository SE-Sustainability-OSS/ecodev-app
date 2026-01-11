"""
File containing the add user modal header.
"""
import dash_mantine_components as dmc
from ecodev_front import subtitle


def add_user_modal_header() -> dmc.Stack:
    """
    Renders a header for the add user modal.
    """
    return dmc.Stack([
        subtitle('Add a new user to the application and set their access rights.', ta='center'),
        dmc.Divider(w='100%')
    ])
