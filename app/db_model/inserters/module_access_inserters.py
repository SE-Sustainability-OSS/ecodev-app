"""
Module containing all module access table insertion and deletion methods.
"""
from ecodev_core import logger_get
from ecodev_front import Module
from sqlmodel import Session

from app.constants import HAS_ACCESS
from app.constants import MODULE_NAME
from app.constants import PROJECT_ACCESS_ID
from app.db_model.inserters.commons import upsert_dict
from app.db_model.module_access import ModuleAccess
from app.db_model.project_access import ProjectAccess

log = logger_get(__name__)


def upsert_module_access(data: dict,
                         modules: list[Module],
                         project_access: ProjectAccess,
                         session: Session
                         ) -> None:
    """
    Upserts module access rights for a given user
    """
    for module in modules:
        upsert_dict({MODULE_NAME: module.name, HAS_ACCESS: data[module.name],
                     PROJECT_ACCESS_ID: project_access.id}, session, ModuleAccess)

    return None
