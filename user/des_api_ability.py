"""DES API Ability.

This module contains the ``DESAPIAbility`` class, which represents a
user's ability to use the Document Generator Service's APIs.
"""

import logging
import os
import time

import letterapi.scripts.client as des_client
import requests

from . import base



logger = logging.getLogger('tsbc-nc-user.des-api')


class DESAPIAbilityError(base.TSBCNCUserError):
    pass


class DESAPIAbility(base.Base):
    """Represents a TSBC NC user's ability to use the DES API to interact with
    the Document Generator Service.
    """

    @property
    def des_client_config(self):
        """Return a config dict that the des_client functions can use."""
        return {'url': self.des_url,
                'token': self.des_access_token,
                'verbose': False,}

    def create_letter(self, letter_dict):
        letter_dict.update(self.des_client_config)
        return des_client.create_letter(letter_dict)
