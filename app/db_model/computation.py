"""
Computation table, used to register the app's computations launches and completion.
"""
from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import TYPE_CHECKING

from ecodev_core import field
from ecodev_core import sfield
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.db_model.project import Project


class ComputationBase(SQLModel):  # type: ignore
    """
    Computation table, used to register the app's computations launches and completion.
    Attributes:
        - name: the name of the computation. The main indexation attribute when updating.
        - launched: boolean flag triggered when the computation is launched. Defaults to True
        - launched_at: datetime of computation launch
        - computed: boolean flag triggered when the computation is completed. Defaults to False
        - completed_at: datetime of computation completion
        - failed: computation failed
    """
    name: str = sfield(index=True)

    launched: bool = sfield(default=True)
    launched_at: datetime = field(default_factory=lambda: datetime.now())

    completed: bool = sfield(default=False)
    completed_at: datetime | None = field(default=None)

    failed: bool | None = field(default=None)


class Computation(ComputationBase, table=True):  # type: ignore
    """
    Computation table, used to register the app's computations launches and completion.
    Attributes:
        - name: the name of the computation. The main indexation attribute when updating.
        - launched: boolean flag triggered when the computation is launched. Defaults to True
        - launched_at: datetime of computation launch
        - computed: boolean flag triggered when the computation is completed. Defaults to False
        - completed_at: datetime of computation completion
        - failed: computation failed
    Relationships:
        - project: relationship to the project table
        - launched_by: the user which last launched the computation

    """
    __tablename__ = 'computation'
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = sfield(index=True, foreign_key='project.id')
    project: Optional['Project'] = Relationship(back_populates='computations')
    launched_by: Optional[int] = field(index=True, default=None, foreign_key='app_user.id')

    @property
    def run_time(self) -> timedelta | None:
        """
        Returns the time it has taken for the computation to run
        """
        if not self.launched_at:
            return None
        return (self.completed_at or datetime.now()) - self.launched_at  # type: ignore[operator]
