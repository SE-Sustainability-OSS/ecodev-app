from sqlmodel import select
from sqlmodel import Session

from app.db_model.computation import Computation


def retrieve_computation(name: str,
                         project_id: int,
                         session: Session) -> Computation | None:
    """
    Retrieve a computation based on its name and project_id (project_id can be None if the
    project hasn't been instantiated yet)
    """

    query = (select(Computation).
             where(Computation.name == name, Computation.project_id == project_id))

    return session.exec(query).first()
