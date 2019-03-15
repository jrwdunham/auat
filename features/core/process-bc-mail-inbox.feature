# BC Mail Inbox Processing
#
# To run this feature file, supply the tag for this feature and the URL and
# access token for running Delivery Service (DES) and Document Generator
# Service (DGS) instances::
#
#     $ behave \
#           --tags=process-bc-mail-inbox \
#           -D des_url=http://127.0.0.1:61780/micros/des/v1/api/ \
#           -D des_access_token=<DES_TOKEN> \
#           -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
#           -D dgs_access_token=<DGS_TOKEN>

@process-bc-mail-inbox
Feature: BC Mail Inbox Processing
  Technical Safety BC wants the Delivery Service (DES) to recognize when BC
  Mail has sent letters via the post. The DES should be able to process the
  plain text files that BC Mail deposits to our BC Mail inbox directory and
  update the Letter table in the database so that the sent letters have their
  statuses updated to "sent".

  Scenario: Jemi wants to confirm that when BC Mail deposits a report file into our BC Mail inbox that the DES will then automatically update itself to record the "sent" status of all letters that were sent by BC Mail.
    Given a DES instance containing multiple letters that have status "not sent"
    When a BC Mail report file is placed in the BC Mail inbox
    Then the DES is updated so that all letters in the report file have status "sent"
