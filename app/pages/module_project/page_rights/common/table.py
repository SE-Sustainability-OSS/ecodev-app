from typing import Any

import dash_ag_grid as dag
from ecodev_core import logger_get
from ecodev_core import select_user
from ecodev_front import custom_column_def
from ecodev_front import data_table
from ecodev_front import Module
from ecodev_front.constants import INDEX
from ecodev_front.constants import OPTIONS
from ecodev_front.constants import TYPE
from sqlmodel import Session

from app.constants import ROLE
from app.constants import USER
from app.db_model.retrievers.access_retrievers import retrieve_project_users
from app.db_model.retrievers.access_retrievers import verify_module_access
from app.domain_model import ADMIN_ROLES
from app.domain_model import RESTRICTED_ROLES
from app.domain_model.color_utils import get_color
from app.pages.module_project.page_rights import MANAGE_RIGHTS
from app.pages.module_project.page_rights import TABLE

USER_DEF = custom_column_def(field=USER)
ROLE_DEF = custom_column_def(field=ROLE, editable=True, width=150,
                             cell_editor='agRichSelectCellEditor',
                             cell_editor_params={'function': 'getOptions(params.data.options)'})

log = logger_get(__name__)


def manage_rights_table(project_id: int,
                        modules: list[Module],
                        session: Session) -> dag.AgGrid:
    """
    Return a grid allowing to manage a project user rights
    """
    column_defs = (
        [USER_DEF, ROLE_DEF] +
        [custom_column_def(field=module.name,
                           header_name=f'Module {module.name.capitalize()}',
                           editable=False,
                           cell_renderer='Checkbox',
                           width='100px') | {'wrapHeaderText': True}
         for module in modules] +
        [_dash_ag_grid_button(field='Remove', color=get_color('red.5'), variant='outline')]
    )

    row_data = retrieve_project_users(project_id, session)
    for row in row_data:
        row[OPTIONS] = ADMIN_ROLES if row[ROLE] in ADMIN_ROLES else RESTRICTED_ROLES
        for module in modules:
            row[module.name] = verify_module_access(select_user(row[USER], session), project_id,
                                                    module.name, session)

    return data_table(id={TYPE: MANAGE_RIGHTS, INDEX: TABLE},
                      row_data=row_data,
                      column_defs=column_defs,
                      default_col_def={'editable': False, 'resizable': True},
                      dash_grid_options={'headerHeight': 50, 'rowHeight': 50})


def _dash_ag_grid_button(field: str,
                         color: str,
                         variant='filled'
                         ) -> dict[str, Any]:
    """
    Helper function to display a dmc.Button in Dash AG Grid column
    """
    return {
        'field': field,
        'headerName': '',
        'editable': False,
        'cellRenderer': 'DMC_Button',
        'cellRendererParams': {
            'color': color,
            'variant': variant,
            'radius': 'md',
            'margin': '5px',
            'value': field
        },
    }
