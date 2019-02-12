"""DGS API Ability.

This module contains the ``DGSAPIAbility`` class, which represents a
user's ability to use TSBC NC's APIs to interact with TSBC NC.
"""

import logging
import os
import time

import requests
import templateapi.scripts.client as dgs_client

from . import base


logger = logging.getLogger('tsbcncuser.api')


class DGSAPIAbilityError(base.TSBCNCUserError):
    pass


class DGSAPIAbility(base.Base):
    """Represents a TSBC NC user's ability to use the DGS API to interact with
    the Document Generator Service.
    def upsert_production(config):
    """

    @property
    def dgs_client_config(self):
        """Return a config dict that the dgs_client functions can use."""
        return {'url': self.dgs_url,
                'token': self.dgs_access_token,
                'verbose': False,}

    def upsert_production_templates(self):
        """Upsert the production templates in the DGS that we are testing."""
        dgs_client.upsert_production(self.dgs_client_config)

    def generate_document(self, template_key, context_path,
                          output_type='text/html'):
        """Generate a document from the template with key ``template_key``
        using the data context at path ``context_path``.
        """
        config = self.dgs_client_config
        config['key'] = template_key
        config['output_type'] = output_type
        context_str = dgs_client.get_context_str(context_path)
        return dgs_client.issue_generate_and_store_request(config, context_str)

    def download_mds_doc_and_write_to_disk(self, doc_url, doc_file_name):
        config = self.dgs_client_config
        config['output_path'] = self.get_write_path_for_fname(doc_file_name)
        dgs_client.download_mds_doc_and_write_to_disk(doc_url, config)
        return config['output_path']

    def get_write_path_for_fname(self, doc_file_name):
        return os.path.join(self.permanent_path, doc_file_name)
