# Email Record Keeping Feature
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for running Document Generator Service (DGS) and Email Sending
# Service (ESS) instances::
#
#     $ behave \
#           --tags=email-record \
#           -D ess_url=http://127.0.0.1:61780/micros/ess/v1/api/ \
#           -D ess_access_token=<ESS_TOKEN> \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN> \
#
# To target a specific template, e.g., the
# ar_op_friendly_reminder_consolidated_email template row of the "templates and
# contexts" table), add the following tag::
#
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_email \

@email-record
Feature: Email Record Keeping
  Users of the DGS (document generator) and ESS (email sender) want to be able
  to keep records of the emails that they send out. These records must be
  human-readable, immutable and non-executable.

  @template.template_key.<template_key>
  Scenario Outline: Kevin wants to generate and send emails using various templates and then generate and store a record of each of those email sending events. He expects the records to accurately document what was sent to whom when.
    Given a DGS instance containing an up-to-date template record_of_sent_email, including its template dependencies
    When an email is generated from <template_key> and <context_path> and sent
    And a request is made to generate a record of the sending of the email
    Then the record is stored in the MDS
    And the record accurately records the sending of the email

    Examples: templates and contexts
    | template_key                                       | output_type | context_path                                      |
    | ar_op_friendly_reminder_consolidated_email         | text/html   | ar-op-friendly-reminder-consolidated.json         |
    | ar_gen_past_due_consolidated_email                 | text/html   | ar-gen-past-due-consolidated.json                 |
    | inspection_nc_friendly_reminder_consolidated_email | text/html   | inspection-nc-friendly-reminder-consolidated.json |
    | so_waived_inspections_email                        | text/html   | so-waived-inspections-email.json                  |
