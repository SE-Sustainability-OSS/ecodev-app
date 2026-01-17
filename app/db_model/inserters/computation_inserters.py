"""
Module containing all Computation table insertion and deletion methods.
"""
from datetime import datetime
from functools import wraps

from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.computation import Computation
from app.db_model.retrievers.computation_retrievers import get_computation

log = logger_get(__name__)


def computation_step(step: str):
    """
    Decorator that adds a computation step status to the database.

    The decorated method must accept the following arguments:
        - project_id (int): ID of the related project.
        - user (AppUser): The user performing the computation.
        - session (sqlmodel.Session): The database session to use.

    Args:
        step (str): Name of the computation step (corresponds to the `computation.name` column).

    Example:
        @computation_step("computation_name")
        def my_method(project_id, user, session, *args, **kwargs):
            # Your computation logic here
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(project_id: int,
                    user: AppUser,
                    session: Session,
                    *args, **kwargs):
            create_update_computation(
                user, step, project_id, False, session
            )
            try:
                result = func(project_id, user, session, *args, **kwargs)
            except Exception:
                create_update_computation(
                    user, step, project_id, True, session, True
                )
                raise
            create_update_computation(user, step, project_id, True, session)
            return result

        return wrapper

    return decorator


def create_update_computation(user: AppUser,
                              name: str,
                              project_id: int,
                              completed: bool,
                              session: Session,
                              failed=False
                              ) -> Computation:
    """
    Creates a computation step, or updates its completed status
    """
    if computation := get_computation(name, project_id, session):
        _update_computation_status(computation, completed, failed)
    else:
        computation = Computation(name=name, project_id=project_id, launched_by=user.id)
        session.add(computation)

    session.commit()

    log.info(f'Computation {name} (for project_id: {project_id}) '
             f'{"completed" if completed else "launched"}!')
    return computation


def _update_computation_status(computation: Computation,
                               completed: bool,
                               failed: bool) -> None:
    """
    Helper function to update an existing computation status,
    between ongoing and completed.
    """
    if completed or failed:
        computation.completed = True
        computation.completed_at = datetime.now()
        computation.failed = failed
        return

    computation.launched = True
    computation.launched_at = datetime.now()
    computation.completed = False
    computation.completed_at = None
