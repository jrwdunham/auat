"""Steps for features involving template verification."""

from collections import namedtuple
import logging
import os
import pprint

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.templates-up-to-date-steps')


# Givens
# ------------------------------------------------------------------------------


# Whens
# ------------------------------------------------------------------------------

@when('DGS template {template_key} is fetched')
def step_impl(context, template_key):
    context.scenario.template = context.user.dgs.get_template_by_key(
        template_key)


# Thens
# ------------------------------------------------------------------------------

@then('the template is up-to-date')
def step_impl(context):
    template_from_service = context.scenario.template
    expected_template = context.user.dgs.get_template_from_key(
        template_from_service['key'])
    assert template_from_service['data'].strip() == expected_template.data.strip(), (
        f'Template:'
        f'\n|{template_from_service["data"]}|\n\n'
        f'differs from:\n\n'
        f'|{expected_template.data}|')


# Utils
# ------------------------------------------------------------------------------
