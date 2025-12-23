from sqlmodel import select
from sqlmodel import Session

from app.db_model.computation import Computation


def get_computation(name: str,
                    project_id: int,
                    session: Session) -> Computation:
    """
    Retrieve a computation based on its name and project_id (project_id can be None if the
    project hasn't been instantiated yet)
    """
    return session.exec(select(Computation).
                        where(Computation.name == name,
                              Computation.project_id == project_id)
                        ).first()
