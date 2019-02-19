"""TSBC NC (Non-Compliances) API User (consumer).

This module contains the ``TSBCNCUser`` class, which represents a user
of the TSBC Non-Compliance APIs.
"""

import logging
import os
import pprint
import shlex
import subprocess

from . import dgs_api_ability
from . import ess_api_ability
from . import gmail_client_ability
from . import base
from . import constants as c


logger = logging.getLogger('tsbcncuser')


class TSBCNCUser(base.Base):
    """Represents a TSBC NC user. A TSBC NC user can have
    different abilities, or ways of interacting with the TSBC NC APIs. Using
    composition, this TSBC NC User has the following types of abilities:

        - API abilities (via Requests) accessed through ``self.api``.

    Maybe it will one day have:

        - Browser abilities (via Selenium) accessed through ``self.browser``.
        - SSH abilities (via ssh, scp) accessed through ``self.ssh``.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dgs = dgs_api_ability.DGSAPIAbility(**kwargs)
        self.ess = ess_api_ability.ESSAPIAbility(**kwargs)
        self.gmail = gmail_client_ability.GMailClientAbility(**kwargs)
