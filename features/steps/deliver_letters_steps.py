"""Steps for features involving letter delivery."""

from collections import namedtuple
import logging
import os
import pprint
import time
from uuid import uuid4

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.deliver-letters-steps')


# Givens
# ------------------------------------------------------------------------------


# Whens
# ------------------------------------------------------------------------------

@when('a request is made to create a letter that references the document in the'
      ' DES')
def step_impl(context):
    url = utils.internalize_url(
        context.scenario.generate_document_response['url'])
    letter_dict = {
        'file-name': context.scenario.generate_document_response['file_name'],
        'folder': 'BCMail',
        'source-url': url,
        'status': 'not delivered',
    }
    context.scenario.deliver_letter_response = (
        context.user.des.create_letter(letter_dict))


# Thens
# ------------------------------------------------------------------------------

@then('a letter referencing the document is created in the DES')
def step_impl(context):
    assert isinstance(context.scenario.deliver_letter_response['id'], int), (
        f'The deliver letter request to the DES failed: the response did not have'
        f' an id attribute of type int.')


@then('the letter has status "not delivered"')
def step_impl(context):
    assert context.scenario.deliver_letter_response[
        'status'] == 'not delivered', (
            f'The letter does not have status "not delivered".')


# Utils
# ------------------------------------------------------------------------------
