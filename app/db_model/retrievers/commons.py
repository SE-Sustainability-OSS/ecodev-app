"""
Contaings common retriever functions
"""
from ecodev_core import AppUser
from ecodev_core import safe_get_user


def get_user(auth: dict | AppUser) -> AppUser:
    """
    Returns either the AppUser or an AppUser from a token
    """
    return auth if isinstance(auth, AppUser) else safe_get_user(auth)
