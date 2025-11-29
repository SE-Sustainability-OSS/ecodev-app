"""
File containing the project general information form
"""
import dash_mantine_components as dmc
from ecodev_core import logger_get
from ecodev_front import INDEX
from ecodev_front import section_title
from ecodev_front import TYPE

from app.constants import DESCRIPTION
from app.constants import NAME
from app.constants import YEAR
from app.db_model.project import Project
from app.pages.module_project.page_info import PROJECT_INFO_INPUT_ID

log = logger_get(__name__)


GENERAL_INFO_HEADER = dmc.Stack([
    section_title('General Information', ta='left', w='100%'),
], w='100%', gap=0, mb=5)


def general_info_section(project: Project | None) -> dmc.Stack:
    """"
    Renders the general info form section
    """
    return dmc.Stack([
        GENERAL_INFO_HEADER,
        dmc.Group([
            _display_project_name(project.name if project else None),
            _display_description_field(project.description if project else None),
            _display_year_field(project.year if project else None)
        ], w='100%', justify='space-between'),
    ], style={'border': '1px solid #cdcdcd', 'borderRadius': '10px'}, p=20, gap='sm', align='center', w='100%')


def _display_project_name(value: str | None = None) -> dmc.TextInput:
    """
    Renders the project name input field
    """
    return dmc.TextInput(
        id={TYPE: PROJECT_INFO_INPUT_ID, INDEX: NAME},
        label='Project Name',
        placeholder='Something recognisable',
        required=True,
        value=value,
        w='20%'
    )


def _display_description_field(value: str) -> dmc.Select:
    """
    Renders the asset organisational unit select
    """
    return dmc.TextInput(
        id={TYPE: PROJECT_INFO_INPUT_ID, INDEX: DESCRIPTION},
        label='Description',
        placeholder='Description',
        value=value,
        w='70%')


def _display_year_field(value: str) -> dmc.Select:
    """
    Renders the asset organisational unit select
    """
    return dmc.NumberInput(
        id={TYPE: PROJECT_INFO_INPUT_ID, INDEX: YEAR},
        label='Year',
        placeholder='Year',
        value=value,
        w='5%')
