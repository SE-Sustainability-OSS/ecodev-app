"""
Module implementing the project table, linking a user to a project and a role / permission
"""
from typing import Optional
from typing import TYPE_CHECKING

from ecodev_core import field
from ecodev_core import sfield
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from app.domain_model.role import Role

if TYPE_CHECKING:
    from app.db_model.project import Project
    from app.db_model.module_access import ModuleAccess


class ProjectAccessBase(SQLModel):
    """
    Project access relationship table, linking a user to a project and a role / permission

    Attributes:
        - role: the role / permission the user has in the project.
        Defaults to the lowest permission level (VIEWER).
    """
    role: Role = field(index=True, default=Role.VIEWER)


class ProjectAccess(ProjectAccessBase, table=True):  # type: ignore
    """
    Project access relationship table, linking a user to a project and a role / permission

     Attributes:
        - role: the role / permission the user has in the project.
        Defaults to the lowest permission level (VIEWER).

    Relationships:
        - project: relationship to the project table
        - user_id: references the user-id of the AppUser table (no back_populates)
        - modules: relationship to the module_access table
    """
    __tablename__ = 'project_access'
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = sfield(index=True, foreign_key='project.id')
    project: Optional['Project'] = Relationship(back_populates='users')
    user_id: int = sfield(index=True, foreign_key='app_user.id')
    modules: list['ModuleAccess'] = Relationship(back_populates='project_access')
