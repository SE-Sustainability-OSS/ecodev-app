"""
File implementing the modules and page's navbar callback.
"""
from dash import callback
from dash import Input
from dash import Output
from dash import State
from ecodev_core import engine
from ecodev_core import safe_get_user
from ecodev_front import APPSHELL
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import NAVBAR
from ecodev_front import PATHNAME
from ecodev_front import TOKEN
from ecodev_front import URL
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.db_model.retrievers.access_retrievers import verify_project_module_access
from app.pages.registry import get_modules


@callback(Output(APPSHELL, NAVBAR,),
          Output(NAVBAR, CHILDREN),
          Input(URL, PATHNAME),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA))
def show_navbar(pathname: str, token: dict, project_id: int):
    """
    Callback displaying the main page navbar and aside (if any)
    """
    navbar_width = {'width': 70}

    if not (user := safe_get_user(token)):
        return {'width': 0}, []

    with Session(engine) as session:
        all_modules = get_modules()
        for module in verify_project_module_access(user, project_id, all_modules, session):
            if pathname in [page.url for page in module.pages]:
                active_page = [page.url for page in module.pages].index(pathname)
                return navbar_width, module.render_navbar(pages=module.pages,
                                                          active_page=active_page)
        return {'width': 0}, []
