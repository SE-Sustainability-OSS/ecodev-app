"""
Module implementing an example dashboard
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_front import background_card
from ecodev_front import card_title

from app.components.plots.bar_chart import bar_chart
from app.components.plots.heatmap import heat_map
from app.components.plots.pie_chart import pie_chart

CANADA = background_card([card_title('Population Canada'), bar_chart()],
                         style={'width': '40vw', 'height': '40vh'})
EUROPE = background_card([card_title('Population Europe (%)'), pie_chart()],
                         style={'width': '40vw', 'height': '40vh'})
PROD = background_card([card_title('Productivity'), heat_map()],
                       style={'width': '40vw', 'height': '40vh'})
BAR = background_card([card_title('Bar chart'), bar_chart()],
                      style={'width': '40vw', 'height': '40vh'})
PROD2 = background_card([card_title('Productivity'), heat_map()],
                        style={'width': '83vw', 'height': '80vh'})
DASHBOARD = html.Div([dmc.Group([
    dmc.Stack([CANADA, dmc.Space(h='1vh'), EUROPE]),
    dmc.Space(w='1vw'),
    dmc.Stack([PROD, dmc.Space(h='1vh'), BAR])]),
    dmc.Space(h='4vh'), PROD2])
