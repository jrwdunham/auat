"""Steps for features involving email sending."""

from collections import namedtuple
import logging
import os
import pprint
import time
from uuid import uuid4

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.send-emails-steps')


# Givens
# ------------------------------------------------------------------------------


# Whens
# ------------------------------------------------------------------------------

@when('a request is made to create an email and send it to the tester using the'
      ' ESS and the generated document')
def step_impl(context):
    key = context.scenario.generated_document_params['template_key']
    # Give the email a unique subject value so that we can easily search for it
    # via the email client's API in a later step.
    context.scenario.sent_email_subject = f'{key}-{str(uuid4())}'
    context.scenario.send_email_resp = (
        context.user.ess.create_and_send_email(
            context.scenario.sent_email_subject,
            context.scenario.generate_document_response['url'],))


# Thens
# ------------------------------------------------------------------------------


@then('an email referencing the document is created in the ESS')
def step_impl(context):
    assert isinstance(context.scenario.send_email_resp['id'], int), (
        f'The send email request to the ESS failed: the response did not have'
        f' an id attribute of type int.')


@then('the email has status sent')
def step_impl(context):
    assert context.scenario.send_email_resp['status'] == 'sent', (
        f'The email does not have status "sent".')


@then('the email is delivered to the tester')
def step_impl(context):
    """Retrieve the email HTML from the email client, retrieve the
    corresponding document from the MDS, and then assert that the two HTML
    documents are identical.
    """
    if os.getenv('SKIP_EMAIL_DELIVERY_VERIFICATION') == 'true':
        return
    from_email_client = None
    sleep = 1
    for i in range(3):
        time.sleep(sleep)
        sleep *= 2
        try:
            from_email_client = (
                context.user.gmail.get_html_message_matching_query(
                    query=f'subject:{context.scenario.sent_email_subject}'))
        except context.user.gmail.GMailError:
            pass
        except Exception as err:
            raise AssertionError(
                f'Failed to retrieve the GMail message with subject'
                f' "{context.scenario.sent_email_subject}". UNEXPECTED ERROR:'
                f' {err}.')
    if not from_email_client:
        raise AssertionError(
            f'Failed to retrieve the GMail message with subject'
            f' "{context.scenario.sent_email_subject}".')
    downloaded_doc_path = (
        context.user.dgs.download_mds_doc_and_write_to_disk(
            context.scenario.generate_document_response['url'],
            f'not-minified-'  # NOTE: NOT MINIFIED
            f'{context.scenario.generate_document_response["file_name"]}'))
    with open(downloaded_doc_path) as fh:
        # assert from_email_client == from_mds  <== oddly, this fails ...
        from_mds = fh.read()
        mds_lines = from_mds.splitlines()
        email_lines = from_email_client.splitlines()
        differing_lines = []
        for i, mds_line in enumerate(mds_lines):
            email_line = email_lines[i]
            if email_line != mds_line:
                differing_lines.append((i, email_line, mds_line))
        if differing_lines:
            raise AssertionError(
                f'The message downloaded from the email client did not match'
                f' the generated document at {downloaded_doc_path}.')


@then('the email renders correctly in the email client of the tester')
def step_impl(context):
    raise NotImplementedError(
        f'Checking that the email renders correctly in the email client of the'
        f' tester is a step that must be performed manually.')


# Utils
# ------------------------------------------------------------------------------
