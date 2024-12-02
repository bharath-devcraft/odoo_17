# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_email, valid_pin_code, valid_aadhaar_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
CM_DRIVER_MASTER='cm.driver.master'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('restricted', 'Restricted')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

LICENSE_TYPE = [('lmv_tr', 'LMV-TR'),
                ('hmv_tr', 'HMV-TR'),
                ('both', 'Both')]

class CmDriverMaster(models.Model):
    _name = 'cm.driver.master'
    _description = 'Driver Master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    employee_code = fields.Char(string="Employee Code", size=50)
    name = fields.Char(string="Name", index=True, copy=False)
    birth_date = fields.Date(string="Date Of Birth", copy=False)
    join_date = fields.Date(string="Joining Date", copy=False, tracking=True)
    blood_group = fields.Char(string="Blood Group", size=252)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)    
    email = fields.Char(string="Email", copy=False, size=252)
    address_line_1 = fields.Char(string="Address Line 1", size=252)
    address_line_2 = fields.Char(string="Address Line 2", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    payroll_company_id = fields.Many2one('res.partner', string="Payroll Company", index=True, ondelete='restrict', tracking=True)
    driving_experience = fields.Integer(string="Driving Experience(Yrs.)", copy=False)
    vehicle_type_id = fields.Many2one('cm.vehicle.type', string="Vehicle Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    dg_trained_drivers = fields.Selection(selection=YES_OR_NO, string="DG Trained Drivers", copy=False)
    health_certificate = fields.Selection(selection=YES_OR_NO, string="Health Certificate", copy=False)
    health_insurance = fields.Selection(selection=YES_OR_NO, string="Health Insurance", copy=False)
    aadhaar_no = fields.Char(string="Aadhaar No", copy=False, size=12, tracking=True)
    monthly_salary = fields.Integer(string="Monthly Salary", copy=False)
    
    
    #License Details
    driver_lic_no = fields.Char(string="Driver License No", size=252)
    license_type = fields.Selection(selection=LICENSE_TYPE, string="License Type", copy=False, help="LMV-TR (Light Motor Vehicle - Transport)\n HMV-TR (Heavy Motor Vehicle - Transport)")
    lic_expire_date = fields.Date(string="License Expiry Date", copy=False)
    renewal_alert_days = fields.Integer(string="Renewal Alert(Days)", copy=False)
       
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    
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


    line_ids = fields.One2many('cm.driver.master.line', 'header_id', string="Additional Contact Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.driver.master.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.driver.master.health.history.line', 'header_id', string="Driver's Health History", copy=True, c_rule=True)
    line_ids_c = fields.One2many('cm.driver.master.lang.details.line', 'header_id', string="Language Details", copy=True, c_rule=True)

    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_driver_master where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Driver Master name must be unique"))

    @api.constrains('pin_code')
    def pin_code_validation(self):
        if self.pin_code:
            if self.country_id.code == 'IN':
                if not(len(str(self.pin_code)) == 6 and self.pin_code.isdigit() == True):
                    raise UserError(_("Invalid pin code(IN). Please enter the correct 6 digit pin code"))
            else:
                if not valid_pin_code(self.pin_code):
                    raise UserError(_("Invalid pin code. Please enter the correct pin code"))
                if is_special_char(self.env,self.pin_code):
                    raise UserError(_("Special character is not allowed in pin code field"))

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


    @api.constrains('aadhaar_no')
    def aadhaar_no_validation(self):
        if self.aadhaar_no and not valid_aadhaar_no(self.aadhaar_no):
            raise UserError(_("Invalid Aadhaar number. Please enter the correct Aadhaar number"))
        if self.env[CM_DRIVER_MASTER].search_count([('aadhaar_no', '=', self.aadhaar_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)]):
                raise UserError(_("Aadhaar number must be unique"))


    @api.constrains('line_ids','email','mobile_no')
    def contact_details_validations(self):
        mobile_nos = {self.mobile_no}
        emails = {self.email.replace(" ", "").upper() if self.email else self.email}
        for item in self.line_ids:
            if item.email:
                emails.add(item.email.replace(" ", "").upper())
            if item.mobile_no:
                mobile_nos.add(item.mobile_no)
        if self.mobile_no:
            if len(mobile_nos) < (1 + len([item for item in self.line_ids if item.mobile_no])):
                raise UserError(_("Duplicate mobile numbers are not allowed within the provided contact details"))
        if self.email:
            if len(emails) < (1 + len([item for item in self.line_ids if item.email])):
                raise UserError(_("Duplicate emails are not allowed within the provided contact details"))
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.country_id
        else:
            self.state_id = False
            self.country_id = False

    def validations(self):
        warning_msg = []
        if not self.line_ids:
            warning_msg.append("System not allow to approve with empty additional contact details")
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if self.line_ids_c:
            if not [line for line in self.line_ids_c if line.lang_read or line.lang_write or line.lang_speak if line.name]:
                warning_msg.append("Either one (Read or Write or Speck) is mandatory in Language Details")            
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
        return super(CmDriverMaster, self).write(vals)
     
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
        
        
        cm_driver_master = self.env[CM_DRIVER_MASTER]
        result['all_draft'] = cm_driver_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_driver_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_driver_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_driver_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_driver_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_driver_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_driver_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_driver_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_driver_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_driver_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_driver_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_driver_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
