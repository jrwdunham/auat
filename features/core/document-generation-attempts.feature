# Document Generation Attempts Feature
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for a running Document Generator Service instance::
#
#     $ behave \
#           --tags=doc-gen-attempts \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN> \
#
# To target a specific template, e.g., the
# ar_op_friendly_reminder_consolidated_email template row of the "templates and
# contexts" table), add the following tag::
#
#           --tags=template.template_key.ar_op_friendly_reminder_consolidated_email \

@doc-gen-attempts
Feature: Document Generation Attempts Recorded
  Users of the Docuemtn Generator Service (DGS) want to ensure that their
  attempts to generate documents are correctly recorded. If a generation
  attempt fails, they want to be able to use the API to gain insight into that
  failure.

  @template.template_key.<template_key>
  Scenario Outline: Joon wants to confirm that failed document generation attempts are correctly recorded in the DGS's database.
    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When an attempt is made to generate a document of type <output_type> from template <template_key> using data context <context_path>
    Then the document generation attempt fails
    And the document generation attempt is correctly recorded

    Examples: templates and contexts
    | template_key                               | output_type | context_path |
    | ar_op_friendly_reminder_consolidated_email | bad/type    | error.json   |
    | ar_op_friendly_reminder_consolidated_email | text/html   | error.json   |
