"""Steps for the "Generate Email Documents" feature."""

from collections import namedtuple
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
    """Using the validators declared in ``VALIDATORS_BY_RECIPE``, validate the
    correct generation of the document.
    """
    recipe = Recipe(
        template=context.scenario.generated_document_params['template_key'],
        context=context.scenario.generated_document_params['context_path'],
        otype=context.scenario.generated_document_params['output_type'],)
    validate_document_generation(
        recipe,
        context.scenario.downloaded_doc_path)


# Utils
# ------------------------------------------------------------------------------

Recipe = namedtuple('Recipe', 'template, context, otype')


FEE_DESCRIPTION_TH = (
    '<th style="background-color: #F4F5F7; border: 1px solid #C1C7D0; margin:'
    ' 0px; padding: 0.5em;"><strong>Fee Description</strong></th>')

ACCOUNT_NUMBER_RIGHT_ALIGNED_TD = (
    '<td style="white-space: nowrap; border: none; text-align:'
    ' right; padding: 0.25em 0.25em;"><strong>Account Number:</strong></td>')


def confirm_total_amount_due_is(total_amount_due):
    def f(document_str):
        if (('>Total amount due for all invoices</td>' not in document_str) or
                (f'>{total_amount_due}</td>' not in document_str)):
            return (f'Failed to find total amount due {total_amount_due} in the'
                    ' document.')
    return f


def confirm_notice_title_is(title_text):
    """Note we allow centered titles with an increased font size and those
    without. This should probably be standardized.
    """

    def f(document_str):
        if  ((f'<div style="text-align: center"> <span style="font-size:'
              f' 16px;"><strong> {title_text} </strong></span> <br> </div>'
              not in document_str) and
             (f'<div style="text-align: center"> <strong>{title_text}</strong>'
              f' </div>') not in document_str):
            return (f'Failed to find expected text "{title_text}" in the'
                    f' document.')
    return f


def confirm_banner_text_is(banner_text):
    def f(document_str):
        if (f'<h3 style="font-size: 18px !important; line-height: 23px'
            f' !important; font-weight: bold !important; margin: 15px 0px'
            f' 10px; color: #FFFFFF; font-family: Arial,'
            f' sans-serif;">{banner_text}</h3></div>') not in document_str:
            return (f'Failed to find expected text "{banner_text}" in the'
                    f' blue banner at the top of the email.')
    return f


def fee_descr_col_is_present():
    def f(document_str):
        if FEE_DESCRIPTION_TH not in document_str:
            return f'Failed to locate a "fee description" table column'
    return f


def fee_descr_col_is_NOT_present():
    return lambda ds: not fee_descr_col_is_present()(ds)


def account_number_invisi_table_is_twice_present():
    def f(document_str):
        prsnc_cnt = document_str.count(ACCOUNT_NUMBER_RIGHT_ALIGNED_TD)
        if prsnc_cnt != 2:
            return (f'The right-aligned borderless "account number" table was'
                    f' found {prsnc_cnt} times. It should have been present 2'
                    f' times.')
    return f


def collection_action_stmnt_removed():
    def f(document_str):
        if ('Failure to forward payment by the expiry date may result in'
            ' collection action') in document_str:
            return (f'The collection action statement was not removed. It'
                    f' should have been removed.')
    return f


def ssgr_s18_italicized_present():
    def f(document_str):
        if (f'<i>Safety Standards General Regulations (SSGR) s. 18</i>'
                ) not in document_str:
            return 'The italicized SSGR s. 18 was not cited.'
    return f


def collection_mention_removed():
    def f(document_str):
        if (('to avoid collection and enforcement actions' in document_str) or
                ('to avoid enforcement actions' not in document_str)):
            return 'The "collection actions" mention was not removed.'
    return f


def invoice_changed_to_notice():
    def f(document_str):
        if ('If you have questions about this notice or your permit(s)'
                ) not in document_str:
            return 'The "this invoice" should have been changed to "this notice".'
    return f


def phone_number_for_payment_added():
    def f(document_str):
        if ('to renew your operating permit or by calling 1 866 566 7233'
                ) not in document_str:
            return ('TSBC\'s phone number was not provided as a payment'
                    ' strategy.')
    return f


# Map 3-tuple recipes for document generation (template_key, context_path,
# output_type) to tuples of "validators", functions that expect the generated
# document as their sole argument.
VALIDATORS_BY_RECIPE = {

    # AR OP CONSOLIDATED NOTICES - START

    Recipe(  # for Friendly Reminder
        template='ar_op_friendly_reminder_consolidated_email',
        context='ar-op-friendly-reminder-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,301.74'),
        confirm_notice_title_is('FRIENDLY REMINDER OPERATING PERMIT RENEWAL NOTICE'),
        fee_descr_col_is_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Past Due
        template='ar_op_past_due_consolidated_email',
        context='ar-op-past-due-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('PAST DUE NOTICE OPERATING PERMIT RENEWAL'),
        fee_descr_col_is_present(),
        account_number_invisi_table_is_twice_present(),
        collection_action_stmnt_removed(),
    ),

    Recipe(  # for Demand
        template='ar_op_demand_consolidated_email',
        context='ar-op-demand-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('DEMAND NOTICE'),
        fee_descr_col_is_present(),
        account_number_invisi_table_is_twice_present(),
        ssgr_s18_italicized_present(),
        collection_mention_removed(),
        invoice_changed_to_notice(),
    ),

    Recipe(  # for Final Warning
        template='ar_op_final_warning_consolidated_email',
        context='ar-op-final-warning-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is(
            'Final Warning Operating Permit Renewal Notice of Non-Compliance'),
        fee_descr_col_is_present(),
        account_number_invisi_table_is_twice_present(),
        invoice_changed_to_notice(),
        phone_number_for_payment_added(),
    ),

    Recipe(  # for Final Notice
        template='ar_op_final_notice_consolidated_email',
        context='ar-op-final-notice-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('FINAL NOTICE OPERATING PERMIT RENEWAL'),
        fee_descr_col_is_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    # AR OP CONSOLIDATED NOTICES - END

    # AR GENERAL CONSOLIDATED NOTICES - START

    Recipe(  # for Past Due
        template='ar_gen_past_due_consolidated_email',
        context='ar-gen-past-due-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('PAST DUE SUMMARY NOTICE'),
        fee_descr_col_is_NOT_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Demand
        template='ar_gen_demand_consolidated_email',
        context='ar-gen-demand-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('DEMAND SUMMARY NOTICE'),
        fee_descr_col_is_NOT_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Final Warning
        template='ar_gen_final_warning_consolidated_email',
        context='ar-gen-final-warning-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('FINAL WARNING SUMMARY NOTICE'),
        fee_descr_col_is_NOT_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Final Notice
        template='ar_gen_final_notice_consolidated_email',
        context='ar-gen-final-notice-consolidated.json',
        otype='text/html',):
    (
        confirm_total_amount_due_is('$3,300.00'),
        confirm_notice_title_is('FINAL NOTICE SUMMARY'),
        fee_descr_col_is_NOT_present(),
        account_number_invisi_table_is_twice_present(),
    ),

    # AR GENERAL CONSOLIDATED NOTICES - END

    # TNC CONSOLIDATED NOTICES - START

    Recipe(  # for Friendly Reminder
        template='inspection_nc_friendly_reminder_consolidated_email',
        context='inspection-nc-friendly-reminder-consolidated.json',
        otype='text/html',):
    (
        confirm_notice_title_is('Inspection Non-compliances Friendly Reminder Notice'),
        confirm_banner_text_is('Inspection Non-compliances Friendly Reminder Notice'),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Past Due
        template='inspection_nc_past_due_consolidated_email',
        context='inspection-nc-past-due-consolidated.json',
        otype='text/html',):
    (
        confirm_notice_title_is('Inspection Non-compliances Past Due Notice'),
        confirm_banner_text_is('Inspection Non-compliances Past Due Notice'),
        account_number_invisi_table_is_twice_present(),
    ),

    Recipe(  # for Final Warning
        template='inspection_nc_final_warning_consolidated_email',
        context='inspection-nc-final-warning-consolidated-multiple-permits.json',
        otype='text/html',):
    (
        confirm_notice_title_is('Inspection Non-compliances Final Warning Notice'),
        confirm_banner_text_is('Inspection Non-compliances Final Warning Notice'),
        account_number_invisi_table_is_twice_present(),
    ),

    # TNC CONSOLIDATED NOTICES - END

}


def validate_document_generation(recipe, generated_doc_path):
    """Validate the document generated using the DGS and 3-tuple
    ``recipe`` and downloaded to ``generated_doc_path``.
    """
    try:
        validators = VALIDATORS_BY_RECIPE[recipe]
    except KeyError:
        raise AssertionError(
            f'Unable to validate generated document at'
            f' {generated_doc_path}.'
            f' The recipe {pprint.pformat(recipe)}'
            f' corresponds to no validators.')
    with open(generated_doc_path) as fh:
        haystack = fh.read()  # TODO: common interface for bytes and text data.
        for validator in validators:
            error = validator(haystack)
            if error:
                raise AssertionError(
                    f'Contrary to expectation, "{error}". Error generated when'
                    f' validating document at {generated_doc_path}')
