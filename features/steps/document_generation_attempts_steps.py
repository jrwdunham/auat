"""Steps for features attempts to generate documents."""

from collections import namedtuple
import logging
import os
import pprint

from behave import when, then, given, use_step_matcher

from features.steps.utils import Recipe


logger = logging.getLogger('tsbc-nc-auat.document-generation-attempts-steps')


# Givens
# ------------------------------------------------------------------------------


# Whens
# ------------------------------------------------------------------------------

@when('an attempt is made to generate a document of type {output_type} from'
      ' template {template_key} using data context {context_path}')
def step_impl(context, output_type, template_key, context_path):
    context.scenario.generated_document_params = {
        'output_type': output_type,
        'template_key': template_key,
        'context_path': context_path,}
    resp = context.user.dgs.generate_document_get_resp(
        template_key, context_path, output_type=output_type)
    try:
        context.scenario.generate_document_response = resp.json()
    except:
        context.scenario.generate_document_response = {}
    context.scenario.generate_document_status_code = resp.status_code


# Thens
# ------------------------------------------------------------------------------

@then('the document generation attempt fails')
def step_impl(context):
    assert context.scenario.generate_document_status_code == 400, (
        f'Expected {context.scenario.generate_document_status_code} to be 400.')
    attempt_url = context.scenario.generate_document_response.get(
        'document_generation_attempt_url')
    assert attempt_url, (
        f'Failed to locate a document generation attempt URL in this response:'
        f' {context.scenario.generate_document_response}')


@then('the document generation attempt is correctly recorded')
def step_impl(context):
    attempt_url = context.scenario.generate_document_response.get(
        'document_generation_attempt_url')
    resp = context.user.dgs.fetch(attempt_url)
    resp_json = resp.json()
    assert resp_json['succeeded'] is False
    recipe = Recipe(
        template=context.scenario.generated_document_params['template_key'],
        context=context.scenario.generated_document_params['context_path'],
        otype=context.scenario.generated_document_params['output_type'],)
    validate_failed_document_generation_attempt(recipe, resp_json)


# Utils
# ------------------------------------------------------------------------------

def error_message_contains(error_msg_substr):
    def f(resp_json):
        error_msg = resp_json.get('error', 'no error attribute')
        if error_msg_substr not in error_msg:
            return (f'Failed to find substring "{error_msg_substr}" in the'
                    f' value of the response error attribute "{error_msg}".')
    return f


# Map 3-tuple recipes for document generation (template_key, context_path,
# output_type) to tuples of "validators", functions that expect the document
# generation attempt JSON response as their sole argument.
VALIDATORS_BY_RECIPE = {

    Recipe(  # for Friendly Reminder
        template='ar_op_friendly_reminder_consolidated_email',
        context='error.json',
        otype='text/html',):

    (
        error_message_contains(
            'The referenced template contains variables that are not present in'
            ' the supplied template context.'),
    ),

    Recipe(
        template='ar_op_friendly_reminder_consolidated_email',
        context='error.json',
        otype='bad/type',):

    (
        error_message_contains('"bad/type" is not a valid choice.'),
    ),

}


def validate_failed_document_generation_attempt(recipe, resp_json):
    try:
        validators = VALIDATORS_BY_RECIPE[recipe]
    except KeyError:
        raise AssertionError(
            f'Unable to validate generation attempt response'
            f' {resp_json}.'
            f' The recipe {pprint.pformat(recipe)}'
            f' corresponds to no validators.')
    for validator in validators:
        error = validator(resp_json)
        if error:
            raise AssertionError(
                f'Contrary to expectation, "{error}". Error generated when'
                f' validating document generation attempt')
