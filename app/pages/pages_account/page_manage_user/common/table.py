from typing import Any

import dash_ag_grid as dag
from ecodev_core import Permission
from ecodev_front import custom_column_def
from ecodev_front import data_table
from ecodev_front import OPTIONS
from ecodev_front import TABLE
from ecodev_front.constants import INDEX
from ecodev_front.constants import TYPE
from sqlmodel import Session

from app.constants import USER
from app.constants import USER_ID
from app.db_model.retrievers import get_all_users
from app.db_model.retrievers import get_app_rights
from app.domain_model.color_utils import get_color
from app.pages.pages_account.page_manage_user import MANAGE_USERS
from app.pages.registry import get_modules

PERMISSION = 'permission'
USER_DEF = custom_column_def(field=USER)
PERMISSION_DEF = custom_column_def(field=PERMISSION, editable=True, width=150,
                                   cell_editor='agRichSelectCellEditor',
                                   cell_editor_params={'function': 'getOptions(params.data.options)'})


def manage_users_table(session: Session) -> dag.AgGrid:
    """
    Return a grid allowing to manage app user rights
    """
    all_modules = get_modules()
    column_defs = (
        [_dash_ag_grid_button(field='Remove', color=get_color('red.5'), variant='outline')] +
        [USER_DEF, PERMISSION_DEF] +
        [custom_column_def(field=module.name,
                           header_name=f'Module {module.name.capitalize()}',
                           editable=False,
                           cell_renderer='Checkbox',
                           width='100px') | {'wrapHeaderText': True}
         for module in all_modules]
    )

    all_users = get_all_users(session)
    row_data = []
    for user in all_users:

        user_app_rights = get_app_rights(user, session)
        row = {
            USER_ID: user.id,
            USER: user.user,
            PERMISSION: user.permission.capitalize(),
            OPTIONS: [p.capitalize() for p in Permission]
        }
        for module in all_modules:
            row[module.name] = any(right.name == module.name for right in user_app_rights)
        row_data.append(row)

    return data_table(id={TYPE: TABLE, INDEX: MANAGE_USERS},
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
        'width': 75,
        'cellRenderer': 'DMC_Button',
        'cellRendererParams': {
            'color': color,
            'variant': variant,
            'radius': 'md',
            'margin': '5px',
            'value': field
        },
    }
