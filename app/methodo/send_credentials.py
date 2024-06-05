"""
Module implementating the sending (by email) of new user credentials
"""
from ecodev_core import send_email

from app.constants import APP_NAME
from app.db_model import AppUser
from app.domain_model import ProductType


def send_credentials(email: str, user: AppUser, password: str) -> None:
    """
    Send email with credentials to provided email address.
    """

    body = f"""
    <body><p>
    You have received new credentials for {APP_NAME}!
    Remember, best product type is {ProductType.FOOD.name}.
    <br>
    <br>
    Your username: {user.user}<br>
    Your password: {password}<br>
    <br>
    We recommend you save these username and password in your browser.
    <br>
    <br>
    Thanks & Kind regards,<br>
    IT team<br>
    </p></body>"""
    send_email(email, body, f'{APP_NAME} Credentials')
