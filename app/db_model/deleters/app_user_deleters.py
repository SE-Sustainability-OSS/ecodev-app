"""
Module containing all app user deletion methods.
"""
from ecodev_core import AppRight
from ecodev_core import AppUser
from sqlmodel import select
from sqlmodel import Session

from app.db_model import ModuleAccess
from app.db_model import ProjectAccess


def delete_user(user: AppUser, session: Session) -> None:
    """
    Deletes a user from the AppUser table and all associated entries:
    - AppRight entries (app-wide module access)
    - ProjectAccess entries (project-specific access)
    - ModuleAccess entries (project-specific module access)
    """
    project_accesses = session.exec(
        select(ProjectAccess).where(ProjectAccess.user_id == user.id)
    ).all()

    for project_access in project_accesses:
        module_accesses = session.exec(
            select(ModuleAccess).where(ModuleAccess.project_access_id == project_access.id)
        ).all()
        for module_access in module_accesses:
            session.delete(module_access)
        session.delete(project_access)

    app_rights = session.exec(select(AppRight).where(AppRight.user_id == user.id)).all()
    for app_right in app_rights:
        session.delete(app_right)

    session.delete(user)
    session.commit()
