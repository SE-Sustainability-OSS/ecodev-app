"""
Main entry point of the solution.
"""
import uvicorn
from ecodev_core import attempt_to_log
from ecodev_core import AUTH
from ecodev_core import engine
from ecodev_core import get_session
from ecodev_core import JwtAuth
from ecodev_core import Token
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqladmin import Admin

from app.admin import ProductAdmin


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ADMIN GUIDANCE #

# The line below is only necessary if wanting to provide POs with an admin view on the DB
# If not the case, remove it alongside its imports (e.g. sqladmin).

# ADMIN #
admin = Admin(app, engine, authentication_backend=JwtAuth(secret_key=AUTH.secret_key))
admin.add_view(ProductAdmin)
# ROUTE GUIDANCE #

# Add API App routes below via:
# "@app.get/post()"

# If many routes, consider:
#   1. Adding a subdirectory "app/routers" with routers,
#   2. Registering the routers in their files via
#      "<your_router_name> = APIRouter()"
#   3. Importing and adding the routers in this file via:
#      "app.include_router(<your_router_name>)


# ROUTES #
@app.post('/login', response_model=Token)
def login_route(
    user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    """
    Route allowing users to log in.
    """
    return attempt_to_log(user.username, user.password, session)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
