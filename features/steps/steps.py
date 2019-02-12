"""General-purpose Steps."""

import logging
import os
import pprint
import time

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.steps')


# Givens
# ------------------------------------------------------------------------------

@given('a DGS instance containing the production templates')
def step_impl(context):
    context.tsbc_nc_user.dgs.upsert_production_templates()


# Whens
# ------------------------------------------------------------------------------

@when('a document of type {output_type} is generated from template'
      ' {template_key} using data context {context_path}')
def step_impl(context, output_type, template_key, context_path):
    context.scenario.generated_document_params = {
        'output_type': output_type,
        'template_key': template_key,
        'context_path': context_path,}
    context.scenario.generate_document_response = (
        context.tsbc_nc_user.dgs.generate_document(
            template_key, context_path, output_type=output_type))


# Thens
# ------------------------------------------------------------------------------

@then('the generated document is stored in the MDS')
def step_impl(context):
    context.scenario.downloaded_doc_path = (
        context.tsbc_nc_user.dgs.download_mds_doc_and_write_to_disk(
            context.scenario.generate_document_response['url'],
            context.scenario.generate_document_response['file_name']))
    assert os.path.isfile(context.scenario.downloaded_doc_path), (
        f'Failed to download generated document'
        f' {context.scenario.generate_document_response["file_name"]}'
        f' from url'
        f' {context.scenario.generate_document_response["url"]}.'
        f' There is no file at the expected download path'
        f' {context.scenario.downloaded_doc_path}.')


@then('the generated document is rendered correctly')
def step_impl(context):
    recipe = (
        context.scenario.generated_document_params['output_type'],
        context.scenario.generated_document_params['template_key'],
        context.scenario.generated_document_params['context_path'],)
    validate_document_generation(
        recipe,
        context.scenario.downloaded_doc_path)


# Utils
# ------------------------------------------------------------------------------

# Map 3-tuple recipes for document generation (output_type, template_key,
# context_path) to tuples of "needles" (i.e., substrings) that should be
# found in the haystack that is the generated document.
NEEDLES_BY_RECIPE = {
    ('text/html',
     'ar_op_friendly_reminder_consolidated_email',
     'etc/test_contexts/ar-op-friendly-reminder-consolidated.json',):
    ('>$3,301.74<',)
}


def validate_document_generation(recipe, generated_doc_path):
    """Validate the document generated using the DGS and 3-tuple
    ``recipe`` and downloaded to ``generated_doc_path``.
    """
    try:
        needles = NEEDLES_BY_RECIPE[recipe]
    except KeyError:
        raise AssertionError(
            f'Unable to validate generated document at'
            f' {generated_doc_path}.'
            f' The recipe {pprint.pformat(recipe)}'
            f' corresponds to no needles.')
    with open(generated_doc_path) as fh:
        haystack = fh.read()
        for needle in needles:
            assert needle in haystack, (
                f'Contrary to expectation, substring "{needle}" is not in the'
                f' file {generated_doc_path}')
