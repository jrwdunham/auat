"""General-purpose Steps."""

import logging
import time

from behave import when, then, given, use_step_matcher

from features.steps import utils


logger = logging.getLogger('tsbc-nc-auat.steps')


# Givens
# ------------------------------------------------------------------------------

@given('a DGS instance containing the production templates')
def step_impl(context):
    print('Given a DGS instance containing the production templates')


# Whens
# ------------------------------------------------------------------------------

@when('a document is generated from template {template_key} using data context'
      ' {context_path}')
def step_impl(context, template_key, context_path):
    print(f'When a document is generated from template {template_key} using'
          f' data context {context_path}')


# Thens
# ------------------------------------------------------------------------------

@then('the generated document is stored in the MDS')
def step_impl(context):
    print('Then the generated document is stored in the MDS')


@then('the generated document is rendered correctly')
def step_impl(context):
    print('Then the generated document is rendered correctly')
