"""DGS API Ability.

This module contains the ``DGSAPIAbility`` class, which represents a
user's ability to use the Document Generator Service's APIs.
"""

import datetime
import json
import logging
import os
import re
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


WHITE_SPACE_PATT = re.compile('\s+')



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

    def generate_document_get_resp(
            self, template_key, context_path, output_type='text/html'):
        config = self.dgs_client_config
        config['key'] = template_key
        config['output_type'] = output_type
        context_path = self.verify_context_path(context_path)
        context_str = dgs_client.get_context_str(context_path)
        generate_and_store_url = dgs_client.get_generate_and_store_by_key_url(
            config, config['key'])
        payload = {'output_type': config['output_type'],
                   'context': context_str}
        return requests.post(
            generate_and_store_url,
            data=payload,
            headers=dgs_client.get_auth_headers(config),)

    def fetch(self, url):
        return requests.get(
            url,
            headers=dgs_client.get_auth_headers(self.dgs_client_config))

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
                return ' '.join(slate.PDF(fh))
        return ' '.join(slate.PDF(pdf_path))

    def pdf2phrases(self, pdf_path):
        """Return a set of the textual "phrases" in the PDF at ``pdf_path``.
        These are snippets of contiguous text, as returned by slate (slate3k),
        with whitespace removed.
        """
        return set(filter(
            None, [phrase.strip() for phrase in
                   self.pdf2text(pdf_path).splitlines()]))

    @staticmethod
    def normalize_all_whitespace(some_text):
        return WHITE_SPACE_PATT.sub(' ', some_text).strip()

    def pdf2normalized_text(self, pdf_path):
        """Return a string of white-space-normalized text extracted from the PDF
        at ``pdf_path``. This is the text extracted by slate (slate3k) with all
        contiguous whitespace blocks replaced with a single space.
        """
        return self.normalize_all_whitespace(self.pdf2text(pdf_path))

    @staticmethod
    def get_email_record_create_context(email_create_template_key,
                                        email_create_context,
                                        send_email_dict):
        """Using the email create key (``email_create_template_key``) and the
        attributes of the send response (``send_email_dict``), return a context
        dict compatible with the "record of email sending" template. That is, a
        dict with all of the create context's keys plus these ones:

            >>> {"COVERLETTERSUBJECTPREFIX": "Record of Sent Email",
            ...  "CONTENTSUBJECTPREFIX": "Content of Sent Email",
            ...  "LETTER_TEMPLATE_KEY": "ar_op_friendly_reminder_consolidated_letter",
            ...  "EMAIL_TOEMAIL": "john@somecompany.com",
            ...  "EMAIL_CC": "",
            ...  "EMAIL_FROMEMAIL": "noreply@technicalsafetybc.ca",
            ...  "EMAIL_SUBJECT": "Friendly Reminder Operating Permit Renewal Invoice Summary",
            ...  "EMAIL_SENT_DATE": "2019-03-12T00:00:00Z",
            ...  "EMAIL_STATUS": "sent",
            ...  "EMAIL_ATTACHMENTS": [],}
        """
        ret = email_create_context.copy()
        ret.update(
            {f'email_{k}'.upper(): v for k, v in send_email_dict.items()})
        ret.update(
            {'COVERLETTERSUBJECTPREFIX': 'Record of Sent Email',
             'CONTENTSUBJECTPREFIX': 'Content of Sent Email',
             'LETTER_TEMPLATE_KEY': email_create_template_key.replace(
                 '_email', '_letter'),
             'EMAIL_SENT_DATE': datetime.datetime.utcnow().isoformat()})
        return ret

    def generate_and_store_email_record(self, send_email_resp,
                                        generated_document_params):
        """Generate and store a record of the sending of an email. The "send
        email" JSON response dict is in ``send_email_resp``; the "generate
        document" request JSON dict is in ``generated_document_params``.
        """
        record_context = self.get_email_record_create_context(
            generated_document_params['template_key'],
            json.loads(
                dgs_client.get_context_str(
                    self.verify_context_path(
                        generated_document_params['context_path']))),
            send_email_resp)
        config = self.dgs_client_config
        config['key'] = 'record_of_sent_email'
        config['output_type'] = 'application/pdf'
        record_context_str = json.dumps(record_context, indent=4)
        return dgs_client.issue_generate_and_store_request(
            config, record_context_str)
