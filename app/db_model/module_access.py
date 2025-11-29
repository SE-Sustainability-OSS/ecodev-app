"""
Module implementing the module access table, used to register the viewing and editing rights of a
user to the app's modules. Linked to project access id (i.e. user, project and role).

NOTE: This table is mostly used for external users, as internal users are given access to all
modules by default.
"""
from typing import Optional
from typing import TYPE_CHECKING

from ecodev_core import field
from ecodev_core import sfield
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.db_model.project_access import ProjectAccess


class ModuleAccessBase(SQLModel):  # type: ignore
    """
    Module access table, used to register the viewing and editing rights of a user to the app's
    modules.Linked to project access id (i.e. user, project and role).

    Usage: A user can be given viewing rights to a module by linking it to its project_access
    (i.e. creating a table row with the relevant module name and project_access id). To give the
    user editing rights, also update the `edit_rights` to True (defaults to False).

    NOTE: This table is mostly used for external users, as internal users are given access to all
    modules by default.

    Attributes:
        - module_name: the module or page url which will give user viewing rights.
        - has_access: determines if the user has access to the specific module
    """
    module_name: str = sfield()
    has_access: bool = field(default=False)


class ModuleAccess(ModuleAccessBase, table=True):  # type: ignore
    """
    Module access table, used to register the viewing and editing rights of a user to the app's
    modules. Linked to project access id (i.e. user, project and role).

    Usage: A user can be given viewing rights to a module by linking it to its project_access
    (i.e. creating a table row with the relevant module name and project_access id). To give the
    user editing rights, also update the `edit_rights` to True (defaults to False).

    NOTE: This table is mostly used for external users, as internal users are given access to all
    modules by default.

    Attributes:
        - module_name: the module or page url which will give user viewing rights.
        - has_access: determines if the user has access to the specific module
    Relationships:
        - project_access: relationship to the project_access table (i.e. user, project and role)
    """
    __tablename__ = 'module_access'
    id: Optional[int] = Field(default=None, primary_key=True)
    project_access_id: int = sfield(index=True, foreign_key='project_access.id')
    project_access: Optional['ProjectAccess'] = Relationship(back_populates='modules')
