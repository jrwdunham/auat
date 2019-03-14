"""Steps for features involving letter delivery."""

from collections import namedtuple
import json
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

@when('a request is made to create a letter in the BC Mail folder that'
      ' references the document in the DES')
def step_impl(context):
    url = utils.internalize_url(
        context.scenario.generate_document_response['url'])
    letter_dict = {
        'file-name': context.scenario.generate_document_response['file_name'],
        'folder': 'BCMail',
        'source-url': url,
        'status': 'not sent',
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


@then('the letter has status "not sent"')
def step_impl(context):
    assert context.scenario.deliver_letter_response[
        'status'] == 'not sent', (
            f'The letter does not have status "not sent".')


@then('the file name of the letter follows the correct BC Mail syntax')
def step_impl(context):
    file_name = context.scenario.deliver_letter_response['file_name']
    letter_id = context.scenario.deliver_letter_response['id']
    try:
        (bcsapi_f, des_id_f, acct_no_f, loc_f, y_f, m_f, d_f,
         ext_f) = file_name.split('.')
    except Exception as err:
        raise AssertionError(f'Failed to parse file name "{file_name}" to a BC'
                             f' Mail compatible format.')
    assert bcsapi_f == 'BCSAPI', (f'The first part of the file name should be'
                                  f' "BCSAPI"; it is "{bcsapi_f}".')
    expected_des_id_f = f'DES{str(letter_id).zfill(12)}'
    assert expected_des_id_f == des_id_f, (
        f'Expected the second field of "{file_name}" to be'
        f' "{expected_des_id_f}"; it was actually "{des_id_f}".')
    context_path = context.scenario.generated_document_params['context_path']
    context_path = context.user.dgs.verify_context_path(context_path)
    with open(context_path, 'rb') as fh:
        context_dict = json.load(fh)
    expected_acct_no_f = context_dict['PERMITHOLDERACCOUNTNUMBER'].zfill(15)
    assert expected_acct_no_f == acct_no_f, (
        f'Expected the third field of "{file_name}" to be'
        f' "{expected_acct_no_f}"; it was actually "{acct_no_f}".')
    expected_loc_f = {'united states': 'U'}.get(
        context_dict.get('PERMITHOLDERCOUNTRY', 'canada').lower(), 'D')
    assert expected_loc_f == loc_f, (
        f'Expected the fourth field of "{file_name}" to be'
        f' "{expected_loc_f}"; it was actually "{loc_f}".')
    assert tuple(map(len, (y_f, m_f, d_f))) == (4, 3, 2), (
        f'Expected the year, month and day fields to have 4, 3, and 2'
        f' characters each, respectively. This was not the case. These fields'
        f' are "{y_f}", "{m_f}", and "{d_f}".')


# Utils
# ------------------------------------------------------------------------------
