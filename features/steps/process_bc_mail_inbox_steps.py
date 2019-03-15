"""Steps for features involving the processing of the BC Mail inbox."""

import datetime
import logging
import os
import pprint
import random
from time import strptime, strftime, sleep

from behave import when, then, given


logger = logging.getLogger('tsbc-nc-auat.generate-documents-steps')


# Givens
# ------------------------------------------------------------------------------

@given('a DES instance containing multiple letters that have status "not sent"')
def step_impl(context):
    not_sent_letter_file_names = set()
    for (template_key, context_path) in (
            ('ar_op_friendly_reminder_consolidated_letter',
             'ar-op-friendly-reminder-consolidated.json'),
            ('ar_gen_demand_consolidated_letter',
             'ar-gen-demand-consolidated.json'),
            ('inspection_nc_final_warning_consolidated_letter',
             'inspection-nc-final-warning-consolidated-multiple-permits.json')):
        context.execute_steps(
            f'Given a DGS instance containing an up-to-date template'
              f' {template_key}, including its template dependencies\n'
            f'When a document of type application/pdf is generated from'
              f' template {template_key} using data context {context_path}\n'
            f'And a request is made to create a letter in the BC Mail folder'
              f' that references the document in the DES\n'
            f'Then a letter referencing the document is created in the DES\n'
            f'And the letter has status "not sent"\n')
        not_sent_letter_file_names.add(
            context.scenario.deliver_letter_response['file_name'])
    context.scenario.not_sent_letter_file_names = not_sent_letter_file_names


# Whens
# ------------------------------------------------------------------------------

@when('a BC Mail report file is placed in the BC Mail inbox')
def step_impl(context):
    report_text = generate_bc_mail_report_text(
        context.scenario.not_sent_letter_file_names)
    report_file_name = f'BCSAPI.{get_bc_mail_report_fname_date()}.REPORT.TXT'
    context.user.des.deposit_to_bc_mail_inbox(report_text, report_file_name)



# Thens
# ------------------------------------------------------------------------------

@then('the DES is updated so that all letters in the report file have status'
      ' "sent"')
def step_impl(context):
    letter_ids = [int(x.split('.')[1][3:]) for x in
                  context.scenario.not_sent_letter_file_names]
    # Fetch the letters up to 4 times, waiting at least 8 seconds for the DES
    # worker to mark the sent letters as such.
    statuses = []
    for _ in range(4):
        letters = context.user.des.fetch_letters_by_ids(letter_ids)
        statuses = [l['status'] for l in letters]
        if set(statuses) == {'sent'}:
            return
        sleep(2)
    logger.error('We expected all %s letters to have status "sent". In fact, %s'
                 ' letters have status "sent" and %s have status "not sent".',
                 len(letter_ids), statuses.count('sent'),
                 statuses.count('not sent'))


# Utils
# ------------------------------------------------------------------------------

def get_bc_mail_long_date(y, m, d):
    """Given (2019, 'MAR', 14), return 'March 14, 2019'."""
    return f'{strftime("%B", strptime(m,"%b"))} {d}, {y}'


def fn_to_bc_mail_report_line(file_name):
    """Given a file name like
    'BCSAPI.DES000000000037.000000000123456.D.2019.MAR.14.PDF',
    return a report line (of 123 characters) like
    DES000000000037 000000000123456 March 14, 2019
    """
    _, des_id, acct_no, _, y, m, d, _ = file_name.split('.')
    ret = f'{des_id} {acct_no} {get_bc_mail_long_date(y, m, d)}'
    return f'{ret}{(123 - len(ret)) * " "}'


def generate_bc_mail_report_text(letter_file_names):
    """Given a set of strings like
    'BCSAPI.DES000000000037.000000000123456.D.2019.MAR.14.PDF',
    return a string of lines like
    DES000000000037 000000000123456 March 14, 2019
    """
    return '\n'.join(map(fn_to_bc_mail_report_line, letter_file_names))


def get_bc_mail_report_fname_date():
    return (f'{datetime.datetime.utcnow().strftime("%b.%d.%Y").upper()}'
            f'.{str(random.random())[2:8]}')
