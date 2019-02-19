"""ESS API Ability.

This module contains the ``ESSAPIAbility`` class, which represents a
user's ability to use the Email Sending Service's APIs.
"""

import logging
import os
import time

import htmlmin
import requests
import slate3k as slate
import emailapi.scripts.client as ess_client

from user import base


logger = logging.getLogger('tsbc-nc-user.ess-api')



class ESSAPIAbilityError(base.TSBCNCUserError):
    pass


DEFAULT_FROMEMAIL = 'noreply@technicalsafetybc.ca'


class ESSAPIAbility(base.Base):
    """Represents a TSBC NC user's ability to use the ESS API to interact with
    the Document Generator Service.
    def upsert_production(config):
    """

    @property
    def ess_client_config(self):
        """Return a config dict that the ess_client functions can use.
        """
        return {'url': self.ess_url,
                'token': self.ess_access_token,
                'verbose': False,
                'toemail': self.tester_email,
                'fromemail': DEFAULT_FROMEMAIL,}

    def create_and_send_email(self, subject, body):
        ess_config = self.ess_client_config
        ess_config.update({'subject': subject, 'body': body,})
        return ess_client.create_and_send_email(ess_config)
