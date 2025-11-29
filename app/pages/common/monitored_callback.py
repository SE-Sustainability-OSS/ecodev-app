"""
Module implementing custom callbacks in order to factor monitoring out of the dash callbacks.
"""
import functools

from dash import callback
from ecodev_core import dash_monitor

from app.constants import APP_NAME


def monitored_callback(*args, **kwargs):
    """
    A custom decorator that combines Dash's @callback functionality with automatic monitoring.

    This decorator uses a three-level structure to integrate with Dash's callback system
    while adding custom monitoring logic:

    1. Outermost function (this function): Captures Dash callback arguments (Output, Input).
    2. Middle function (create_monitored_dash_callback): Wraps the user-defined callback function.
    3. Innermost function (execute_monitored_callback): Executes monitoring logic and calls callback

    The three levels are necessary to:
    - Maintain compatibility with Dash's callback system
    - Add custom monitoring behavior
    - Preserve the original callback's functionality

    Args:
        *args: Variable length argument list for Dash callback (e.g., Output, Input).
        **kwargs: Arbitrary keyword arguments for Dash callback.

    Returns:
        function: A decorator that wraps the user's callback function with monitoring logic.
    """
    def create_monitored_dash_callback(func):
        """
        Middle function that wraps the user-defined callback function.

        This level is needed to capture the original function and apply both
        the monitoring logic and Dash's callback decorator.

        Args:
            func (function): The original callback function defined by the user.

        Returns:
            function: The wrapped function with monitoring and Dash callback applied.

        NB: @functools.wraps is there for the following reasons:
         - It ensures that dash_monitor receives the correct function name (func.__name__). MAIN
         - It maintains any docstrings or other metadata that might be important for Dash
         - It helps in scenarios where the callback might be further introspected or manipulated

        """
        @functools.wraps(func)
        def execute_monitored_callback(*func_args, **func_kwargs):
            """
            Innermost function that executes monitoring logic and calls the original callback.

            This wrapper adds the monitoring call before executing the user's callback function.
            It preserves the original function's signature and docstring.

            Use the original function's name for monitoring

            Args:
                *func_args: Variable length argument list for the original callback.
                **func_kwargs: Arbitrary keyword arguments for the original callback.

            Returns:
                The result of the original callback func.

            NB: token HAS to be the first argument of func
            """
            if (token := func_args[0] if func_args else func_kwargs.get('token')) is None:
                raise ValueError('Token not found in callback arguments')
            dash_monitor(func.__name__, token, APP_NAME)
            return func(*func_args, **func_kwargs)

        return callback(*args, **kwargs)(execute_monitored_callback)

    return create_monitored_dash_callback
