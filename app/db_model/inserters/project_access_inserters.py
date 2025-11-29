"""
Module containing all project access table insertion and deletion methods.
"""
from ecodev_core import logger_get
from sqlmodel import Session

from app.constants import ROLE
from app.constants import USER
from app.constants import USER_ID
from app.db_model.inserters.app_user_inserters import add_user
from app.db_model.inserters.commons import upsert_dict
from app.db_model.inserters.module_access_inserters import upsert_module_access
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.access_retrievers import retrieve_project_access
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_id

log = logger_get(__name__)


def upsert_project_access(project_id: int,
                          data: dict,
                          modules: list[str],
                          session: Session,
                          ) -> None:
    """
    Checks if the user already exist in the app AppUser database (inserts it if not) and upserts
    access rights
    """
    if not retrieve_user_by_id(data[USER_ID], session):
        add_user(data[USER_ID], data[USER], session)

    project_access = upsert_dict(data, session, ProjectAccess)
    log.info(
        f"""User #{data[USER]} now has {data[ROLE]} access rights
        on project {project_id}""")  # type: ignore[union-attr]
    upsert_module_access(data, modules, project_access, session)

    return None


def delete_project_access(user_id: int,
                          project_id: int,
                          session: Session,
                          ) -> None:
    """
    Deletes the access rights of a user (and associated module accesses) for a given project
    """
    if project_access := retrieve_project_access(user_id, project_id, session):
        for module in project_access.modules:
            session.delete(module)
        session.delete(project_access)
        session.commit()
    return None
