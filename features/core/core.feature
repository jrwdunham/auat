# To run this feature file against a Docker-compose deploy of TSBC NC DGS::
#
#     $ behave \
#           --tags=generate-ar-op-cons-emails \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN> \
#           -D ess_url=http://127.0.0.1:61780/micros/ess/v1/api/ \
#           -D ess_access_token=<ESS_TOKEN> \
#           --no-skipped \
#           -D driver_name=Firefox \

@generate-ar-op-cons-emails
Feature: AR OP Consolidated HTML Email Generation
  Clients of the TSBC NC APIs want to be able to generate HTML email documents
  using the Email Sending Service (ESS).

  @production
  Scenario Outline: Dan wants to generate the Accounts Receivable (AR) Operating Permit (OP) renewal HTML email documents using the DGS and confirm that the generated documents have the expected properties.
    Given a DGS instance containing the production templates
    When a document is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    AND the generated document is rendered correctly

    Examples: templates and contexts
    | template_key                               | context_path                                                |
    | ar_op_friendly_reminder_consolidated_email | etc/test_contexts/ar-op-friendly-reminder-consolidated.json |