"""DES API Ability.

This module contains the ``DESAPIAbility`` class, which represents a
user's ability to use the Document Generator Service's APIs.
"""

import logging
import os

import requests

import letterapi.scripts.client as des_client

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

    def fetch_letters_by_ids(self, letter_ids):
        """Fetch and return all letter objects/rows/dicts corresponding to the
        IDs in ``letter_ids`` and return them as a list of dicts.
        """
        ret = []
        for letter_id in letter_ids:
            letter_url = des_client.get_letter_url(
                self.des_client_config, letter_id)
            try:
                resp = requests.get(
                    letter_url,
                    headers=des_client.get_auth_headers(
                        self.des_client_config),)
                resp_json = resp.json()
                resp.raise_for_status()
            except Exception as err:
                logger.warning(
                    f'Failed to fetch letter {letter_id}. Status code:'
                    f' {resp.status_code}. Response JSON: {resp_json}. Error:'
                    f' {err}')
            else:
                ret.append(resp_json)
        return ret

    def deposit_to_bc_mail_inbox(self, report_text, report_file_name):
        """Write the string ``report_text`` to a file named
        ``report_file_name`` in the DES's BC Mail inbox directory. If that
        directory is not accessible to the AUAT tests (i.e., via a shared
        volume), then raise an exception.
        """
        if not self.des_inbox_accessible:
            raise DESAPIAbilityError(
                'Unable to deposit to the DES BC Mail inbox. That directory is'
                ' inaccessible to the AUAT tests.')
        if not os.path.isdir(self.des_inbox_path):
            raise DESAPIAbilityError(
                'Unable to deposit to the DES BC Mail inbox. There is no'
                ' directory at "{self.des_inbox_path}".')
        write_path = os.path.join(self.des_inbox_path, report_file_name)
        with open(write_path, 'w') as fh:
            fh.write(report_text)
