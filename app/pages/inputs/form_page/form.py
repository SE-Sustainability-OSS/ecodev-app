"""
Module implementing components for a form example
"""
import dash_mantine_components as dmc
from ecodev_front import background_card
from ecodev_front import card_title

from app.constants import COLORS_ID


def get_example_form() -> dmc.Card:
    """
    Components for a form example
    """
    return background_card(
        [
            dmc.Stack(
                [
                    card_title('Example input form', align='left'),
                    dmc.SimpleGrid(
                        cols=3,
                        children=[
                            dmc.TextInput(label='Input text'),
                            dmc.Select(label='Input select'),
                            dmc.MultiSelect(label='Input multi-select'),
                        ],
                        style={'text-align': 'left'},
                    ),
                    dmc.Button('Submit', color=COLORS_ID),
                ]
            )
        ]
    )
