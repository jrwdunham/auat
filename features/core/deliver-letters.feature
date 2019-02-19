# PDF Letter Delivery
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for running Delivery Service (DES) and Document Generator
# Service (DGS) instances::
#
#     $ behave \
#           --tags=letter-deliver \
#           -D des_url=http://127.0.0.1:61780/micros/des/v1/api/ \
#           -D des_access_token=<DES_TOKEN> \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN>
#
# To target the template of a specific letter to deliver, e.g., the
# ar_op_friendly_reminder_consolidated_letter template row of the "templates and
# contexts" table), add the following tag::
#
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_letter \

@letter-delivery
Feature: PDF Letter Delivery
  Clients of the TSBC NC APIs want to be able to generate PDF letters and
  deliver them to recipients using the Delivery Service (DES).

  @deliver-ar-op-cons-letters @template.template_key.<template_key> @production
  Scenario Outline: Dan wants to deliver sample Accounts Receivable (AR) Operating Permit (OP) renewal letters to test permit holders and confirm that the letters are deposited correctly in the Delivery Service.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create a letter that references the document in the DES
    Then a letter referencing the document is created in the ESS
    And the letter has status "not delivered"

    Examples: templates and contexts
    | template_key                                | output_type       | context_path                              |
    | ar_op_friendly_reminder_consolidated_letter | application/pdf   | ar-op-friendly-reminder-consolidated.json |
    | ar_op_past_due_consolidated_letter          | application/pdf   | ar-op-past-due-consolidated.json          |
    | ar_op_demand_consolidated_letter            | application/pdf   | ar-op-demand-consolidated.json            |
    | ar_op_final_warning_consolidated_letter     | application/pdf   | ar-op-final-warning-consolidated.json     |
    | ar_op_final_notice_consolidated_letter      | application/pdf   | ar-op-final-notice-consolidated.json      |

  @deliver-ar-gen-cons-letters @template.template_key.<template_key> @production
  Scenario Outline: Ireen wants to deliver sample Accounts Receivable (AR) general invoice notice letters to test permit holders and confirm that the letters are deposited correctly in the Delivery Service.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create a letter that references the document in the DES
    Then a letter referencing the document is created in the ESS
    And the letter has status "not delivered"

    Examples: templates and contexts
    | template_key                                | output_type       | context_path                              |
    | ar_gen_past_due_consolidated_letter         | application/pdf   | ar-gen-past-due-consolidated.json         |
    | ar_gen_demand_consolidated_letter           | application/pdf   | ar-gen-demand-consolidated.json           |
    | ar_gen_final_warning_consolidated_letter    | application/pdf   | ar-gen-final-warning-consolidated.json    |
    | ar_gen_final_notice_consolidated_letter     | application/pdf   | ar-gen-final-notice-consolidated.json     |

  @deliver-tnc-cons-letters @template.template_key.<template_key> @production
  Scenario Outline: Thor wants to deliver sample TNC notice letters to test permit holders and confirm that the letters are deposited correctly in the Delivery Service.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    And a request is made to create a letter that references the document in the DES
    Then a letter referencing the document is created in the ESS
    And the letter has status "not delivered"

    Examples: templates and contexts
    | template_key                                        | output_type       | context_path                                                       |
    | inspection_nc_friendly_reminder_consolidated_letter | application/pdf   | inspection-nc-friendly-reminder-consolidated.json                  |
    | inspection_nc_past_due_consolidated_letter          | application/pdf   | inspection-nc-past-due-consolidated.json                           |
    | inspection_nc_final_warning_consolidated_letter     | application/pdf   | inspection-nc-final-warning-consolidated-multiple-permits.json     |
