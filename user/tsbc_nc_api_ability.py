"""TSBC NC API Ability.

This module contains the ``TSBCNCAPIAbility`` class, which represents a
user's ability to use TSBC NC's APIs to interact with TSBC NC.
"""

import logging
import os
import time

import requests

from . import base


logger = logging.getLogger('tsbcncuser.api')


class TSBCNCAPIAbilityError(base.TSBCNCUserError):
    pass


class TSBCNCAPIAbility(base.Base):
    """Represents a TSBC NC user's ability to use APIs to interact with the NC
    infrastructure.
    """


def _save_download(request, file_path):
    with open(file_path, 'wb') as f:
        for block in request.iter_content(1024):
            f.write(block)
