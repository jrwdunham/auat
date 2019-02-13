"""Steps for the "Generate Email Documents" feature."""

import logging
import os
import pprint

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.generate-email-documents-steps')


# Givens
# ------------------------------------------------------------------------------

@given('a DGS instance containing an up-to-date template {template_key},'
       ' including its template dependencies')
def step_impl(context, template_key):
    template = context.tsbc_nc_user.dgs.get_template_from_key(template_key)
    dependencies = context.tsbc_nc_user.dgs.get_template_dependencies(template)
    context.tsbc_nc_user.dgs.upsert_templates([template] + dependencies)


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
            context.scenario.generate_document_response['file_name'],
            doc_processor=context.tsbc_nc_user.dgs.minify_html))
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

AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL_RECIPE = (
    'text/html',
    'ar_op_friendly_reminder_consolidated_email',
    'ar-op-friendly-reminder-consolidated.json')

AR_OP_FINAL_NOTICE_CONSOLIDATED_EMAIL_RECIPE = (
    'text/html',
    'ar_op_final_notice_consolidated_email',
    'ar-op-final-notice-consolidated.json')


def get_total_amount_due_tds(total_amount_due):
    return (
        f'<td colspan=5 style="border: 1px solid #C1C7D0; margin: 0px; padding:'
        f' 0.5em;">Total amount due for all invoices</td> <td style="border:'
        f' 1px solid #C1C7D0; margin: 0px; padding: 0.5em; text-align:'
        f' right;">{total_amount_due}</td>')


def get_notice_title_div(title_text):
    return (
        f'<div style="text-align: center"> <span style="font-size:'
        f' 16px;"><strong> {title_text} </strong></span> <br> </div>')


FEE_DESCRIPTION_TH = (
    '<th style="background-color: #F4F5F7; border: 1px solid #C1C7D0; margin:'
    ' 0px; padding: 0.5em;"><strong>Fee Description</strong></th>')

ACCOUNT_NUMBER_RIGHT_ALIGNED_TD = (
    '<td style="white-space: nowrap; border: none; text-align:'
    ' right; padding: 0.25em 0.25em;"><strong>Account Number:</strong></td>')


# Map 3-tuple recipes for document generation (output_type, template_key,
# context_path) to tuples of "needles" (i.e., substrings) that should be
# found in the haystack that is the generated document.
NEEDLES_BY_RECIPE = {

    AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL_RECIPE:
    (
     # Amounts due get summed correctly
     get_total_amount_due_tds('$3,301.74'),
     # Correct notice title <div>
     get_notice_title_div('FRIENDLY REMINDER OPERATING PERMIT RENEWAL NOTICE'),
     # Fee description column is present in invoices table
     FEE_DESCRIPTION_TH,
     # Account number right-aligned table cell is present
     ACCOUNT_NUMBER_RIGHT_ALIGNED_TD,
    ),

    AR_OP_FINAL_NOTICE_CONSOLIDATED_EMAIL_RECIPE:
    (
     # Amounts due get summed correctly
     get_total_amount_due_tds('$3,300.00'),
     # Correct notice title <div>
     get_notice_title_div('FINAL NOTICE OPERATING PERMIT RENEWAL'),
     # Fee description column is present in invoices table
     FEE_DESCRIPTION_TH,
     # Account number right-aligned table cell is present
     ACCOUNT_NUMBER_RIGHT_ALIGNED_TD,
    ),

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
