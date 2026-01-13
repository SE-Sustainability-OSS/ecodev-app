"""
Custom Callback Module

This module provides a custom Dash callback decorator that extends the standard
@callback functionality with additional security, monitoring, and computation tracking features.

Key Features:
- Project access verification to ensure users can only access authorized projects
- Computation tracking for long-running operations with status updates

Requirements:
- token and project_id must be provided as keyword arguments, unless check_access is False.
  In that case, the token must still be provided as the first callback argument.
"""
import functools
from typing import Any
from typing import Callable

from dash import callback
from dash.exceptions import PreventUpdate
from ecodev_core import dash_monitor
from ecodev_core import engine
from ecodev_core import log_critical
from ecodev_core import logger_get
from ecodev_core import SETTINGS
from ecodev_front import TOKEN
from sqlmodel import Session

from app.constants import CHECK_ACCESS
from app.constants import COMPUTATION
from app.constants import MONITOR_DETAILS
from app.constants import MONITORING
from app.constants import PROJECT
from app.db_model.inserters.computation_inserters import create_update_computation
from app.db_model.retrievers.project_retrievers import verify_project_access


log = logger_get(__name__)


def safe_callback(*args: Any,
                  **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A custom decorator that combines Dash's @callback functionality with additional functionalities:
    - access (bool):
        Checks for project access. This is to prevent retrieval of project data to be done without
        permission. True by default.
    - computation (str):
        Creates a computation step for this callback run, if computation name (str) is
        provided. None by default.
    - monitoring (bool):
        Creates a monitoring log in db every time this callback is activated.
        False by default.
    - monitor_details (str):
        Additional monitoring log details to pass to the db logger.
        None by default.
    - project (SQLModelMetaclass):
        Project model class to use for access verification.
        ProjectBase by default.

    NOTE: User TOKEN and the project ID must be the first two args of this callback.

    NOTE: This decorator uses a three-level structure to integrate with Dash's callback system
    while adding custom access check logic:
    1. Outermost function (this function): Captures Dash callback arguments (Output, Input).
    2. Middle function (create_custom_dash_callback): Wraps the user-defined callback function.
    3. Innermost function (execute_custom_callback): Executes monitoring logic and calls callback
    The three levels are necessary to:
    - Maintain compatibility with Dash's callback system
    - Add custom access check behavior
    - Preserve the original callback's functionality
    Args:
        *args: Variable length argument list for Dash callback (e.g., Output, Input).
        **kwargs: Arbitrary keyword arguments for Dash callback.
    Returns:
        function: A decorator that wraps the user's callback function with monitoring logic.

    NOTE: Must remove our custom kwargs from the list of kwargs that would be provided to Dash,
    else this results in a TypeError: custom_callback() got multiple values for argument ...
    """
    check_access = kwargs.pop(CHECK_ACCESS, True)
    computation = kwargs.pop(COMPUTATION, None)
    monitoring = kwargs.pop(MONITORING, False)
    monito_details = kwargs.pop(MONITOR_DETAILS, None)
    kwargs.pop(PROJECT, None)

    def create_custom_dash_callback(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Middle function that wraps the user-defined callback function.
        This level is needed to capture the original function and apply both
        the project access logic and Dash's callback decorator.
        Args:
            func (function): The original callback function defined by the user.
        Returns:
            function: The wrapped function with project check and Dash callback applied.
        NB: @functools.wraps is there for the following reasons:
         - It ensures that receives the correct function name (func.__name__). MAIN
         - It maintains any docstrings or other metadata that might be important for Dash
         - It helps in scenarios where the callback might be further introspected or manipulated
        """
        @functools.wraps(func)
        def execute_custom_callback(*func_args: Any, **func_kwargs: Any) -> Any:
            """
            Innermost function that executes custom logic and calls the original callback.


            This wrapper adds the project access check call before executing the user's callback
            function. It preserves the original function's signature and docstring.
            Args:
                *func_args: Variable length argument list for the original callback.
                **func_kwargs: Arbitrary keyword arguments for the original callback.
            Returns:
                The result of the original callback func.
            NOTE:  User TOKEN and project ID are automatically extracted from
            positional arguments (token as dict with 'access_token', project_id as int).
            """
            try:
                token, project_id = _extract_token_and_project_id(func_args, check_access)

                with Session(engine) as session:
                    if check_access is True or project_id is not None:
                        if not verify_project_access(token, int(project_id), session):
                            raise ValueError('User does not have access to the requested project')

                    if monitoring:
                        dash_monitor(func.__name__, token, SETTINGS.app_name, monito_details)

                    if computation and project_id:
                        return _execute_with_computation_tracking(
                            func, func_args, func_kwargs, token, computation, project_id, session
                        )

                    return func(*func_args, **func_kwargs)
            except PreventUpdate:
                # PreventUpdate is a normal Dash control flow, not an error
                raise
            except Exception as e:
                log_critical(f'Error in func: {func.__name__}: {e}', log)
                raise e

        return callback(*args, **kwargs)(execute_custom_callback)
    return create_custom_dash_callback


def _execute_with_computation_tracking(
    func: Callable[..., Any],
    func_args: tuple[Any, ...],
    func_kwargs: dict[str, Any],
    token: dict[str, Any],
    computation: str,
    project_id: int,
    session: Session
) -> Any:
    """
    Execute a callback function with computation tracking.

    This function handles the computation lifecycle:
    1. Creates a computation step with 'launched' status
    2. Executes the callback function
    3. Marks computation as completed on success
    4. Marks computation as failed on exception

    Args:
        func: The callback function to execute
        func_args: Positional arguments for the callback
        func_kwargs: Keyword arguments for the callback
        token: User authentication token
        computation: Computation name/identifier
        project_id: Project ID for the computation
        session: Database session for computation tracking

    Returns:
        The result of the callback function

    Raises:
        Exception: Re-raises any exception from the callback, after marking computation as failed
    """
    create_update_computation(token, computation, project_id, False, session)

    try:
        result = func(*func_args, **func_kwargs)
        create_update_computation(token, computation, project_id, True, session)
        return result
    except Exception as e:
        with Session(engine) as failed_session:
            create_update_computation(token, computation, project_id,
                                      True, failed_session, failed=True)
        raise e


def _extract_token_and_project_id(func_args: tuple[Any, ...],
                                  check_access: bool) -> tuple[dict[str, Any], int | None]:
    """
    Extract token and project_id from callback positional arguments.

    Args:
        func_args: Positional arguments from the callback

    Returns:
        tuple: (token, project_id)

    Raises:
        ValueError: If token or project_id cannot be found
    """
    if not (token := func_args[0]).get(TOKEN).get('access_token'):
        raise ValueError(
            '''Token not found in callback arguments.
            Token should be a dict with "access_token" key''')

    project_id = None
    if check_access and not (project_id := int(func_args[1])):
        raise ValueError(
            'Project ID not found in callback arguments. Project ID should be an integer ')

    return token, project_id
