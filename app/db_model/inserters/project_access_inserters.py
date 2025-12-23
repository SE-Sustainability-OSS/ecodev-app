"""
Module containing all project access table insertion and deletion methods.
"""
from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.constants import MODULE_ACCESS
from app.db_model.inserters.commons import upsert_dict
from app.db_model.inserters.module_access_inserters import upsert_module_access
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.access_retrievers import get_project_access
from app.domain_model import ProjectAccessData

log = logger_get(__name__)


def upsert_project_access(project_id: int,
                          access_data: ProjectAccessData,
                          session: Session,
                          ) -> None:
    """
    Creates mew / Updates project access record and upserts the module access rights.
    """
    project_access = upsert_dict(
        ProjectAccess,
        access_data.model_dump(exclude_unset=True, exclude={MODULE_ACCESS}),
        session
    )
    log.info(f"""User #{access_data.user_id} now has {access_data.role} access
             rights on project {project_id}""")
    upsert_module_access(access_data.module_access, project_access, session)
    return None


def delete_project_access(user: AppUser,
                          project_id: int,
                          session: Session,
                          ) -> None:
    """
    Deletes the access rights of a user (and associated module accesses) for a given project
    """
    if project_access := get_project_access(user, project_id, session):
        for module in project_access.modules:
            session.delete(module)
        session.delete(project_access)
        session.commit()
    return None
