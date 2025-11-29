"""
Module including the background card to either load or create new project
"""
import dash_mantine_components as dmc
from dash import callback
from dash import Input
from dash import Output
from dash_iconify import DashIconify
from ecodev_core import logger_get
from ecodev_front import background_card
from ecodev_front import card_title
from ecodev_front import DATA
from ecodev_front import INDEX
from ecodev_front import TYPE
from ecodev_front import VALUE
from ecodev_front.ids import MODULE_BUTTON
from sqlmodel import Session

from app.constants import APP_NAME
from app.constants import PROJECT_ID_STORE
from app.db_model.project import Project
from app.db_model.retrievers.project_retrievers import retrieve_user_projects
from app.pages.page_main.project_options import NEW_PROJECT_BUTTON_ID
from app.pages.page_main.project_options import PROJECT_SELECT_ID


log = logger_get(__name__)


NEW_PROJECT_BUTTON = dmc.Group([
    dmc.Button(
        'Create New Project',
        id={TYPE: MODULE_BUTTON, INDEX: NEW_PROJECT_BUTTON_ID},
        color='blue',
        leftSection=DashIconify(icon='mdi:chevron-left', width=28),
        size='md', w='30%', style={'flex': '1'},
    ),
    dmc.Divider(orientation='vertical', size=1, mr=10),
])


def project_loader(token: dict, project_id: int | None, session: Session) -> dmc.Container:
    """
    Displays the project create / select component
    """
    project_select_data = [{VALUE: str(project.id), 'label': _create_project_label(project)}
                           for project in retrieve_user_projects(token, session)]

    return dmc.Container([background_card([
        card_title(f'{APP_NAME} | Project Loader', background_color='blue.6'),
        dmc.Group([
            NEW_PROJECT_BUTTON,
            project_select(project_select_data, project_id),
        ], mt=10),
    ])
    ], w='80%')


def _create_project_label(project: Project) -> str:
    """
    Helper function to extract the project label to be rendered in a dmc.Select
    """
    label = f'{project.client} | '
    label += f'{project.name} | ' if project.name else ''
    label += f'{project.year} | '
    label += f'{project.description}' if project.description else ''
    return label


def project_select(data: list[dict[str, str]], project_id: int | None) -> dmc.Stack:
    """
    Renders the project select button.
    Data provided corresponds to the client's list of projects
    """
    return dmc.Select(id=PROJECT_SELECT_ID,
                      placeholder='Select an existing project',
                      data=data,
                      value=project_id,
                      searchable=True,
                      checkIconPosition='right',
                      size='md',
                      allowDeselect=False,
                      nothingFoundMessage='Nothing found...',
                      maxDropdownHeight=200,
                      comboboxProps={'dropdownPadding': 10,
                                     'shadow': 'md'},
                      style={'flex': '1'},)


@callback(Output(PROJECT_ID_STORE, DATA, allow_duplicate=True),
          Input(PROJECT_SELECT_ID, VALUE),
          prevent_initial_call=True)
def update_project_id(project_id: str) -> str:
    """
    Store the selected project id in a store for use in other pages
    """
    return project_id
