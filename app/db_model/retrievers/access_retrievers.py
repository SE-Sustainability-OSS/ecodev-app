"""
Module containing all retrievers used to check user's access to projects and modules
"""
from ecodev_core import AppRight
from ecodev_core import AppUser
from ecodev_core import Permission
from ecodev_core.list_utils import list_tuple_to_dict
from sqlmodel import col
from sqlmodel import select
from sqlmodel import Session

from app.constants import USER_ID
from app.db_model.module_access import ModuleAccess
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.commons import get_user
from app.db_model.retrievers.project_retrievers import retrieve_project_by_id
from app.domain_model import AppModule
from app.domain_model.role import Role


def retrieve_project_users(project_id: int,
                           session: Session) -> list:
    """
    Returns a list of users that have access to a specific project
    """
    query = (select(ProjectAccess.project_id, AppUser.id.label(USER_ID), AppUser.user,
                    ProjectAccess.role).
             join(AppUser).
             where(ProjectAccess.project_id == project_id))

    return list_tuple_to_dict(session.exec(query).all())


def retrieve_project_access(user_id: int, project_id: int, session: Session
                            ) -> ProjectAccess | None:
    """
    Returns a ProjectAccess linked to a specific user and project_id
    """
    query = select(ProjectAccess).where(ProjectAccess.user_id == user_id,
                                        ProjectAccess.project_id == project_id)
    return session.exec(query).first()


def retrieve_project_role(auth: dict | AppUser,
                          project_id: int,
                          session: Session
                          ) -> Role | None:
    """
    Attempts to retrieve the user's access rights. If not found, it means user does not have access
    to the project. If found, returns role of user in that project.
    """

    return session.exec(select(ProjectAccess.role)
                        .where(ProjectAccess.project_id == project_id,
                               ProjectAccess.user_id == get_user(auth).id)
                        ).first()


def retrieve_license_rights(user: AppUser, session: Session) -> list[AppModule]:
    """
    Retrieves the user's license (list of AppModules) rights.
    """
    if user.permission == Permission.ADMIN:
        return list(AppModule)
    return [AppModule(rights.app_service) for rights in
            session.exec(select(AppRight).where(AppRight.user_id == user.id)).all()]


def get_project_accessible_modules(auth: dict | AppUser,
                                   project_id: int,
                                   modules: list[AppModule],
                                   session: Session,
                                   ) -> list[AppModule]:
    """
    Verifies user has access to the requested module.
    By default, internal staff have access to all of the app's modules.
    """
    if not (user := get_user(auth)):
        return []

    role = retrieve_project_role(user, project_id, session)

    if (project := retrieve_project_by_id(user, project_id, session)):
        return modules

    if user.permission == Permission.ADMIN or role == Role.OWNER:
        return modules

    accessible_modules = retrieve_project_accessible_modules(user, project_id, session)
    return [module for module in modules
            if module.name in [m.module_name for m in accessible_modules]]


def verify_module_access(auth: dict | AppUser,
                         project_id: int,
                         module_name: str,
                         session: Session) -> bool:
    """
    Verifies user has access to the requested module.
    By default, internal staff have access to all of the app's modules.
    """
    if not (user := get_user(auth)):
        return False

    if (user.permission == Permission.ADMIN or
            retrieve_project_role(user, project_id, session) == Role.OWNER):
        return True

    accessible_modules = retrieve_project_accessible_modules(user, project_id, session)
    return True if module_name in [a.module_name for a in accessible_modules] else False


def retrieve_project_accessible_modules(auth: dict | AppUser,
                                        project_id: int,
                                        session: Session) -> list[ModuleAccess]:
    """
    Retrieves all modules the user has access to.

    NOTE: By default, internal staff are granted access to all modules without being recorded
    in the module access table. Therefore this method should only be used with external users (see
    `verify_module_access` method below).
    """
    return list(session.exec(select(ModuleAccess)
                             .join(ProjectAccess)
                             .where(ProjectAccess.user_id == get_user(auth).id,
                                    ProjectAccess.project_id == project_id,
                                    col(ModuleAccess.has_access).is_(True))
                             ).all())
