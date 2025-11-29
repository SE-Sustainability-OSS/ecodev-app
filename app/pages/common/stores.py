"""File containing all stores."""
from dash import dcc

from app.constants import ALERT_STORE
from app.constants import PROJECT_ID_STORE
from app.constants import USER_DELETION_STORE

STORES = [dcc.Store(PROJECT_ID_STORE, 'session'),
          dcc.Store(ALERT_STORE, 'session', data={}),
          dcc.Store(USER_DELETION_STORE, 'session')]
