"""Steps for features involving document generation."""

from collections import namedtuple
import logging
import os
import pprint

from behave import when, then, given, use_step_matcher

from features.steps import utils
from features.steps.expected_pdf_texts import (
    TEXTS_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_LETTER,
    TEXTS_AR_OP_PAST_DUE_CONSOLIDATED_LETTER,
    TEXTS_AR_OP_DEMAND_CONSOLIDATED_LETTER,
    TEXTS_AR_OP_FINAL_WARNING_CONSOLIDATED_LETTER,
    TEXTS_AR_OP_FINAL_NOTICE_CONSOLIDATED_LETTER,
    TEXTS_AR_GEN_PAST_DUE_CONSOLIDATED_LETTER,
    TEXTS_AR_GEN_DEMAND_CONSOLIDATED_LETTER,
    TEXTS_AR_GEN_FINAL_WARNING_CONSOLIDATED_LETTER,
    TEXTS_AR_GEN_FINAL_NOTICE_CONSOLIDATED_LETTER,
    TEXTS_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_LETTER,
    TEXTS_INSPECTION_NC_PAST_DUE_CONSOLIDATED_LETTER,
    TEXTS_INSPECTION_NC_FINAL_WARNING_CONSOLIDATED_LETTER,
    TEXTS_SO_WAIVED_INSPECTIONS_LETTER,
    TEXTS_RECORD_OF_SENT_EMAIL_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL,
    TEXTS_RECORD_OF_SENT_EMAIL_AR_GEN_PAST_DUE_CONSOLIDATED_EMAIL,
    TEXTS_RECORD_OF_SENT_EMAIL_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL,
    TEXTS_RECORD_OF_SENT_EMAIL_SO_WAIVED_INSPECTIONS_EMAIL,
)


logger = logging.getLogger('tsbc-nc-auat.generate-documents-steps')


# Givens
# ------------------------------------------------------------------------------

@given('a DGS instance containing an up-to-date template {template_key},'
       ' including its template dependencies')
def step_impl(context, template_key):
    template = context.user.dgs.get_template_from_key(template_key)
    dependencies = context.user.dgs.get_template_dependencies(template)
    context.user.dgs.upsert_templates([template] + dependencies)


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
        context.user.dgs.generate_document(
            template_key, context_path, output_type=output_type))


# Thens
# ------------------------------------------------------------------------------

@then('the {document_description} is stored in the MDS')
def step_impl(context, document_description):
    """Expect ``document_description`` to be one of 'generated document' or
    'record'.
    """
    if document_description == 'record':
        generated_document_params = context.scenario.generated_record_params
        generate_document_response = context.scenario.generate_record_response
    else:
        generated_document_params = context.scenario.generated_document_params
        generate_document_response = context.scenario.generate_document_response
    doc_processor = {
        'application/pdf': lambda d: d,
        'text/html': context.user.dgs.minify_html_file,}.get(
            generated_document_params['output_type'])
    url = utils.internalize_url(
        generate_document_response['url'])
    context.scenario.downloaded_doc_path = (
        context.user.dgs.download_mds_doc_and_write_to_disk(
            url,
            generate_document_response['file_name'],
            doc_processor=doc_processor))
    assert os.path.isfile(context.scenario.downloaded_doc_path), (
        f'Failed to download generated document'
        f' {generate_document_response["file_name"]}'
        f' from url'
        f' {url}.'
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
        context.scenario.downloaded_doc_path,
        context.user.dgs)


@then('the record accurately records the sending of the email')
def step_impl(context):
    recipe = Recipe(
        template=context.scenario.generated_record_params['template_key'],
        context=context.scenario.generated_record_params['context_path'],
        otype=context.scenario.generated_record_params['output_type'],)
    validate_document_generation(
        recipe,
        context.scenario.downloaded_doc_path,
        context.user.dgs)


# Utils
# ------------------------------------------------------------------------------

# A "recipe" deterministically defines how to generate a document of type otype
# from template using context.
Recipe = namedtuple('Recipe', 'template, context, otype')


FEE_DESCRIPTION_TH = (
    '<th style="background-color: #F4F5F7; border: 1px solid #C1C7D0; margin:'
    ' 0px; padding: 0.5em;"><strong>Fee Description</strong></th>')

ACCOUNT_NUMBER_RIGHT_ALIGNED_TD = (
    '<td style="white-space: nowrap; border: none; text-align:'
    ' right; padding: 0.25em 0.25em;"><strong>Account Number:</strong></td>')


# Validator Creators
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# These are functions that return validator functions for a generated document.
# A validator takes two arguments, the first being the document to
# validate---either as a string of text (for HTML) or a file handle (for
# PDF)---, the second being the DGS ability instance. If the function returns a
# truthy value, it should be an error message. Implicitly returning ``None`` is
# the success case.


def confirm_total_amount_due_is(total_amount_due):
    def f(document_str, dgs_ability):
        if (('>Total amount due for all invoices</td>' not in document_str) or
                (f'>{total_amount_due}</td>' not in document_str)):
            return (f'Failed to find total amount due {total_amount_due} in the'
                    f' document.\n\n{document_str}')
    return f


def confirm_notice_title_is(title_text):
    """Note we allow centered titles with an increased font size and those
    without. This should probably be standardized.
    """
    def f(document_str, dgs_ability):
        if  ((f'<div style="text-align: center"> <span style="font-size:'
              f' 16px;"><strong> {title_text} </strong></span> <br> </div>'
              not in document_str) and
             (f'<div style="text-align: center"> <strong>{title_text}</strong>'
              f' </div>') not in document_str):
            return (f'Failed to find expected text "{title_text}" in the'
                    f' document.')
    return f


def confirm_banner_text_is(banner_text):
    def f(document_str, dgs_ability):
        if (f'<h3 style="font-size: 18px !important; line-height: 23px'
            f' !important; font-weight: bold !important; margin: 15px 0px'
            f' 10px; color: #FFFFFF; font-family: Arial,'
            f' sans-serif;">{banner_text}</h3></div>') not in document_str:
            return (f'Failed to find expected text "{banner_text}" in the'
                    f' blue banner at the top of the email.')
    return f


def confirm_greeting_is(greeting_text):
    def f(document_str, dgs_ability):
        if greeting_text not in document_str:
            return (f'Failed to find expected greeting "{greeting_text}" in the'
                    f' email.')
    return f


def fee_descr_col_is_present():
    def f(document_str, dgs_ability):
        if FEE_DESCRIPTION_TH not in document_str:
            return f'Failed to locate a "fee description" table column'
    return f


def fee_descr_col_is_NOT_present():
    return lambda ds, da: not fee_descr_col_is_present()(ds, da)


def account_number_invisi_table_is_twice_present():
    def f(document_str, dgs_ability):
        prsnc_cnt = document_str.count(ACCOUNT_NUMBER_RIGHT_ALIGNED_TD)
        if prsnc_cnt != 2:
            return (f'The right-aligned borderless "account number" table was'
                    f' found {prsnc_cnt} times. It should have been present 2'
                    f' times.')
    return f


def collection_action_stmnt_removed():
    def f(document_str, dgs_ability):
        if ('Failure to forward payment by the expiry date may result in'
            ' collection action') in document_str:
            return (f'The collection action statement was not removed. It'
                    f' should have been removed.')
    return f


def ssgr_s18_italicized_present():
    def f(document_str, dgs_ability):
        if (f'<i>Safety Standards General Regulations (SSGR) s. 18</i>'
                ) not in document_str:
            return 'The italicized SSGR s. 18 was not cited.'
    return f


def collection_mention_removed():
    def f(document_str, dgs_ability):
        if (('to avoid collection and enforcement actions' in document_str) or
                ('to avoid enforcement actions' not in document_str)):
            return 'The "collection actions" mention was not removed.'
    return f


def invoice_changed_to_notice():
    def f(document_str, dgs_ability):
        if ('If you have questions about this notice or your permit(s)'
                ) not in document_str:
            return 'The "this invoice" should have been changed to "this notice".'
    return f


def phone_number_for_payment_added():
    def f(document_str, dgs_ability):
        if ('to renew your operating permit or by calling 1 866 566 7233'
                ) not in document_str:
            return ('TSBC\'s phone number was not provided as a payment'
                    ' strategy.')
    return f



def phrases_in_pdf(expected_phrases):
    def f(document_bytes, dgs_ability):
        actual_phrases = dgs_ability.pdf2phrases(document_bytes)
        missing_phrases = expected_phrases - actual_phrases
        if missing_phrases:
            actual_phrases_str = '\n'.join(actual_phrases)
            return (f'The expected phrases are not all present in those extracted from'
                    f' the generated PDF file. There is/are'
                    f' {len(missing_phrases)} MISSING PHRASES; here is one:'
                    f' "{list(missing_phrases)[0]}". Here are the actual'
                    f' phrases from the PDF:\n{actual_phrases_str}')
    return f


def normalized_text_contains(expected_normalized_texts):
    """Return a validator function that checks whether all of the texts
    (strings) in expected_normalized_texts are present in document_bytes.
    """
    def f(document_bytes, dgs_ability):
        actual_normalized_text = dgs_ability.pdf2normalized_text(
            document_bytes)
        errors = []
        for text in expected_normalized_texts:
            if text not in actual_normalized_text:
                errors.append(text)
        if errors:
            delim = "\n\n"
            return (f'At least one expected normalized text fragment was not'
                    f' found in the actual normalized text of the document. The'
                    f' following text fragments were not'
                    f' found:\n\n{delim.join(errors)}\n\n'
                    f'The actual normalized text is:\n\n'
                    f'{actual_normalized_text}')
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

    # MISCELLANEOUS EMAILS - START

    Recipe(
        template='so_waived_inspections_email',
        context='so-waived-inspections-email.json',
        otype='text/html',):
    (
        confirm_banner_text_is(
            'Declaration submitted for Permit # &lt;PERMITNUMBER&gt; and'
            ' Inspection # &lt;INSPECTIONNUMBER&gt;'),
        confirm_greeting_is('Dear John Smith,'),
    ),

    # MISCELLANEOUS EMAILS - END

    # AR OP CONSOLIDATED LETTER NOTICES - START

    Recipe(
        template='ar_op_friendly_reminder_consolidated_letter',
        context='ar-op-friendly-reminder-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_op_past_due_consolidated_letter',
        context='ar-op-past-due-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_OP_PAST_DUE_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_op_demand_consolidated_letter',
        context='ar-op-demand-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_OP_DEMAND_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_op_final_warning_consolidated_letter',
        context='ar-op-final-warning-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_OP_FINAL_WARNING_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_op_final_notice_consolidated_letter',
        context='ar-op-final-notice-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_OP_FINAL_NOTICE_CONSOLIDATED_LETTER),
    ),

    # AR OP CONSOLIDATED LETTER NOTICES - END

    # AR GEN CONSOLIDATED LETTER NOTICES - START

    Recipe(
        template='ar_gen_past_due_consolidated_letter',
        context='ar-gen-past-due-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_GEN_PAST_DUE_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_gen_demand_consolidated_letter',
        context='ar-gen-demand-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_GEN_DEMAND_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_gen_final_warning_consolidated_letter',
        context='ar-gen-final-warning-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_GEN_FINAL_WARNING_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='ar_gen_final_notice_consolidated_letter',
        context='ar-gen-final-notice-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_AR_GEN_FINAL_NOTICE_CONSOLIDATED_LETTER),
    ),

    # AR GEN CONSOLIDATED LETTER NOTICES - END

    # TNC CONSOLIDATED LETTER NOTICES - START

    Recipe(
        template='inspection_nc_friendly_reminder_consolidated_letter',
        context='inspection-nc-friendly-reminder-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='inspection_nc_past_due_consolidated_letter',
        context='inspection-nc-past-due-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_INSPECTION_NC_PAST_DUE_CONSOLIDATED_LETTER),
    ),

    Recipe(
        template='inspection_nc_final_warning_consolidated_letter',
        context='inspection-nc-final-warning-consolidated-multiple-permits.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_INSPECTION_NC_FINAL_WARNING_CONSOLIDATED_LETTER),
    ),

    # TNC CONSOLIDATED LETTER NOTICES - END

    # MISCELLANEOUS LETTER NOTICES - START

    Recipe(
        template='so_waived_inspections_letter',
        context='so-waived-inspections-email.json',
        otype='application/pdf'):
    (
        normalized_text_contains(TEXTS_SO_WAIVED_INSPECTIONS_LETTER),
    ),

    # MISCELLANEOUS LETTER NOTICES - END

    # RECORDS OF EMAILS (PDFS) - START

    Recipe(
        template='record_of_sent_email',
        context='ar-op-friendly-reminder-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(
            TEXTS_RECORD_OF_SENT_EMAIL_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL),
    ),

    Recipe(
        template='record_of_sent_email',
        context='ar-gen-past-due-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(
            TEXTS_RECORD_OF_SENT_EMAIL_AR_GEN_PAST_DUE_CONSOLIDATED_EMAIL),
    ),

    Recipe(
        template='record_of_sent_email',
        context='inspection-nc-friendly-reminder-consolidated.json',
        otype='application/pdf'):
    (
        normalized_text_contains(
            TEXTS_RECORD_OF_SENT_EMAIL_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_EMAIL),
    ),

    Recipe(
        template='record_of_sent_email',
        context='so-waived-inspections-email.json',
        otype='application/pdf'):
    (
        normalized_text_contains(
            TEXTS_RECORD_OF_SENT_EMAIL_SO_WAIVED_INSPECTIONS_EMAIL),
    ),

    # RECORDS OF EMAILS (PDFS) - END
}


def validate_document_generation(recipe, generated_doc_path, dgs_ability):
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
    _, ext = os.path.splitext(generated_doc_path)
    kwargs = {'.pdf': {'mode': 'rb'}}.get(ext.lower(), {})
    with open(generated_doc_path, **kwargs) as fh:
        haystack = fh
        if not kwargs:
            haystack = fh.read()
        for validator in validators:
            error = validator(haystack, dgs_ability)
            if error:
                raise AssertionError(
                    f'Contrary to expectation, "{error}". Error generated when'
                    f' validating document at {generated_doc_path}')
