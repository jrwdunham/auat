# Templates Up-to-date Feature
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for a running Document Generator Service instance::
#
#     $ behave \
#           --tags=templates-up-to-date \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN> \
#
# To target a specific template, e.g., the
# ar_op_friendly_reminder_consolidated_email template row of the "templates and
# contexts" table), add the following tag::
#
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_email \

@templates-up-to-date @non-mutative
Feature: Templates Up-to-date
  Users of a DGS API instance want to be able to confirm that the templates
  of that instance are up-to-date.

  @ar-op-cons @template.template_key.<template_key>
  Scenario Outline: Dan wants to confirm that the Accounts Receivable (AR) Operating Permit (OP) renewal templates are up-to-date.
    When DGS template <template_key> is fetched
    Then the template is up-to-date

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_op_friendly_reminder_consolidated_email | text/html   | ar-op-friendly-reminder-consolidated.json |
    | ar_op_past_due_consolidated_email          | text/html   | ar-op-past-due-consolidated.json          |
    | ar_op_demand_consolidated_email            | text/html   | ar-op-demand-consolidated.json            |
    | ar_op_final_warning_consolidated_email     | text/html   | ar-op-final-warning-consolidated.json     |
    | ar_op_final_notice_consolidated_email      | text/html   | ar-op-final-notice-consolidated.json      |

  @ar-gen-cons @template.template_key.<template_key>
  Scenario Outline: Ireen wants to confirm that the Accounts Receivable (AR) general invoice notice templates are up-to-date.
    When DGS template <template_key> is fetched
    Then the template is up-to-date

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_gen_past_due_consolidated_email         | text/html   | ar-gen-past-due-consolidated.json         |
    | ar_gen_demand_consolidated_email           | text/html   | ar-gen-demand-consolidated.json           |
    | ar_gen_final_warning_consolidated_email    | text/html   | ar-gen-final-warning-consolidated.json    |
    | ar_gen_final_notice_consolidated_email     | text/html   | ar-gen-final-notice-consolidated.json     |

  @tnc-cons @template.template_key.<template_key>
  Scenario Outline: Thor wants to confirm that the TNC notice templates are up-to-date.
    When DGS template <template_key> is fetched
    Then the template is up-to-date

    Examples: templates and contexts
    | template_key                                       | output_type | context_path                                                       |
    | inspection_nc_friendly_reminder_consolidated_email | text/html   | inspection-nc-friendly-reminder-consolidated.json                  |
    | inspection_nc_past_due_consolidated_email          | text/html   | inspection-nc-past-due-consolidated.json                           |
    | inspection_nc_final_warning_consolidated_email     | text/html   | inspection-nc-final-warning-consolidated-multiple-permits.json     |

  @miscellaneous @template.template_key.<template_key>
  Scenario Outline: Young wants to confirm that the miscellaneous templates are up-to-date.
    When DGS template <template_key> is fetched
    Then the template is up-to-date

    Examples: templates and contexts
    | template_key                | output_type | context_path                     |
    | so_waived_inspections_email | text/html   | so-waived-inspections-email.json |
