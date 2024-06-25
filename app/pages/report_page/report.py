"""
Module implementing components for a report example
"""
import dash_mantine_components as dmc
from ecodev_front.components import background_card
from ecodev_front.components import card_title
from ecodev_front.components import report_value


def get_example_report() -> dmc.Card:
    """
    Components for a report example
    """
    return background_card(
        [
            dmc.Stack(
                [
                    card_title('Example output report', align='center'),
                    dmc.Space(h=5),
                    dmc.Divider(),
                    dmc.Space(h=5),
                    dmc.SimpleGrid(
                        cols=2,
                        children=[
                            report_value('Scope 1', 15_000, 'kgCO2e'),
                            report_value('Scope 2', 32_000, 'kgCO2e'),
                        ],
                    ),
                    dmc.Space(h=5),
                    dmc.Divider(),
                    dmc.Space(h=5),
                    dmc.SimpleGrid(
                        cols=3,
                        children=[
                            report_value('Scope 3 - Cat 1', 15_000_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 2', 15_000_000_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 3', 15_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 4', 15_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 5', 15_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 6', 15_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 7', 15_000, 'kgCO2e'),
                            report_value('Scope 3 - Cat 8', 15_000, 'kgCO2e'),
                        ],
                    ),
                ]
            )
        ]
    )
