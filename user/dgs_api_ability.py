"""DGS API Ability.

This module contains the ``DGSAPIAbility`` class, which represents a
user's ability to use the Document Generator Service's APIs.
"""

import logging
import os
import time

import htmlmin
import requests
import slate3k as slate
import templateapi.scripts.client as dgs_client
from templateapi.templates import TEMPLATES
from templateapi.tests.utils import TEST_CONTEXT_PATHS
from templateapi.utils import (
    find_extended_parent_ref_name,
    find_includee_ref_names,
)

from . import base


logger = logging.getLogger('tsbc-nc-user.dgs-api')


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

    @staticmethod
    def get_template_from_key(template_key):
        try:
            return [t for t in TEMPLATES if t.key == template_key][0]
        except IndexError:
            raise ValueError(f'Template key "{template_key}" is unknown.')

    def get_template_dependencies(self, template):
        ret = []
        local_dependencies = []
        template_data = template.data
        local_dependencies += list(map(
            self.get_template_from_key,
            filter(None, [find_extended_parent_ref_name(template_data)])))
        local_dependencies += list(map(
            self.get_template_from_key,
            find_includee_ref_names(template_data)))
        for tmplt in local_dependencies:
            ret += self.get_template_dependencies(tmplt)
        return ret + local_dependencies

    def upsert_template(self, template):
        """Upsert template ``template`` into the target DGS instance.
        """
        dgs_client.upsert_templates(
            self.dgs_client_config, templates_=(template,))

    def upsert_templates(self, templates):
        """Upsert templates ``templates`` into the target DGS instance.
        """
        dgs_client.upsert_templates(
            self.dgs_client_config, templates_=templates)

    @staticmethod
    def verify_context_path(context_path):
        if os.path.isfile(context_path):
            return context_path
        try:
            return [p for p in TEST_CONTEXT_PATHS if
                    p.endswith(context_path)][0]
        except IndexError:
            raise ValueError(
                f'Unable to locate context at path "{context_path}".')

    def generate_document(self, template_key, context_path,
                          output_type='text/html'):
        """Generate a document from the template with key ``template_key``
        using the data context at path ``context_path``.
        """
        config = self.dgs_client_config
        config['key'] = template_key
        config['output_type'] = output_type
        context_path = self.verify_context_path(context_path)
        context_str = dgs_client.get_context_str(context_path)
        return dgs_client.issue_generate_and_store_request(config, context_str)

    @staticmethod
    def minify_html(html_str):
        """Rewrite the HTML document at ``html_path`` after minifying it."""
        return htmlmin.minify(html_str)

    def minify_html_file(self, html_path):
        """Rewrite the HTML document at ``html_path`` after minifying it."""
        with open(html_path) as fhi:
            html = fhi.read()
        with open(html_path, 'w') as fho:
            fho.write(self.minify_html(html))

    def get_template_by_key(self, key):
        return dgs_client.get_template_by_key(self.dgs_client_config, key)

    def download_mds_doc_and_write_to_disk(self, doc_url, doc_file_name,
                                           doc_processor=None):
        config = self.dgs_client_config
        config['output_path'] = self.get_write_path_for_fname(doc_file_name)
        dgs_client.download_mds_doc_and_write_to_disk(doc_url, config)
        if doc_processor:  # make local changes to the doc, if processor func supplied
            doc_processor(config['output_path'])
        return config['output_path']

    def get_write_path_for_fname(self, doc_file_name):
        return os.path.join(self.tmp_path, doc_file_name)

    @staticmethod
    def pdf2text(pdf_path):
        if isinstance(pdf_path, (str, bytes)):
            with open(pdf_path, 'rb') as fh:
                return slate.PDF(fh)
        return slate.PDF(pdf_path)

    def pdf2phrases(self, pdf_path):
        """Return a list of the textual "phrases" in the PDF at ``pdf_path``.
        These are snippets of contiguous text, as returned by slate (slate3k),
        with whitespace removed.
        """
        return set(filter(
            None, [phrase.strip() for phrase in
                   self.pdf2text(pdf_path)[0].splitlines()]))
