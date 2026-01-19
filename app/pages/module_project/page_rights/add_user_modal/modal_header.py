"""
File containing the add user modal header.
"""
import dash_mantine_components as dmc
from ecodev_core import AppUser
from ecodev_core import Permission
from ecodev_front import subtitle


def add_user_modal_header(user: AppUser) -> dmc.Stack:
    """
    Renders a header for the add user modal, with additional information to external users.
    """
    return dmc.Stack([
        subtitle('It is possible to add multiple users at the same time.', ta='center'),
        guidance_external_user_restriction(user),
        dmc.Divider(w='100%')
    ])


def guidance_external_user_restriction(user: AppUser) -> dmc.Stack | None:
    """
    Renders a guidance for external users.
    """
    if user.permission == Permission.Client:
        return dmc.Stack([
            dmc.Group([
                dmc.Text('Client restriction:', c='red', fw=700),
                subtitle(f"""You may only invite any users the same domain name as yourself
                            (@{user.client})""", ta='center'),
            ], w='100%'),
        ], gap=0, w='100%')
