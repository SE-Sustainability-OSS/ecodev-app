"""
Lists the various roles which can be assigned to a user on a project (unlike Permissions which are
assigned to a user across all apps / projects).

These are associated to certain level of permissions (view, edit, invite) but can be customised
on each app, if required.
"""
from enum import Enum
from enum import unique


@unique
class Role(str, Enum):
    """
    OWNER: Project Owner has edit and view rights to all modules of a single project.
    Can invite anyone to the project (internal and external).

    COLLABORATOR: Collaborator typically has view and edit rights to all modules of a project.
    Cannot invite others to the project.

    CLIENT: Client has view and edit rights which can be restricted to specific modules or pages of
    a project. Cannot invite others to join the project.

    VIEWER: View only has view rights which can be restricted to specific modules or pages of
    a project. May required additional code to prevent editing fields of accessible pages.
    Cannot invite others to join the project.
    """
    OWNER = 'Owner'
    COLLABORATOR = 'Collaborator'
    VIEWER = 'Viewer'
    CLIENT = 'Client'


ADMIN_ROLES = [Role.OWNER, Role.COLLABORATOR]
RESTRICTED_ROLES = [Role.CLIENT, Role.VIEWER]
