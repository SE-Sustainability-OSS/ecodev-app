"""
Module implementing the project table, which saves the information associated with an app's project.
It has relationships to the many-to-many table project_access and the one-to-many table computation.
"""
from datetime import datetime
from datetime import timezone
from typing import Optional
from typing import TYPE_CHECKING

from ecodev_core import field
from ecodev_core import sfield
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.db_model.computation import Computation
    from app.db_model.project_access import ProjectAccess


class ProjectBase(SQLModel):
    """
      Database table for an app's project.

      Each app can have multiple projects, each with its own set of users, data inputs, and
      computations.

      A project is defined by its name and year.

      Attributes:
        - name: the name of the project
        - description: a short description of the project (optional)
        - year: the year of the project (defaults to the project's creation year)
        - modified_by: Used to keep track of the user who last modified the project.
        - modified_at: Used to keep track of the last modification date of the project.

    """
    name: str | None = sfield(default=None)
    description: str | None = field(default=None)
    year: int = sfield(default_factory=lambda: datetime.now(timezone.utc).year)
    modified_by: Optional[int] = field(index=True, default=None, foreign_key='app_user.id')
    modified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Project(ProjectBase, table=True):
    """
      Database table for an app's project.

      Each app can have multiple projects, each with its own set of users, data inputs, and
      computations.

      A project is defined by its name and year.

      Attributes:
        - name: the name of the project
        - description: a short description of the project (optional)
        - year: the year of the project (defaults to the project's creation year)
        - modified_by: Used to keep track of the user who last modified the project.
        - modified_at: Used to keep track of the last modification date of the project.

      Relationships:
        - users: Link users to the project and to a specific role / permissions.
        - computations: Link to the project's ongoing and completed computations.
    """
    __tablename__ = 'project'
    id: Optional[int] = Field(default=None, primary_key=True)
    users: list['ProjectAccess'] = Relationship(back_populates='project')
    computations: list['Computation'] = Relationship(back_populates='project')


class ProjectCreate(ProjectBase):
    pass


class ProjectPublic(ProjectBase):
    id: int


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    year: int | None = None
