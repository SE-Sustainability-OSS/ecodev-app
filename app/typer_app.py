"""
Module with typer commands
"""
import typer
from ecodev_core import logger_get
from ecodev_core import safe_clt


typer_app = typer.Typer()
log = logger_get(__name__)


@safe_clt
@typer_app.command()
def example_typer_command() -> None:
    """
    Example typer command
    """
    log.info('example typer command')


if __name__ == '__main__':
    typer_app()
