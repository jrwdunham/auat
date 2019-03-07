"""Contains the texts that we expect to be able to extract from specific PDFs
generated by the DGS. These texts are the extracted texts from the PDFs with
all strings of contiguous whitespace converted to a single space character.
This is a pretty hacky and brittle way to test, but it works as a first
approximation---a basic regression test.

For the implementation of the "extract texts from a pdf" algorithm assumed
here, see ``DGSAPIAbility.pdf2normalized_text``.
"""


TEXTS_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_LETTER = """Friendly Reminder Operating Permit Renewal Invoice Summary Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Friendly Reminder Date: March 06, 2019 The following Operating Permit(s) are due to expire as per the due dates listed below. To renew operating permit(s), please remit the total amount due. For Electrical operating permits, please also submit the Operating Permit-FSR Verification form (attached to your operating permit renewal invoice). Operating permits will be issued upon receipt of payment and signed FSR Verification form for Electrical operating permit(s). Invoice Number Due Date Fee Description Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 01/20/2019 00345689 01/20/2019 Site: 17e 34 Surrey BC; Work Class: Energy Utility Site: 45w 64 Surrey BC; Work Class: Energy Utility $1,000.00 $2,500.00 Total amount due for all invoices Payment terms and conditions $198.25 $0.01 $801.75 $2,499.99 $3,301.74 We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. Payment can be made online at www.technicalsafetybc.ca or by calling 1 866 566 7233. The person/entity named on this notice is wholly responsible for remitting the total amount due prior to expiry date. In British Columbia, the Safety Standards General Regulations (SSGR) s. 18 requires a valid operating permit to maintain or operate a regulated product. For more information visit our website www.technicalsafetybc.ca. This invoice is now due and payable to Technical Safety BC. To pay online, go to www.technicalsafetybc.ca and click "Pay an Invoice." BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1623 Page 1 of 1"""
TEXTS_AR_OP_PAST_DUE_CONSOLIDATED_LETTER = """Past Due Operating Permit Renewal Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Past Due Date: March 06, 2019 Further to our Friendly Reminder Operating Permit Renewal Invoice notice, our records indicate that your operating permit(s) is (are) now expired and you are not compliant with provincial regulations. Please forward payment immediately to renew your operating permit and to avoid collection and enforcement actions. You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" to renew your operating permit. If you have questions about this notice or your permit(s), call our contact center at 1 866 566 7233. If you have already made payment to renew your operating permit or have requested an adjustment to your account that has not been processed, please disregard this notice. Operating permits will be issued upon receipt of payment and signed FSR Verification form for Electrical operating permit(s). Invoice Number Due Date Fee Description Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 01/20/2019 00345689 01/20/2019 Site: 17e 34 Surrey BC; Work Class: Energy Utility Site: 45w 64 Surrey BC; Work Class: Energy Utility $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1624 Page 1 of 2"""
TEXTS_AR_OP_DEMAND_CONSOLIDATED_LETTER = """Demand Operating Permit Renewal Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Demand Date: March 06, 2019 Further to our Past Due Notice, our records still indicate that your operating permit(s) is (are) now expired and you are not compliant with provincial regulations. You are required to make payment for this amount upon receipt. Please forward payment immediately to renew your operating permit and to avoid enforcement actions. In British Columbia, the Safety Standards General Regulations (SSGR) s. 18 requires a valid operating permit to maintain or operate a regulated product. For more information visit our website www.technicalsafetybc.ca. Take notice that, because of your failure to pay money owed under the Act, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under authority of section 18(3) of the Act. You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" to renew your operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), please call our contact center at 1 866 566 7233. Should we fail to receive your payment and confirmation of your permit renewal by the timeline herein, we will be taking further action without notice to you. Invoice Number Due Date Fee Description Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 01/20/2019 00345689 01/20/2019 Site: 17e 34 Surrey BC; Work Class: Energy Utility Site: 45w 64 Surrey BC; Work Class: Energy Utility $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1625 Page 1 of 1"""
TEXTS_AR_OP_FINAL_WARNING_CONSOLIDATED_LETTER = """Final Warning Operating Permit Renewal Notice of Non- compliance Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Final Warning Date: March 06, 2019 Further to the Demand Notice you have received from us, your operating permit(s) is/are expired. You do not have a current operating permit and are therefore in breach of your obligations under the Safety Standards Act, SBC 2003, c. 39 (the "Act"). You are required to make immediate payment of this account. Should we we fail to receive your payment and confirmation of your permit renewal within the next 20 working days of this notice, you may be subject to enforcement actions as a result of your failure to obtain an operating permit as required by section 18 of the Safety Standards General Regulation. Take notice that, because of your non-compliant status, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under the authority of section 18(3) of the Act. You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" to renew your operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), please call our contact center at 1 866 566 7233. Should we fail to receive a response from you by the timeline herein, we will be taking further action without notice to you. If you have already made payment to renew your operating permit, please disregard this notice. Invoice Number Due Date Fee Description Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 01/20/2019 00345689 01/20/2019 Site: 17e 34 Surrey BC; Work Class: Energy Utility Site: 45w 64 Surrey BC; Work Class: Energy Utility $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1626 Page 1 of 1"""
TEXTS_AR_OP_FINAL_NOTICE_CONSOLIDATED_LETTER = """Final Notice Operating Permit Renewal Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Final Notice Date: March 06, 2019 As a result of the failure to comply with the Final Warning Notice we have sent you regarding your operating permit(s) which is expired over 150 days, please be advised that you may be subject to immediate compliance and enforcement action. As you do not have a current operating permit you are in breach of your obligations under the Safety Standards Act, SBC 2003, c. 39 (the "Act"). A record has been created with our Compliance and Enforcement team regarding your account and they will be in contact with you directly shortly. Take further notice that, because of your non-compliant status, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under the authority of section 18(3) of the Act. The following Operating Permit(s) below are expired. To renew operating permit(s), please remit the total amount due. For Electrical operating permits, please also submit the Operating Permit-FSR Verification form (attached to the renewal invoice). You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" to renew your operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), please call our contact center at 1 866 566 7233. Operating permits will be issued upon receipt of payment and signed FSR Verification form for Electrical operating permit(s). Invoice Number Due Date Fee Description Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 01/20/2019 00345689 01/20/2019 Site: 17e 34 Surrey BC; Work Class: Energy Utility Site: 45w 64 Surrey BC; Work Class: Energy Utility $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1627 Page 1 of 2"""
TEXTS_AR_GEN_PAST_DUE_CONSOLIDATED_LETTER = """Past Due Summary Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Past Due Date: March 06, 2019 Our records indicate that you have failed to make payments for the invoices listed below. Your invoices are now past due and you were required to make payment for these invoices upon receipt. The amount on this statement is a debt owing to Technical Safety BC. If you have already made payment or have requested an adjustment to your account that has not been processed, please disregard this notice. Failure to make immediate payment may result in collections action being taken against you. Take further notice that, because of your failure to pay money owed under the Act, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under authority of section 18.1(1) of the Act. You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), call our contact center at 1 866 566 7233. Past Due Invoice Number Due Date Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 00345689 Upon Receipt Upon Receipt $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 For fast, easy payment, use our online services! Login with your online account details or register for an online account by emailing us at clientportal@technicalsafetybc.ca . BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1628 Page 1 of 1"""
TEXTS_AR_GEN_DEMAND_CONSOLIDATED_LETTER = """Demand Summary Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Demand Date: March 06, 2019 Further to our Past Due Summary notice, our records still indicate that you have failed to make payments for the invoices listed below. Your account balance of $3,300.00 is overdue. You are required to make payment for this amount upon receipt. The amount on this statement is a debt owing to Technical Safety BC. If you have already made payment or have requested an adjustment to your account that has not been processed, please disregard this notice. Take notice that you are required to make immediate payment of this account. If we fail to receive your payment by within 30 days of this, you may be subject to collections action or we may pursue a claim against you in the Courts of British Columbia. Take further notice that, because of your failure to pay money owed under the Act, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under authority of section 18.1(1) of the Act. You may make payment online by going to www.technicalsafetybc.ca and click "Pay an Invoice" or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), call our contact center at 1 866 566 7233. Past Due Invoice Number Due Date Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 00345689 Upon Receipt Upon Receipt $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 For fast, easy payment, use our online services! Login with your online account details or register for an online account by emailing us at clientportal@technicalsafetybc.ca . BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1629 Page 1 of 1"""
TEXTS_AR_GEN_FINAL_WARNING_CONSOLIDATED_LETTER = """Final Warning Summary Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Final Warning Date: March 06, 2019 Further to our Demand Summary notice, our records still indicate that you have failed to make payment for invoices listed below. Your account balance of $3,300.00 is overdue. You are required to make payment for this amount upon receipt. The amount on this statement is a debt owing to Technical Safety BC. Please note that should we fail to receive your payment within the next 20 working days of this notice, your invoice will be sent to a third party collections agency for further action. Take notice that, because of your non-compliant status, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under the authority of section 18.1(1) of the Act. We reserve the right to pursue a claim against you in the Courts of British Columbia to recover the amount of this debt and to seek all available remedies including seizure and sale pursuant to the Court Order Enforcement Act, RSBC 1996, c. 78. You may make payment online by going to www.technicalsafetybc.ca and click "Pay an Invoice" or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), call our contact center at 1 866 566 7233. Should we fail to receive a response from you by the timeline herein, we will be taking further action without notice to you. If you have already made payment, please disregard this notice. Past Due Invoice Number Due Date Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 00345689 Upon Receipt Upon Receipt $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1630 Page 1 of 2"""
TEXTS_AR_GEN_FINAL_NOTICE_CONSOLIDATED_LETTER = """Final Notice Summary Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 123456 Final Notice Date: March 06, 2019 Further to our Final Warning Summary notice, our records still indicate that you have failed to make payments for the invoices listed below. Your account balance of $3,300.00 is overdue. You are required to make payment for this amount upon receipt. The amount on this statement is a debt owing to Technical Safety BC. Take notice that, because of your non-compliant status, a Safety Officer or Safety Manager may refuse to issue or may cancel or suspend any other certificate, license, permit or other permission you apply for or currently hold, under the authority of section 18.1(1) of the Act. You may make payment by going to www.technicalsafetybc.ca and click "Pay an Invoice" or by calling 1 866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made payable to Technical Safety BC), and money orders. If you have questions about this notice or your permit(s), call our contact center at 1 866 566 7233. Should we fail to receive a response from you by the timeline herein, we will be taking further action without notice to you. If you have already made payment, please disregard this notice. Past Due Invoice Number Due Date Invoice Total Payments/Adjustment Credits Total Amount Due 00345678 00345689 Upon Receipt Upon Receipt $1,000.00 $2,500.00 Total amount due for all invoices $200.00 $0.00 $800.00 $2,500.00 $3,300.00 For fast, easy payment, use our online services! Login with your online account details or register for an online account by emailing us at clientportal@technicalsafetybc.ca . BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1631 Page 1 of 1"""
TEXTS_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_LETTER = """Inspection Non-compliances Friendly Reminder Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 1122334455 Date: March 06, 2019 Dear John Smith, Further to our certificate of inspection(s) issued regarding the assessment(s) performed at your site(s), please note that correction of your non-compliances are due as per the dates listed in the following notice. In accordance with s. 20(3) of the Safety Standards General Regulation , you are required to correct any non-compliances with respect to regulated work or regulated product identified on a certificate of inspection and notify the safety officer that the corrections have been completed. Please submit your declaration to confirm that the non-compliances below have been resolved by the required due dates. You can submit your declaration via your online account. Failure to resolve assessed non- compliances by the required due dates may result in compliance and enforcement action for breach of s. 20(3) of the Safety Standards General Regulation. If you have any questions regarding this notification, please contact us directly via your online account, via email at contact@technicalsafetybc.ca, or contact your safety officer directly. Thank you in advance for your attention. Technical Safety BC BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1632 Page 1 of 4"""
TEXTS_INSPECTION_NC_PAST_DUE_CONSOLIDATED_LETTER = """Inspection Non-compliances Past Due Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 1122334455 Date: March 06, 2019 Dear John Smith, Further to our Certificate of Inspection regarding the assessment performed at your site, please note that correction of your non-compliances is now past due. You were issued certificate of inspection(s) that required you to resolve non-compliances by due dates listed in the following notice. Our records indicate that you have not submitted a declaration to confirm that your non-compliances have been resolved by the required due dates nor have you submitted a request for an extension of time. In accordance with s. 20(3) of the Safety Standards General Regulation , you are required to correct any non-compliances with respect to regulated work or regulated product identified on a certificate of inspection and notify the safety officer that the corrections have been completed. You are now in breach of this requirement. You may be subject to compliance and enforcement action for failure to submit a declaration confirming correction of these non-compliances. Please submit your declaration as soon as possible. You can submit your declaration directly by contacting our office or via your online account. We will be contacting you shortly to follow up on this notification. Thank you in advance for your attention. Technical Safety BC BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1633 Page 1 of 4"""
TEXTS_INSPECTION_NC_FINAL_WARNING_CONSOLIDATED_LETTER = """Inspection Non-compliances Final Warning Notice Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Account Number: 1122334455 Date: March 06, 2019 Dear John Smith, Further to our INSPECTION NON-COMPLIANCES PAST DUE NOTICE regarding the assessment(s) performed at your site, our records indicate that you have not submitted a declaration to confirm that your non- compliances have been resolved by the required due date(s) nor have you submitted a request for an extension of time. In accordance with s. 20(3) of the Safety Standards General Regulation , you are required to correct any non-compliances with respect to regulated work or regulated product identified on a certificate of inspection and notify the safety officer that the corrections have been completed. You are now in breach of this requirement. Please note that you may be subject to immediate compliance and enforcement action for failure to declare the completion of these non-compliances. Your file may be forwarded to compliance and enforcement for consideration of next steps without further warning to you. Submit your declaration or request for an extension of time as soon as possible. You can submit your declaration via your online account. Thank you in advance for your attention. Technical Safety BC BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-1635 Page 1 of 6"""
TEXTS_SO_WAIVED_INSPECTIONS_LETTER = """Declaration submitted for Permit # <PERMITNUMBER> and Inspection # <INSPECTIONNUMBER> Some Company Inc. ATTN: John Smith 123 SOME STREET VANCOUVER BC V8V 8V8 Date: March 06, 2019 Dear John Smith, Thank you for submitting your declaration. After reviewing your declaration, your inspection has been assessed and at this time no further actions are required. Please note that since a physical inspection was not performed, your submitted declaration form serves as documentation verifying that the scope of work has been completed to Code. If you have any questions regarding this permit and or corresponding inspection(s), please contact Technical Safety BC at 1 866 566 7233. For information on the Safety Standards Act, Regulations, and the review/appeal process, please visit www.technicalsafetybc.ca. Thank you, Dave Gilmour Safety Officer Name: Dave Gilmour Safety Officer Phone: 604-999-7777 Safety Officer Email: Dave.Gilmour@technicalsafetybc.ca BC Safety Authority is now Technical Safety BC. While we have changed our name, we remain committed to our vision of Safe Technical Systems. Everywhere. Learn more about our evolving services and how we share safety knowledge at www.technicalsafetybc.ca. Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E contact@technicalsafetybc.ca www.technicalsafetybc.ca FRM-0001 Page 1 of 1"""
