"""File containing all stores."""
from dash import dcc
from ecodev_front import SESSION_STORE

from app.constants import ALERT_STORE
from app.constants import PROJECT_ID_STORE
from app.constants import USER_DELETION_STORE

STORES = [dcc.Store(PROJECT_ID_STORE, SESSION_STORE),
          dcc.Store(ALERT_STORE, SESSION_STORE, data={}),
          dcc.Store(USER_DELETION_STORE, SESSION_STORE)]
