"""Steps for features involving email record keeping."""

import logging

from behave import when, then, given


logger = logging.getLogger('tsbc-nc-auat.record-email-sendings-steps')


# Givens
# ------------------------------------------------------------------------------


# Whens
# ------------------------------------------------------------------------------

@when('a request is made to generate a record of the sending of the email')
def step_impl(context):
    context.scenario.generated_record_params = {  # just for later steps
        'output_type': 'application/pdf',
        'template_key': 'record_of_sent_email',
        'context_path': context.scenario.generated_document_params[
            'context_path'],}
    context.scenario.generate_record_response = (
        context.user.dgs.generate_and_store_email_record(
            context.scenario.send_email_resp,
            context.scenario.generated_document_params))


# Thens
# ------------------------------------------------------------------------------


# Utils
# ------------------------------------------------------------------------------

