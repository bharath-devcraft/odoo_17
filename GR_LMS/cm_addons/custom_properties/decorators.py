# -*- coding: utf-8 -*-
from odoo import fields, _
from odoo.exceptions import UserError
from functools import wraps

import re


PATTERN : str = r'[!@#$%^&*()_+{}\[\]:;<>,.?\/\\~-]'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

def check_previous_entrydate(self, date):
    return bool(self.env[self._name].with_context(active_test=False).search([
              ('entry_date','>',date),('status','in',['approved']),('id','!=',self.id)]))

def is_future_date(date):
    return True if date > fields.Date.today() else False

def is_past_date(date):
    return True if date < fields.Date.today() else False

def is_special_char(env, text, skip_chars=None):
    if not skip_chars:
        skip_chars = env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.skip_chars')
    special_chars: str = PATTERN
    for char in skip_chars or []:
        special_chars = special_chars.replace(char, '')
    return bool(re.search(special_chars, text))

def is_negative(num):
    return True if num < 0 else False

def valid_mobile_no(char):
    return False if re.match("^((\+)?\d{10,15})$", char) == None else True

def check_age_below_eighteen(birth_date):
    """ Is age lesser than 18 means return True, Ex. format should be like --> 1999-11-09 """
    year, month, day = map(int, str(birth_date).split("-"))
    today = fields.Date.today()
    #24  = 2024 - 1999 - ((5, 28) < (11, 9)
    age : int = today.year - year - ((today.month, today.day) < (month, day))
    return True if age < 18 else False

def is_alphanum(text):
    return text.isalnum()
    
def valid_email(mail):
    return False if re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,6}$", mail) == None else True

def check_delete_access(user, record):
    return True if ((user.id == record.user_id.id\
		or record.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.del_self_draft_entry')\
		or user.has_group('cm_user_mgmt.group_mgmt_admin')) and\
		record.entry_mode == 'manual' and record.status == 'draft') else False

def validate_fax(fax_number):
    pattern = r"^(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
    return bool(re.match(pattern, fax_number))

def valid_website(url):
    pattern = r'www\.[\w-]{2,255}\.\w{2,6}(?:/\S*)?'
    return False if re.match(pattern, url) is None else True

def valid_gst_no(gst_num):
    regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"
    return bool(re.match(regex, gst_num))

def is_less_than_zero(value):
    return True if value <= 0 else False

def is_number(value):
    return value.isnumeric()

def valid_ifsc_code(code):
    regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
    return bool(re.match(regex, code))

def valid_pin_code(pin):
    return False if len(str(pin)) not in (5, 6, 7, 8, 9, 10) else True

def valid_pan_no(pan_no):
    pattern = r"^[A-Z]{5}\d{4}[A-Z]$"
    return False if not re.match(pattern, pan_no) else True

def valid_tan_no(tan_no):
    return False if len(tan_no) < 10 or len(tan_no) > 20 else True

def valid_cst_no(cst_no):
    return False if cst_no and (len(str(cst_no)) != 11 or not str(cst_no).isdigit()) else True

def valid_aadhaar_no(aadhaar_no):
    return False if (len(str(aadhaar_no)) != 12 or not str(aadhaar_no).isdigit()) else True

def valid_phone_no(phone_no):
    return True if (len(str(phone_no)) in (9, 10, 11, 12) and phone_no.isdigit() == True) else False

def valid_cin_no(cin_no):
    return False if cin_no and len(cin_no) != 21 else True

def valid_tin_no(tin_no):
    return False if len(tin_no) < 11 or len(tin_no) > 18 else True

def valid_account_no(account_no):
    return True if (8 <= len(account_no) <= 20 and account_no.isdigit()) else False

def is_alphabets(text):
    pattern = r"^[A-Za-z ]+$"
    return True if (re.match(pattern, text)) else False


def _check_c_rule(self_obj, field_name):
    return self_obj._fields[field_name].args and not self_obj._fields[field_name].args.get('c_rule')
    
def validation(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0] if args[0] else False
        warning_msg: list[str] = []
        if self:
            if self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.server_side_validation'):
                if 'delivery_date' in self._fields and _check_c_rule(self, 'delivery_date'):
                    if 'entry_date' in self._fields and self.delivery_date and self.entry_date:
                        if self.delivery_date < self.entry_date:
                           warning_msg.append(f"{self._fields.get('delivery_date').string} date should be greater than or equal to order date.")

                if 'from_date' in self._fields and 'to_date' in self._fields and _check_c_rule(self, 'from_date'):
                    if self.from_date and self.to_date:
                        if self.from_date > self.to_date:
                           warning_msg.append(f"{self._fields.get('from_date').string} should not be greater than to date")
                    
                if 'due_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'due_date'):
                    if self.due_date and self.entry_date:
                        if self.entry_date > self.due_date:  
                           warning_msg.append(f"{self._fields.get('due_date').string} should not be less than entry date")

                if 'vendor_inv_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'vendor_inv_date'):
                    if self.vendor_inv_date and self.entry_date:
                        if self.entry_date > self.vendor_inv_date:  
                           warning_msg.append(f"{self._fields.get('vendor_inv_date').string} should not be less than entry date")
            
                if 'quote_date' in self._fields and 'entry_date' in self._fields and self.quote_date\
                           and self.entry_date and _check_c_rule(self, 'quote_date'):
                    if self.entry_date < self.quote_date:  
                       warning_msg.append(f"{self._fields.get('quote_date').string} should not be greater than entry date")

                if 'ack_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'ack_date'):
                    if self.ack_date and self.entry_date:
                        if self.entry_date > self.ack_date:  
                           warning_msg.append(f"{self._fields.get('ack_date').string} should not be less than entry date")

                if 'ship_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'ship_date'):
                    if self.ship_date and self.entry_date:
                        if self.entry_date > self.ship_date:  
                           warning_msg.append(f"{self._fields.get('ship_date').string} should not be less than entry date")

                if 'enq_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'enq_date'):
                    if self.enq_date and self.entry_date:
                        if self.entry_date > self.enq_date:  
                           warning_msg.append(f"{self._fields.get('enq_date').string} should not be less than entry date")

                if 'customer_po_date' in self._fields and 'entry_date' in self._fields and _check_c_rule(self, 'customer_po_date'):
                    if self.customer_po_date and self.entry_date:
                        if self.entry_date < self.customer_po_date:  
                           warning_msg.append(f"{self._fields.get('customer_po_date').string} should not be greater than entry date")

                if 'relive_date' in self._fields and 'join_date' in self._fields and _check_c_rule(self, 'relive_date'):
                    if self.relive_date and self.join_date:
                        if self.join_date > self.relive_date:  
                           warning_msg.append(f"{self._fields.get('relive_date').string} should not be less than joining date")

                ## Future Date
                if 'entry_date' in self._fields and self.entry_date and _check_c_rule(self, 'entry_date'):
                    if is_future_date(self.entry_date):
                        warning_msg.append(f"{self._fields.get('entry_date').string} should not be greater than current date")

                if 'request_date' in self._fields and self.request_date and _check_c_rule(self, 'request_date'):
                    if is_future_date(self.request_date):
                        warning_msg.append(f"{self._fields.get('request_date').string} should not be greater than current date")

                if 'draft_date' in self._fields and self.draft_date and _check_c_rule(self, 'draft_date'):
                    if is_future_date(self.draft_date):
                        warning_msg.append(f"{self._fields.get('draft_date').string} should not be greater than current date")

                if 'ack_date' in self._fields and self.ack_date and _check_c_rule(self, 'ack_date'):
                    if is_future_date(self.ack_date):
                        warning_msg.append(f"{self._fields.get('ack_date').string} should not be greater than current date")

                if 'comply_date' in self._fields and self.comply_date and _check_c_rule(self, 'comply_date'):
                    if is_future_date(self.comply_date):
                        warning_msg.append(f"{self._fields.get('comply_date').string} should not be greater than current date")

                if 'receive_date' in self._fields and self.receive_date and _check_c_rule(self, 'receive_date'):
                    if is_future_date(self.receive_date):
                        warning_msg.append(f"{self._fields.get('receive_date').string} should not be greater than current date")

                if 'ship_date' in self._fields and self.ship_date and _check_c_rule(self, 'ship_date'):
                    if is_future_date(self.ship_date):
                        warning_msg.append(f"{self._fields.get('ship_date').string} should not be greater than current date")

                if 'enq_date' in self._fields and self.enq_date and _check_c_rule(self, 'enq_date'):
                    if is_future_date(self.enq_date):
                        warning_msg.append(f"{self._fields.get('enq_date').string} should not be greater than current date")

                if 'join_date' in self._fields and self.join_date and _check_c_rule(self, 'join_date'):
                    if is_future_date(self.join_date):
                        warning_msg.append(f"{self._fields.get('join_date').string} should not be greater than current date")

                if 'birth_date' in self._fields and self.birth_date and _check_c_rule(self, 'birth_date'):
                    if is_future_date(self.birth_date):
                        warning_msg.append(f"{self._fields.get('birth_date').string} should not be greater than current date")

                if 'dc_date' in self._fields and self.dc_date and _check_c_rule(self, 'dc_date'):
                    if is_future_date(self.dc_date):
                        warning_msg.append(f"{self._fields.get('dc_date').string} should not be greater than current date")



                ## Past Date
                if 'cheque_date' in self._fields and self.cheque_date and _check_c_rule(self, 'cheque_date'):
                    if is_past_date(self.cheque_date):
                        warning_msg.append(f"{self._fields.get('cheque_date').string} should not be less than current date")

                if 'clearing_date' in self._fields and self.clearing_date and _check_c_rule(self, 'clearing_date'):
                    if is_past_date(self.clearing_date):
                        warning_msg.append(f"{self._fields.get('clearing_date').string} should not be less than current date")

                if 'eff_from_date' in self._fields and self.eff_from_date and _check_c_rule(self, 'eff_from_date'):
                    if is_past_date(self.eff_from_date):
                        warning_msg.append(f"{self._fields.get('eff_from_date').string} should not be less than current date")

                if 'relive_date' in self._fields and self.relive_date and _check_c_rule(self, 'relive_date'):
                    if is_past_date(self.relive_date):
                        warning_msg.append(f"{self._fields.get('relive_date').string} should not be less than current date")

                if 'remind_date' in self._fields and self.remind_date and _check_c_rule(self, 'remind_date'):
                    if is_past_date(self.remind_date):
                        warning_msg.append(f"{self._fields.get('remind_date').string} should not be less than current date")

                if 'entry_date' in self._fields and _check_c_rule(self, 'entry_date'):
                    if 'draft_date' in self._fields and self.draft_date and self.entry_date:
                        if self.draft_date > self.entry_date:
                           warning_msg.append(f"{self._fields.get('entry_date').string} should not be less than draft date.")

                #Special character
                special_char_warning = "Special character is not allowed in"
                if 'quote_ref' in self._fields and self.quote_ref and _check_c_rule(self, 'quote_ref'):
                    if is_special_char(self.env, self.quote_ref):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('quote_ref').string}")

                if 'vendor_inv_no' in self._fields and self.vendor_inv_no and _check_c_rule(self, 'vendor_inv_no'):
                    if is_special_char(self.env, self.vendor_inv_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('vendor_inv_no').string}")

                if 'ref_no' in self._fields and self.ref_no and _check_c_rule(self, 'ref_no'):
                    if is_special_char(self.env, self.ref_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('ref_no').string}")

                if 'short_name' in self._fields and self.short_name and _check_c_rule(self, 'short_name'):
                    if is_special_char(self.env, self.short_name):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('short_name').string}")

                if 'ack_no' in self._fields and self.ack_no and _check_c_rule(self, 'ack_no'):
                    if is_special_char(self.env, self.ack_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('ack_no').string}")

                if 'cheque_favor' in self._fields and self.cheque_favor and _check_c_rule(self, 'cheque_favor'):
                    if is_special_char(self.env, self.cheque_favor):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('cheque_favor').string}")

                if 'tin_no' in self._fields and self.tin_no and _check_c_rule(self, 'tin_no'):
                    if not valid_tin_no(self.tin_no):
                       warning_msg.append(f"Invalid {self._fields.get('tin_no').string}. Please enter the correct {self._fields.get('tin_no').string}")

                if 'pan_no' in self._fields and self.pan_no and _check_c_rule(self, 'pan_no'):
                    if is_special_char(self.env, self.pan_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('pan_no').string}")

                if 'cst_no' in self._fields and self.cst_no and _check_c_rule(self, 'cst_no'):
                    if is_special_char(self.env, self.cst_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('cst_no').string}")

                if 'vat_no' in self._fields and self.vat_no and _check_c_rule(self, 'vat_no'):
                    if is_special_char(self.env, self.vat_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('vat_no').string}")

                if 'gst_no' in self._fields and self.gst_no and _check_c_rule(self, 'gst_no'):
                    if is_special_char(self.env, self.gst_no):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('gst_no').string}")

                if 'contact_person' in self._fields and self.contact_person and _check_c_rule(self, 'contact_person'):
                    if is_special_char(self.env, self.contact_person):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('contact_person').string}")

                if 'branch_name' in self._fields and self.branch_name and _check_c_rule(self, 'branch_name'):
                    if is_special_char(self.env, self.branch_name):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('contact_person').string}")

                if 'bank_name' in self._fields and self.bank_name and _check_c_rule(self, 'bank_name'):
                    if is_special_char(self.env, self.bank_name):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('bank_name').string}")

                if 'acc_holder_name' in self._fields and self.acc_holder_name and _check_c_rule(self, 'acc_holder_name'):
                    if is_special_char(self.env, self.acc_holder_name):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('acc_holder_name').string}")

                if 'landmark' in self._fields and self.landmark and _check_c_rule(self, 'landmark'):
                    if is_special_char(self.env, self.landmark):
                       warning_msg.append(f"{special_char_warning} {self._fields.get('landmark').string}")

                num_only_warning = "Numbers only allowed in"
                if 'disc_amt' in self._fields and self.disc_amt and _check_c_rule(self, 'disc_amt'):
                    if is_negative(self.disc_amt):
                        warning_msg.append("Negative value is not allowed in %s"%(self._fields.get('disc_amt').string))

                if 'disc_per' in self._fields and self.disc_per and _check_c_rule(self, 'disc_per'):
                    if is_negative(self.disc_per):
                        warning_msg.append("Negative value is not allowed in %s"%(self._fields.get('disc_per').string))

                if 'mobile_no' in self._fields and self.mobile_no and _check_c_rule(self, 'mobile_no'):
                    if not valid_mobile_no(self.mobile_no):
                        warning_msg.append(f"{num_only_warning} {self._fields.get('mobile_no').string}")

                if 'mobile_no1' in self._fields and self.mobile_no1 and _check_c_rule(self, 'mobile_no1'):
                    if not valid_mobile_no(self.mobile_no1):
                       warning_msg.append(f"{num_only_warning} {(self._fields.get('mobile_no1').string)}")

                if 'phone_no' in self._fields and self.phone_no and _check_c_rule(self, 'phone_no'):
                    if not valid_phone_no(self.phone_no):
                       warning_msg.append(f"{(self._fields.get('phone_no').string)} is invalid.Please enter the correct {(self._fields.get('phone_no').string)} with SDD code")

                #Age
                if 'birth_date' in self._fields and self.birth_date and _check_c_rule(self, 'birth_date'):
                    if check_age_below_eighteen(self.birth_date): 
                        warning_msg.append("Age must above 18 in %s"%(self._fields.get('birth_date').string))

            if 'request_date' in self._fields and _check_c_rule(self, 'request_date'):
                if check_previous_entrydate(self, self.request_date):
                    warning_msg.append(f"{self._fields.get('request_date').string} should not be less than previous approved entry date")

            if 'draft_date' in self._fields and _check_c_rule(self, 'draft_date'):
                if check_previous_entrydate(self, self.draft_date):
                    warning_msg.append(f"{self._fields.get('draft_date').string} should not be less than previous approved entry date")

            if 'dc_date' in self._fields and _check_c_rule(self, 'dc_date'):
                if check_previous_entrydate(self, self.dc_date):
                    warning_msg.append(f"{self._fields.get('dc_date').string} should not be less than previous approved entry date")

            if 'remind_date' in self._fields and _check_c_rule(self, 'remind_date'):
                if check_previous_entrydate(self, self.remind_date):
                    warning_msg.append(f"{self._fields.get('remind_date').string} should not be less than previous approved entry date")

            #Alpha-num
            if 'gst_no' in self._fields and self.gst_no and _check_c_rule(self, 'gst_no'):
                if not is_alphanum(self.gst_no):
                    warning_msg.append(f"Only alphabet(a-z) and numbers(0-9) only allowed in {self._fields.get('gst_no').string}")

            #Email
            if 'email' in self._fields and self.email and _check_c_rule(self, 'email'):
                if not valid_email(self.email):
                    warning_msg.append("Email is not valid, check the given email")

            if 'from_mail_id' in self._fields and self.from_mail_id and _check_c_rule(self, 'from_mail_id'):
                if not valid_email(self.from_mail_id):
                    warning_msg.append("From mail is not valid, check the given from mail")

            if 'mail_bcc' in self._fields and self.mail_bcc and _check_c_rule(self, 'mail_bcc'):
                if not valid_email(self.mail_bcc):
                    warning_msg.append(f"{self._fields.get('mail_bcc').string} is not valid, check the given {self._fields.get('mail_bcc').string}")

            if 'mail_cc' in self._fields and self.mail_cc and _check_c_rule(self, 'mail_cc'):
                if not valid_email(self.mail_cc):
                    warning_msg.append(f"{self._fields.get('mail_cc').string} is not valid, check the given {self._fields.get('mail_cc').string}")

            if 'mail_to' in self._fields and self.mail_to and _check_c_rule(self, 'mail_to'):
                if not valid_email(self.mail_to):
                    warning_msg.append(f"{self._fields.get('mail_to').string} is not valid, check the given {self._fields.get('mail_to').string}")

            if 'mail_from' in self._fields and self.mail_from and _check_c_rule(self, 'mail_from'):
                if not valid_email(self.mail_from):
                    warning_msg.append(f"{self._fields.get('mail_from').string} is not valid, check the given {self._fields.get('mail_from').string}")

            if 'ifsc_code' in self._fields and self.ifsc_code and _check_c_rule(self, 'ifsc_code'):
                if not valid_ifsc_code(self.ifsc_code):
                   warning_msg.append(f"{self._fields.get('ifsc_code').string} is not valid, check the given {self._fields.get('ifsc_code').string}")

            if 'website' in self._fields and self.website and _check_c_rule(self, 'website'):
                if not valid_website(self.website):
                    warning_msg.append(f"{self._fields.get('website').string} is not valid, check the given {self._fields.get('website').string}")
	   
            if 'gst_no' in self._fields and self.gst_no and _check_c_rule(self, 'gst_no'):
                if not valid_gst_no(self.gst_no):
                    warning_msg.append(f"{self._fields.get('gst_no').string} is not valid, check the given {self._fields.get('gst_no').string}")

            if 'qty' in self._fields and _check_c_rule(self, 'qty'):
                if is_less_than_zero(self.qty):
                    warning_msg.append(f"{self._fields.get('qty').string} must be grater than zero.")

            if 'pin_code' in self._fields and self.pin_code and _check_c_rule(self, 'pin_code'):
                if not valid_pin_code(self.pin_code):
                    warning_msg.append(f"Invalid {self._fields.get('pin_code').string}. Please enter the correct {self._fields.get('pin_code').string}.")

            if 'pan_no' in self._fields and self.pan_no and _check_c_rule(self, 'pan_no'):
                if not valid_pan_no(self.pan_no):
                    warning_msg.append(f"Invalid {self._fields.get('pan_no').string}.Please enter the correct {self._fields.get('pan_no').string}")
                    
            if 'tan_no' in self._fields and self.tan_no and _check_c_rule(self, 'tan_no'):
                if not valid_tan_no(self.tan_no):
                    warning_msg.append(f"Invalid {self._fields.get('tan_no').string}.Please enter the correct {self._fields.get('tan_no').string}")

            if 'cst_no' in self._fields and self.cst_no and _check_c_rule(self, 'cst_no'):
                if not valid_cst_no(self.cst_no):
                    warning_msg.append(f"Invalid {self._fields.get('cst_no').string}.Please enter the correct {self._fields.get('cst_no').string}")
                    
            if 'cin_no' in self._fields and self.cin_no and _check_c_rule(self, 'cin_no'):
                if not valid_cin_no(self.cin_no):
                    warning_msg.append(f"Invalid {self._fields.get('cin_no').string}.Please enter the correct {self._fields.get('cin_no').string}")

            if 'account_no' in self._fields and self.account_no and _check_c_rule(self, 'account_no'):
                if not valid_account_no(self.account_no):
                    warning_msg.append(f"Invalid {self._fields.get('account_no').string}.Please enter the correct {self._fields.get('account_no').string}")
                    
            if 'bank_name' in self._fields and self.bank_name and _check_c_rule(self, 'bank_name'):
                if not is_alphabets(self.bank_name):
                    warning_msg.append(f"Invalid {self._fields.get('bank_name').string}.{self._fields.get('bank_name').string} should only contain alphabets")
                    
            if 'branch_name' in self._fields and self.branch_name and _check_c_rule(self, 'branch_name'):
                if not is_alphabets(self.branch_name):
                    warning_msg.append(f"Invalid {self._fields.get('branch_name').string}.{self._fields.get('branch_name').string} should only contain alphabets")
            #Digits
            if 'aadhaar_no' in self._fields and self.aadhaar_no and _check_c_rule(self, 'aadhaar_no'):
                if not valid_aadhaar_no(self.aadhaar_no):
                    warning_msg.append(f"Invalid {self._fields.get('aadhaar_no').string}.Please enter the correct {self._fields.get('aadhaar_no').string}")

        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(_(formatted_messages))
        return method(*args, **kwargs)
    return wrapper
