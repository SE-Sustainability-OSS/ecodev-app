import dash_mantine_components as dmc
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.pages.module_project.page_info import PROJECT_INFO_INPUT


def number_input(id: str | dict, label: str, value: int | float | None) -> dmc.NumberInput:
    """
    Number input component for the project info financial form
    """
    return dmc.NumberInput(
        id={TYPE: PROJECT_INFO_INPUT, INDEX: id},
        label=label,
        value=value,
        hideControls=True,
        allowNegative=False,
        allowDecimal=False,
        thousandSeparator=',',
        rightSection='EUR',
        rightSectionWidth=50,
        placeholder=label,
        debounce=500,
        w=200,
        style={'textAlign': 'left'},
    )
