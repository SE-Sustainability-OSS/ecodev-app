"""
Module rendering the app's introductory text
"""
import dash_mantine_components as dmc
from ecodev_front import app_title
from ecodev_front import subtitle

INTRO_TEXT = dmc.Stack([
    app_title('App Template'),
    subtitle('Template for multi-module apps.', ta='center'),
    subtitle(""" It includes, off the shelf, a user and project management module, an internal documentation module,
    as well as dummy configuration and dashboard modules.""", ta='center')
], align='center', gap=0, mb=10)
