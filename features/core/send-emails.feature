# Send Emails Feature
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for running Email Sending Service (ESS) and Document Generator
# Service (DGS) instances::
#
#     $ behave \
#           --tags=email-send \
#           -D ess_url=http://127.0.0.1:61780/micros/ess/v1/api/ \
#           -D ess_access_token=<ESS_TOKEN> \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN>
#
# To target the template of a specific email to send, e.g., the
# ar_op_friendly_reminder_consolidated_email template row of the "templates and
# contexts" table), add the following tag::
#
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_email \

@email-send
Feature: Email Sending
  Clients of the TSBC NC APIs want to be able to send emails using the
  Email Sending Service (ESS). The emails being sent are HTML documents created
  using the Document Generator Service (DGS).

  @send-ar-op-cons-emails @template.template_key.<template_key>
  Scenario Outline: Dan wants to send sample Accounts Receivable (AR) Operating Permit (OP) renewal emails to an email address that he can access so that he can verify that the emails are delivered to their recipients and that they render correctly in target email clients.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create an email and send it to the tester using the ESS and the generated document
    Then the generated document is stored in the MDS
    And an email referencing the document is created in the ESS
    And the email has status sent
    And the email is delivered to the tester

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_op_friendly_reminder_consolidated_email | text/html   | ar-op-friendly-reminder-consolidated.json |
    | ar_op_past_due_consolidated_email          | text/html   | ar-op-past-due-consolidated.json          |
    | ar_op_demand_consolidated_email            | text/html   | ar-op-demand-consolidated.json            |
    | ar_op_final_warning_consolidated_email     | text/html   | ar-op-final-warning-consolidated.json     |
    | ar_op_final_notice_consolidated_email      | text/html   | ar-op-final-notice-consolidated.json      |

  @send-ar-gen-cons-emails @template.template_key.<template_key>
  Scenario Outline: Ireen wants to send sample Accounts Receivable (AR) general invoice notice emails to an email address that she can access so that she can verify that the emails are delivered to their recipients and that they render correctly in target email clients.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create an email and send it to the tester using the ESS and the generated document
    Then an email referencing the document is created in the ESS
    And the email has status sent
    And the email is delivered to the tester

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_gen_past_due_consolidated_email         | text/html   | ar-gen-past-due-consolidated.json         |
    | ar_gen_demand_consolidated_email           | text/html   | ar-gen-demand-consolidated.json           |
    | ar_gen_final_warning_consolidated_email    | text/html   | ar-gen-final-warning-consolidated.json    |
    | ar_gen_final_notice_consolidated_email     | text/html   | ar-gen-final-notice-consolidated.json     |

  @send-tnc-cons-emails @template.template_key.<template_key>
  Scenario Outline: Thor wants to send sample consolidated TNC notice HTML emails to an email address that he can access so that he can verify that the emails are delivered to their recipients and that they render correctly in target email clients.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create an email and send it to the tester using the ESS and the generated document
    Then an email referencing the document is created in the ESS
    And the email has status sent
    And the email is delivered to the tester

    Examples: templates and contexts
    | template_key                                       | output_type | context_path                                                       |
    | inspection_nc_friendly_reminder_consolidated_email | text/html   | inspection-nc-friendly-reminder-consolidated.json                  |
    | inspection_nc_past_due_consolidated_email          | text/html   | inspection-nc-past-due-consolidated.json                           |
    | inspection_nc_final_warning_consolidated_email     | text/html   | inspection-nc-final-warning-consolidated-multiple-permits.json     |

  @send-miscellaneous-emails @template.template_key.<template_key>
  Scenario Outline: Young wants to send sample miscellaneous HTML emails to an email address that he can access so that he can verify that the emails are delivered to their recipients and that they render correctly in target email clients.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create an email and send it to the tester using the ESS and the generated document
    Then an email referencing the document is created in the ESS
    And the email has status sent
    And the email is delivered to the tester

    Examples: templates and contexts
    | template_key                | output_type | context_path                     |
    | so_waived_inspections_email | text/html   | so-waived-inspections-email.json |
