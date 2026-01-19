"""
File containing a module's aside layout.
"""
import dash_mantine_components as dmc
from ecodev_front import section_title
from ecodev_front import subtitle
from sqlmodel import Session

from app.db_model.retrievers.project_retrievers import get_project_by_id


def dashboard_aside_layout(token: dict, project_id: int, session: Session):
    """
    Layout for the module's aside.
    """
    project = get_project_by_id(token, project_id, session)
    return dmc.Stack([
        section_title(f'{project.name.capitalize()} Dashboard', ta='center'),
        subtitle('Aside section', ta='center')
    ], w='100%', mt=10)
