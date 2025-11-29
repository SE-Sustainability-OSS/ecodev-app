"""
File containing the module access selection component for the add user modal in the page rights.
"""
import dash_mantine_components as dmc
from ecodev_front import label_text
from ecodev_front import Module
from ecodev_front import section_title
from ecodev_front import subtext

from app.pages.module_project.page_rights import MODULE_MULTISELECT_ID


def module_access_field(modules: list[Module]) -> dmc.Stack:
    """
    Renders the module access section of the 'add user modal'.
    """
    data = [{'value': module.name, 'label': module.name.capitalize()} for module in modules]
    return dmc.Stack([
        section_title('Module access'),
        dmc.Stack([
            label_text('Which module should the user be granted access to ?'),
            subtext('Internal users will be granted access to all modules by default')
        ], gap=0),
        dmc.MultiSelect(
            data=data,
            value=[m['value'] for m in data],
            clearable=True,
            id=MODULE_MULTISELECT_ID),
    ], gap=3, w='80%')
