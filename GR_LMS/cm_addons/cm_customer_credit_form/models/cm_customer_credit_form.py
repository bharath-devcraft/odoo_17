# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website, valid_tin_no, valid_pan_no, valid_tan_no, valid_cst_no,valid_aadhaar_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
CM_CUSTOMER_CREDIT_FORM='cm.customer.credit.form'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
CM_CUSTOMER = 'cm.customer'
RES_CURRENCY = 'res.currency'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revised', 'Revised')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COMPANY_TYPE_OPTIONS = [('proprietary', 'Proprietary'), ('partnership', 'Partnership'), ('private', 'Private'), ('public_limited', 'Public Limited')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

INTEREST_CAL = [('from_invoice_date', 'From Invoice Date'), (' from_due_date', ' From Due Date')]
APPLICABLE_OPTION = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]


class CmCustomerCreditForm(models.Model):
    _name = 'cm.customer.credit.form'
    _description = 'Customer Credit Form'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True, copy=False)
    # short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    

    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    landmark = fields.Char(string="Landmark", size=252)
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    designation = fields.Char(string="Designation", copy=False, size=50)
    skype = fields.Char(string="Skype ID")
    currency_id = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    applied_on = fields.Date(string="Applied On")
    customer_id = fields.Many2one(CM_CUSTOMER, string="Customer Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    year_id = fields.Many2one('cm.calendar.year', string="Year Established", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    parent_company_id = fields.Many2one(CM_CUSTOMER, string="Parent Company", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customer_type_id = fields.Many2one('cm.customer.type', string="Customer Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customer_bus_act_id = fields.Many2many('cm.customer.business.activity', string="Customer's Business Activity", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])

    is_registered = fields.Selection(selection=YES_OR_NO, string="Is Registered Company", copy=False)
    pdc_waived = fields.Selection(selection=YES_OR_NO, string="PDC To Be Waived / Obtained", copy=False)
    security_chk_obt = fields.Selection(selection=YES_OR_NO, string="Security Cheque To Be Obtained / Waived", copy=False)
    cheque_bounced = fields.Selection(selection=YES_OR_NO, string="Has Party Cheque Bounced in Last 6 Months?", copy=False)
    paid_up_capital = fields.Float(string="Paid-up Capital", copy=False)
    proj_bus_volume = fields.Float(string="Projected Volume of Business", copy=False)
    

    credit_days = fields.Integer(string="Credit Days", copy=False)
    interest = fields.Integer(string="Interest(%)", default = 18)
    credit_limit = fields.Float(string="Number", copy=False)
    credit_agreement = fields.Selection(selection=APPLICABLE_OPTION, string="Credit Agreement", copy=False)
    credit_currency_id = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, tracking=True)
    interest_cal_date = fields.Selection(selection=INTEREST_CAL, string="Interest Calculation Date", copy=False)
    auto_draft_inv = fields.Selection(selection=YES_OR_NO, string="Automate Draft Invoice", copy=False)
    overdue_currency_id = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, tracking=True)

    cin_no = fields.Char(string="CIN No", copy=False, size=21)
    tax_reg_no = fields.Char(string="Tax Reg No(TRC)", copy=False, size=20)
    company_type = fields.Selection(selection=COMPANY_TYPE_OPTIONS, string="Company Type", copy=False)
    pan_no = fields.Char(string="PAN No", copy=False, size=10)

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True, readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)


    line_ids = fields.One2many('cm.customer.credit.form.line', 'header_id', string="Director Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.customer.credit.form.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_customer_credit_form where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Profile master name must be unique"))
        
    @api.constrains('phone_no')
    def phone_validation(self):
        if self.phone_no  and not valid_phone_no(self.phone_no):
           raise UserError(_("Landline No / Ext is invalid. Please enter the correct Landline No / Ext with SDD code"))

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        if self.mobile_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
                    raise UserError(_("Mobile number(IN) is invalid. Please enter correct mobile number"))
            if not valid_mobile_no(self.mobile_no):
                raise UserError(_("Mobile number is invalid. Please enter correct mobile number"))

    @api.constrains('email')
    def email_validation(self):
        if self.email  and not valid_email(self.email):
            raise UserError(_("Email is invalid. Please enter the correct email"))
    

    @api.constrains('street')
    def street_validation(self):
        if self.street and is_special_char(self.env,self.street):
            raise UserError(_("Special character is not allowed in Address Line 1 field"))                

    @api.constrains('street1')
    def street1_validation(self):
        if self.street1 and is_special_char(self.env,self.street1):
            raise UserError(_("Special character is not allowed in Address Line 2 field"))

    @api.constrains('pin_code')
    def pin_code_validation(self):
        if self.pin_code:
            if self.country_id.code == 'IN':
                if not(len(str(self.pin_code)) == 6 and self.pin_code.isdigit() == True):
                    raise UserError(_("Invalid zip code(IN). Please enter the correct 6 digit zip code"))
            else:
                if not valid_pin_code(self.pin_code):
                    raise UserError(_("Invalid zip code. Please enter the correct zip code"))
                if is_special_char(self.env,self.pin_code):
                    raise UserError(_("Special character is not allowed in zip code field"))

    @api.constrains('pan_no')
    def pan_no_validation(self):
        if self.pan_no:
            if not valid_pan_no(self.pan_no):
                raise UserError(_("Invalid PAN number. Please enter the correct PAN number"))
            existing_record = self.env[CM_CUSTOMER_CREDIT_FORM].search_count([('pan_no', '=', self.pan_no),('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
            if existing_record:
                raise UserError(_("PAN number must be unique"))


    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code
            self.city_id = False
            self.state_id = False
        else:
            self.country_code = False
            self.city_id = False
            self.state_id = False
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
        else:
            self.state_id = False
    
    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            self.name = self.customer_id.name
            self.year_id = self.customer_id.year_id
            self.parent_company_id = self.customer_id.parent_company_id
            self.company_type = self.customer_id.company_type
            self.customer_type_id = self.customer_id.customer_type_id
            self.is_registered = self.customer_id.is_registered
            self.cin_no = self.customer_id.cin_no
            self.tax_reg_no = self.customer_id.tax_reg_no
            self.pan_no = self.customer_id.pan_no

            self.contact_person = self.customer_id.contact_person
            self.designation = self.customer_id.designation
            self.mobile_no = self.customer_id.mobile_no
            self.whatsapp_no = self.customer_id.whatsapp_no
            self.phone_no = self.customer_id.phone_no
            self.email = self.customer_id.email
            self.skype = self.customer_id.skype
            self.fax = self.customer_id.fax
            self.street = self.customer_id.street
            self.street1 = self.customer_id.street1
            self.city_id = self.customer_id.city_id
            self.state_id = self.customer_id.state_id
            self.country_id = self.customer_id.country_id
            self.pin_code = self.customer_id.pin_code
        else:
            self.name = False
            self.year_id = False
            self.parent_company_id = False
            self.customer_type_id = False
            self.company_type = False
            self.is_registered = False
            self.cin_no = False
            self.tax_reg_no = False
            self.pan_no = False

            self.contact_person = False
            self.designation = False
            self.mobile_no = False
            self.whatsapp_no = False
            self.phone_no = False
            self.email = False
            self.skype = False
            self.fax = False
            self.street = False
            self.street1 = False
            self.city_id = False
            self.state_id = False
            self.country_id = False
            self.pin_code = False


    def validations(self):
        warning_msg = []
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(_(formatted_messages))

        return True

    @validation
    def entry_approve(self):
        if self.status in ('draft', 'editable'):
            self.validations()
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)})
        return True

    def entry_draft(self):
        if self.status == 'active':
            if not(self.env[RES_USERS].has_group('custom_properties.group_set_to_draft')):
                raise UserError(_("You can't draft this entry. Draft Admin have the rights"))
            self.write({'status': 'editable'})
        return True

    def entry_inactive(self):
        if self.status != 'active':
            raise UserError(_("Unable to inactive other than active entry"))

        remark = self.inactive_remark.strip() if self.inactive_remark else None

        if not remark:
            raise UserError(_("Inactive remarks is required. Please enter the remarks in the Inactive Remarks field"))

        min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
        if len(remark) < int(min_char):
            raise UserError(_(f"Minimum {min_char} characters are required for Inactive Remarks"))

        self.write({
            'status': 'inactive',
            'inactive_user_id': self.env.user.id,
            'inactive_date': time.strftime(TIME_FORMAT)})
        return True

    def unlink(self):
        for rec in self:
            if rec.status != 'draft' or rec.entry_mode == 'auto':
                raise UserError(_("You can't delete other than manually created draft entries"))
            if rec.status == 'draft':
                is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
                if not is_mgmt:
                    res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.del_self_draft_entry')
                    if not res_config_rule and self.user_id != self.env.user:
                        raise UserError(_("You can't delete other users draft entries"))
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CmCustomerCreditForm, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {
            'all_draft': 0,
            'all_active': 0,
            'all_inactive': 0,
            'all_editable': 0,
            'my_draft': 0,
            'my_active': 0,
            'my_inactive': 0,
            'my_editable': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0,
        }
        
        
        cm_customer_credit_form = self.env[CM_CUSTOMER_CREDIT_FORM]
        result['all_draft'] = cm_customer_credit_form.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_customer_credit_form.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_customer_credit_form.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_customer_credit_form.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_customer_credit_form.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_customer_credit_form.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_customer_credit_form.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_customer_credit_form.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_customer_credit_form.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_customer_credit_form.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_customer_credit_form.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_customer_credit_form.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
