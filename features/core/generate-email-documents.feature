# HTML Email Geneartion Feature
#
# To run this feature file against a Docker-compose deploy of TSBC NC DGS::
#
#     $ behave \
#           --tags=generate-ar-op-cons-emails \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN> \
#           -D ess_url=http://127.0.0.1:61780/micros/ess/v1/api/ \
#           -D ess_access_token=<ESS_TOKEN> \
#           --no-skipped
#
# To target a specific template, e.g., the
# ar_op_friendly_reminder_consolidated_email template row of the "templates and
# contexts" table), add the following tag::
#
#     $ behave \
#           --tags=generate-ar-op-cons-emails \
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_email \
#           ...

Feature: HTML Email Generation
  Clients of the TSBC NC APIs want to be able to generate HTML email documents
  using the Document Generator Service (DGS).

  @generate-ar-op-cons-emails @template.template_key.<template_key> @production
  Scenario Outline: Dan wants to generate the Accounts Receivable (AR) Operating Permit (OP) renewal HTML email documents using the DGS and confirm that the generated documents have the expected properties.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    And the generated document is rendered correctly

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_op_friendly_reminder_consolidated_email | text/html   | ar-op-friendly-reminder-consolidated.json |
    | ar_op_past_due_consolidated_email          | text/html   | ar-op-past-due-consolidated.json          |
    | ar_op_demand_consolidated_email            | text/html   | ar-op-demand-consolidated.json            |
    | ar_op_final_warning_consolidated_email     | text/html   | ar-op-final-warning-consolidated.json     |
    | ar_op_final_notice_consolidated_email      | text/html   | ar-op-final-notice-consolidated.json      |

  @generate-ar-gen-cons-emails @template.template_key.<template_key> @production
  Scenario Outline: Ireen wants to generate the Accounts Receivable (AR) general invoice notice HTML email documents using the DGS and confirm that the generated documents have the expected properties.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    And the generated document is rendered correctly

    Examples: templates and contexts
    | template_key                               | output_type | context_path                              |
    | ar_gen_past_due_consolidated_email         | text/html   | ar-gen-past-due-consolidated.json         |
    | ar_gen_demand_consolidated_email           | text/html   | ar-gen-demand-consolidated.json           |
    | ar_gen_final_warning_consolidated_email    | text/html   | ar-gen-final-warning-consolidated.json    |
    | ar_gen_final_notice_consolidated_email     | text/html   | ar-gen-final-notice-consolidated.json     |

  @generate-tnc-cons-emails @template.template_key.<template_key> @production
  Scenario Outline: Thor wants to generate consolidated TNC notice HTML email documents using the DGS and confirm that the generated documents have the expected properties.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    And the generated document is rendered correctly

    Examples: templates and contexts
    | template_key                                       | output_type | context_path                                                       |
    | inspection_nc_friendly_reminder_consolidated_email | text/html   | inspection-nc-friendly-reminder-consolidated.json                  |
    | inspection_nc_past_due_consolidated_email          | text/html   | inspection-nc-past-due-consolidated.json                           |
    | inspection_nc_final_warning_consolidated_email     | text/html   | inspection-nc-final-warning-consolidated-multiple-permits.json     |
