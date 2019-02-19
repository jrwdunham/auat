"""GMail Client Ability

This module contains the ``GMailClientAbility`` class, which represents a
user's ability to retrieve emails from their GMail account. Note: that most
functionality is in a base class defined in lib/gmail.py.
"""

import logging

from . import base
from .lib.gmail import GMailClient, GMailError

logger = logging.getLogger('tsbc-nc-user.gmail-client')


class GMailClientAbility(base.Base, GMailClient):
    """Represents a TSBC NC user's ability to access emails from a GMail
    account.
    """

    GMailError = GMailError

    def __init__(self, **kwargs):
        base.Base.__init__(self, **kwargs)
        GMailClient.__init__(self, **kwargs)
