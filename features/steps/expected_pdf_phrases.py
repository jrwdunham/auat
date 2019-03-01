"""Contains exact sets of the "phrases" that we expect to be able to extract
from specific PDFs generated by the DGS. This is a pretty hacky and brittle way
to test, but it works as a first approximation---a basic regression test.

For the implementation of the "extract text phrases from a pdf" algorithm
assumed here, see ``DGSAPIAbility.pdf2phrases``.

"""


PHRASES_AR_OP_FRIENDLY_REMINDER_CONSOLIDATED_LETTER = {
    '$0.01',
    '$1,000.00',
    '$198.25',
    '$2,499.99',
    '$2,500.00',
    '$3,301.74',
    '$801.75',
    '00345678',
    '00345689',
    '01/20/2019',
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Credits',
    'Due',
    'Due Date',
    'Electrical operating permit(s).',
    'Energy Utility',
    'FRM-1623',
    'Fee Description',
    'Friendly Reminder Operating Permit Renewal',
    'Invoice',
    'Invoice Summary',
    'Number',
    'Operating permits will be issued upon receipt of payment and signed FSR '
    'Verification form for',
    'Page 1 of 2',
    'Payments/Adjustment',
    'Permit-FSR Verification form (attached to your operating permit renewal '
    'invoice).',
    'Site: 17e 34 Surrey BC; Work Class:',
    'Site: 45w 64 Surrey BC; Work Class:',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'The following Operating Permit(s) are due to expire as per the due dates '
    'listed below. To renew operating',
    'Total',
    'Total Amount',
    'Total amount due for all invoices',
    'VANCOUVER BC V8V 8V8',
    'permit(s), please remit the total amount due. For Electrical operating '
    'permits, please also submit the Operating'
}


PHRASES_AR_OP_PAST_DUE_CONSOLIDATED_LETTER = {
    '$0.00',
    '$1,000.00',
    '$2,500.00',
    '$200.00',
    '$3,300.00',
    '$800.00',
    '00345678',
    '00345689',
    '01/20/2019',
    '123 SOME STREET',
    '7233.',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Credits',
    'Due',
    'Due Date',
    'Electrical operating permit(s).',
    'Energy Utility',
    'FRM-1624',
    'Fee Description',
    'Further to our Friendly Reminder Operating Permit Renewal Invoice notice, '
    'our records indicate',
    'If you have already made payment to renew your operating permit or have '
    'requested an adjustment to your',
    'Invoice',
    'Number',
    'Operating permits will be issued upon receipt of payment and signed FSR '
    'Verification form for',
    'Page 1 of 2',
    'Past Due Operating Permit Renewal Notice',
    'Payments/Adjustment',
    'Site: 17e 34 Surrey BC; Work Class:',
    'Site: 45w 64 Surrey BC; Work Class:',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Total',
    'Total Amount',
    'Total amount due for all invoices',
    'VANCOUVER BC V8V 8V8',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" to renew your',
    'account that has not been processed, please disregard this notice.',
    'collection and enforcement actions.',
    'operating permit. If you have questions about this notice or your permit(s), '
    'call our contact center at 1 866 566',
    'regulations. Please forward payment immediately to renew your operating '
    'permit and to avoid',
    'that your operating permit(s) is (are) now expired and you are not compliant '
    'with provincial'
}


PHRASES_AR_OP_DEMAND_CONSOLIDATED_LETTER = {
    '(made payable to Technical Safety BC), and money orders. If you have '
    'questions about this notice or your',
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Demand Operating Permit Renewal Notice',
    'FRM-1625',
    'Further to our Past Due Notice, our records still indicate that your '
    'operating permit(s) is (are) now',
    'In British Columbia, the Safety Standards General Regulations (SSGR) s. 18 '
    'requires a valid operating permit to',
    'Page 1 of 2',
    'Should we fail to receive your payment and confirmation of your permit '
    'renewal by the timeline herein, we will',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take notice that, because of your failure to pay money owed under the Act, a '
    'Safety Officer or Safety Manager',
    'VANCOUVER BC V8V 8V8',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" to renew your',
    'apply for or currently hold, under authority of section 18(3) of the Act.',
    'be taking further action without notice to you.',
    'enforcement actions.',
    'expired and you are not compliant with provincial regulations. You are '
    'required to make payment for',
    'maintain or operate a regulated product. For more information visit our '
    'website www.technicalsafetybc.ca.',
    'may refuse to issue or may cancel or suspend any other certificate, license, '
    'permit or other permission you',
    'operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, '
    'Mastercard, and Amex), cheques',
    'permit(s), please call our contact center at 1 866 566 7233.',
    'this amount upon receipt. Please forward payment immediately to renew your '
    'operating permit and to avoid'
}


PHRASES_AR_OP_FINAL_WARNING_CONSOLIDATED_LETTER = {
    '(made payable to Technical Safety BC), and money orders. If you have '
    'questions about this notice or your',
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'FRM-1626',
    'Final Warning Operating Permit Renewal Notice',
    'Further to the Demand Notice you have received from us, your operating '
    'permit(s) is/are expired.',
    'Page 1 of 2',
    'Should we fail to receive a response from you by the timeline herein, we '
    'will be taking further action without',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take notice that, because of your non-compliant status, a Safety Officer or '
    'Safety Manager may refuse to issue',
    'VANCOUVER BC V8V 8V8',
    'You are required to make immediate payment of this account. Should we we '
    'fail to receive your payment',
    'You do not have a current operating permit and are therefore in breach of '
    'your obligations under',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" to renew your',
    'and confirmation of your permit renewal within the next 20 working days of '
    'this notice, you may',
    'be subject to enforcement actions as a result of your failure to obtain an '
    'operating permit as',
    'hold, under the authority of section 18(3) of the Act.',
    'notice to you. If you have already made payment to renew your operating '
    'permit, please disregard this notice.',
    'of Non-compliance',
    'operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, '
    'Mastercard, and Amex), cheques',
    'or may cancel or suspend any other certificate, license, permit or other '
    'permission you apply for or currently',
    'permit(s), please call our contact center at 1 866 566 7233.',
    'required by section 18 of the Safety Standards General Regulation.',
    'the Safety Standards Act, SBC 2003, c. 39 (the "Act").'
}


PHRASES_AR_OP_FINAL_NOTICE_CONSOLIDATED_LETTER = {
    '(attached to the renewal invoice).',
    '(made payable to Technical Safety BC), and money orders. If you have '
    'questions about this notice or your',
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 123456',
    'Act, SBC 2003, c. 39 (the "Act"). A record has been created with our '
    'Compliance and Enforcement team',
    'As a result of the failure to comply with the Final Warning Notice we have '
    'sent you regarding your',
    'As you do not have a current operating permit you are in breach of your '
    'obligations under the Safety Standards',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Electrical operating permit(s).',
    'FRM-1627',
    'Final Notice Operating Permit Renewal',
    'Operating permits will be issued upon receipt of payment and signed FSR '
    'Verification form for',
    'Page 1 of 2',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take further notice that, because of your non-compliant status, a Safety '
    'Officer or Safety Manager may refuse',
    'The following Operating Permit(s) below are expired. To renew operating '
    'permit(s), please remit the total',
    'VANCOUVER BC V8V 8V8',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" to renew your',
    'amount due. For Electrical operating permits, please also submit the '
    'Operating Permit-FSR Verification form',
    'currently hold, under the authority of section 18(3) of the Act.',
    'immediate compliance and enforcement action.',
    'operating permit or by calling 1 866 566 7233. We accept credit cards (Visa, '
    'Mastercard, and Amex), cheques',
    'operating permit(s) which is expired over 150 days, please be advised that '
    'you may be subject to',
    'permit(s), please call our contact center at 1 866 566 7233.',
    'regarding your account and they will be in contact with you directly '
    'shortly.',
    'to issue or may cancel or suspend any other certificate, license, permit or '
    'other permission you apply for or'
}


PHRASES_AR_GEN_PAST_DUE_CONSOLIDATED_LETTER = {
    '$0.00',
    '$1,000.00',
    '$2,500.00',
    '$200.00',
    '$3,300.00',
    '$800.00',
    '00345678',
    '00345689',
    '123 SOME STREET',
    '566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made '
    'payable to Technical Safety',
    '866 566 7233.',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'BC), and money orders. If you have questions about this notice or your '
    'permit(s), call our contact center at 1',
    'Due Date',
    'FRM-1628',
    'Failure to make immediate payment may result in collections action being '
    'taken against you. Take further',
    'For fast, easy payment, use our online services! Login with your online '
    'account details or register for an online',
    'If you have already made payment or have requested an adjustment to your '
    'account that has not been',
    'Invoice Total',
    'Our records indicate that you have failed to make payments for the invoices '
    'listed below. Your invoices are now',
    'Page 1 of 1',
    'Past Due Invoice Number',
    'Past Due Summary Notice',
    'Payments/Adjustment Credits',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Total Amount Due',
    'Total amount due for all invoices',
    'Upon Receipt',
    'VANCOUVER BC V8V 8V8',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" or by calling 1 866',
    'account by emailing us at clientportal@technicalsafetybc.ca .',
    'notice that, because of your failure to pay money owed under the Act, a '
    'Safety Officer or Safety Manager may',
    'or currently hold, under authority of section 18.1(1) of the Act.',
    'past due and you were required to make payment for these invoices upon '
    'receipt. The amount on this',
    'processed, please disregard this notice.',
    'refuse to issue or may cancel or suspend any other certificate, license, '
    'permit or other permission you apply for',
    'statement is a debt owing to Technical Safety BC.'
}


PHRASES_AR_GEN_DEMAND_CONSOLIDATED_LETTER = {
    '123 SOME STREET',
    '866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques '
    '(made payable to Technical',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'BC.',
    'Demand Summary Notice',
    'FRM-1629',
    'Further to our Past Due Summary notice, our records still indicate that you '
    'have failed to make',
    'If you have already made payment or have requested an adjustment to your '
    'account that has not been',
    'Manager may refuse to issue or may cancel or suspend any other certificate, '
    'license, permit or other',
    'Page 1 of 2',
    'Safety BC), and money orders. If you have questions about this notice or '
    'your permit(s), call our contact center',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take further notice that, because of your failure to pay money owed under '
    'the Act, a Safety Officer or Safety',
    'Take notice that you are required to make immediate payment of this account. '
    'If we fail to receive your',
    'VANCOUVER BC V8V 8V8',
    'You may make payment online by going to www.technicalsafetybc.ca and click '
    '"Pay an Invoice" or by calling 1',
    'at 1 866 566 7233.',
    'make payment for this amount upon receipt. The amount on this statement is a '
    'debt owing to Technical Safety',
    'payment by within 30 days of this, you may be subject to collections action '
    'or we may pursue a claim against',
    'payments for the invoices listed below. Your account balance of $3,300.00 is '
    'overdue. You are required to',
    'permission you apply for or currently hold, under authority of section '
    '18.1(1) of the Act.',
    'processed, please disregard this notice.',
    'you in the Courts of British Columbia.'
}


PHRASES_AR_GEN_FINAL_WARNING_CONSOLIDATED_LETTER = {
    '123 SOME STREET',
    '866 566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques '
    '(made payable to Technical',
    'ATTN: John Smith',
    'Account Number: 123456',
    'Act, RSBC 1996, c. 78.',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'BC.',
    'FRM-1630',
    'Final Warning Summary Notice',
    'Further to our Demand Summary notice, our records still indicate that you '
    'have failed to make',
    'Page 1 of 2',
    'Please note that should we fail to receive your payment within the next 20 '
    'working days of this',
    'Safety BC), and money orders. If you have questions about this notice or '
    'your permit(s), call our contact center',
    'Should we fail to receive a response from you by the timeline herein, we '
    'will be taking further action without',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take notice that, because of your non-compliant status, a Safety Officer or '
    'Safety Manager may refuse to issue',
    'VANCOUVER BC V8V 8V8',
    'We reserve the right to pursue a claim against you in the Courts of British '
    'Columbia to recover the amount of',
    'You may make payment online by going to www.technicalsafetybc.ca and click '
    '"Pay an Invoice" or by calling 1',
    'at 1 866 566 7233.',
    'hold, under the authority of section 18.1(1) of the Act.',
    'make payment for this amount upon receipt. The amount on this statement is a '
    'debt owing to Technical Safety',
    'notice to you. If you have already made payment, please disregard this '
    'notice.',
    'notice, your invoice will be sent to a third party collections agency for '
    'further action.',
    'or may cancel or suspend any other certificate, license, permit or other '
    'permission you apply for or currently',
    'payment for invoices listed below. Your account balance of $3,300.00 is '
    'overdue. You are required to',
    'this debt and to seek all available remedies including seizure and sale '
    'pursuant to the Court Order Enforcement'
}


PHRASES_AR_GEN_FINAL_NOTICE_CONSOLIDATED_LETTER = {
    '$0.00',
    '$1,000.00',
    '$2,500.00',
    '$200.00',
    '$3,300.00',
    '$800.00',
    '00345678',
    '00345689',
    '123 SOME STREET',
    '566 7233. We accept credit cards (Visa, Mastercard, and Amex), cheques (made '
    'payable to Technical Safety',
    '866 566 7233.',
    'ATTN: John Smith',
    'Account Number: 123456',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'BC), and money orders. If you have questions about this notice or your '
    'permit(s), call our contact center at 1',
    'Due Date',
    'FRM-1631',
    'Final Notice Summary',
    'For fast, easy payment, use our online services! Login with your online '
    'account details or register for an online',
    'Further to our Final Warning Summary notice, our records still indicate that '
    'you have failed to',
    'Invoice Total',
    'Page 1 of 1',
    'Past Due Invoice Number',
    'Payments/Adjustment Credits',
    'Should we fail to receive a response from you by the timeline herein, we '
    'will be taking further action without',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Take notice that, because of your non-compliant status, a Safety Officer or '
    'Safety Manager may',
    'Technical Safety BC.',
    'Total Amount Due',
    'Total amount due for all invoices',
    'Upon Receipt',
    'VANCOUVER BC V8V 8V8',
    'You may make payment by going to www.technicalsafetybc.ca and click "Pay an '
    'Invoice" or by calling 1 866',
    'account by emailing us at clientportal@technicalsafetybc.ca .',
    'are required to make payment for this amount upon receipt. The amount on '
    'this statement is a debt owing to',
    'make payments for the invoices listed below. Your account balance of '
    '$3,300.00 is overdue. You',
    'notice to you. If you have already made payment, please disregard this '
    'notice.',
    'refuse to issue or may cancel or suspend any other certificate, license, '
    'permit or other permission',
    'you apply for or currently hold, under the authority of section 18.1(1) of '
    'the Act.'
}


PHRASES_INSPECTION_NC_FRIENDLY_REMINDER_CONSOLIDATED_LETTER = {
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 1122334455',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Dear John Smith,',
    'FRM-1632',
    'Further to our certificate of inspection(s) issued regarding the '
    'assessment(s) performed at your site(s),',
    'If you have any questions regarding this notification, please contact us '
    'directly via your online account, via',
    'In accordance with s. 20(3) of the Safety Standards General Regulation , you '
    'are required to correct any',
    'Inspection Non-compliances Friendly Reminder',
    'Notice',
    'Page 1 of 4',
    'Please submit your declaration to confirm that the non-compliances below '
    'have been resolved by the required',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Technical Safety BC',
    'Thank you in advance for your attention.',
    'VANCOUVER BC V8V 8V8',
    'and notify the safety officer that the corrections have been completed.',
    'compliances by the required due dates may result in compliance and '
    'enforcement action for breach of s. 20(3)',
    'due dates. You can submit your declaration via your online account. Failure '
    'to resolve assessed non-',
    'email at contact@technicalsafetybc.ca, or contact your safety officer '
    'directly.',
    'non-compliances with respect to regulated work or regulated product '
    'identified on a certificate of inspection',
    'of the Safety Standards General Regulation.',
    'please note that correction of your non-compliances are due as per the dates '
    'listed in the following notice.'
}


PHRASES_INSPECTION_NC_PAST_DUE_CONSOLIDATED_LETTER = {
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 1122334455',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Dear John Smith,',
    'FRM-1633',
    'Further to our Certificate of Inspection regarding the assessment performed '
    'at your site, please note that',
    'In accordance with s. 20(3) of the Safety Standards General Regulation , you '
    'are required to correct any',
    'Inspection Non-compliances Past Due Notice',
    'Our records indicate that you have not submitted a declaration to confirm '
    'that your non-compliances have',
    'Page 1 of 4',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Technical Safety BC',
    'Thank you in advance for your attention.',
    'VANCOUVER BC V8V 8V8',
    'You may be subject to compliance and enforcement action for failure to '
    'submit a declaration confirming',
    'and notify the safety officer that the corrections have been completed. You '
    'are now in breach of this',
    'been resolved by the required due dates nor have you submitted a request for '
    'an extension of time.',
    'correction of these non-compliances. Please submit your declaration as soon '
    'as possible. You can submit your',
    'correction of your non-compliances is now past due. You were issued '
    'certificate of inspection(s) that',
    'declaration directly by contacting our office or via your online account. We '
    'will be contacting you shortly to',
    'follow up on this notification.',
    'non-compliances with respect to regulated work or regulated product '
    'identified on a certificate of inspection',
    'required you to resolve non-compliances by due dates listed in the following '
    'notice.',
    'requirement.'
}


PHRASES_INSPECTION_NC_FINAL_WARNING_CONSOLIDATED_LETTER = {
    '123 SOME STREET',
    'ATTN: John Smith',
    'Account Number: 1122334455',
    'BC Safety Authority is now Technical Safety BC. While we have changed our '
    'name, we remain committed to our vision of Safe Technical',
    'Dear John Smith,',
    'FRM-1635',
    'Further to our INSPECTION NON-COMPLIANCES PAST DUE NOTICE regarding the '
    'assessment(s) performed',
    'In accordance with s. 20(3) of the Safety Standards General Regulation , you '
    'are required to correct any',
    'Inspection Non-compliances Final Warning Notice',
    'Page 1 of 6',
    'Please note that you may be subject to immediate compliance and enforcement '
    'action for failure to',
    'Some Company Inc.',
    'Suite 600 - 2889 East 12th Avenue Vancouver, BC V5M 4T5 T 1 866 566 7233 E '
    'contact@technicalsafetybc.ca www.technicalsafetybc.ca',
    'Systems. Everywhere. Learn more about our evolving services and how we share '
    'safety knowledge at www.technicalsafetybc.ca.',
    'Technical Safety BC',
    'Thank you in advance for your attention.',
    'VANCOUVER BC V8V 8V8',
    'account.',
    'and notify the safety officer that the corrections have been completed. You '
    'are now in breach of this',
    'at your site, our records indicate that you have not submitted a declaration '
    'to confirm that your non-',
    'compliances have been resolved by the required due date(s) nor have you '
    'submitted a request for an extension',
    'declare the completion of these non-compliances. Your file may be forwarded '
    'to compliance and',
    'enforcement for consideration of next steps without further warning to you. '
    'Submit your declaration',
    'non-compliances with respect to regulated work or regulated product '
    'identified on a certificate of inspection',
    'of time.',
    'or request for an extension of time as soon as possible. You can submit your '
    'declaration via your online',
    'requirement.'
}
