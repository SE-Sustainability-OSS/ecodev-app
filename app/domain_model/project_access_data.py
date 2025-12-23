"""
Domain model for project access data transfer object.
"""
from pydantic import BaseModel
from pydantic import Field

from app.domain_model.app_modules import AppModule
from app.domain_model.role import Role


class ProjectAccessData(BaseModel):
    """
    Data transfer object for upserting project access rights.

    Attributes:
        user_id: The user's ID
        user: The user's email/username
        role: The user's role on the project
        project_id: The project ID
        module_access: Dict mapping modules to access boolean
    """
    user_id: int | None = None
    role: Role
    project_id: int
    module_access: dict[AppModule, bool] = Field(
        default_factory=lambda: {module.value: False for module in AppModule}
    )
