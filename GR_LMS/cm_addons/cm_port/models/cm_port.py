# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char,valid_pin_code,valid_mobile_no,valid_email,valid_phone_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_PORT = 'cm.port'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('blacklist', 'Blacklist'),
        ('suspension', 'Suspension'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

PORT_CATEGORY = [('seaport', 'Seaport'), ('airport', 'Airport'), ('dry_port', 'Dry(ICD) Port')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

AGENT_TYPE = [('internal', 'Internal'), ('external', 'External'), ('no_agent', 'No Agent')]

LOCATION = [('pan_india', 'PAN India'), ('exim', 'Exim(Global)')]

class CmPort(models.Model):
    _name = 'cm.port'
    _description = 'Port'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 5 char is allowed and will accept upper case only", size=5, c_rule=True)
    bus_location = fields.Selection(selection=LOCATION, string="Location", copy=False)
    edi_code = fields.Char(string="EDI Code", index=True, copy=False, size=252)
    port_category = fields.Selection(selection=PORT_CATEGORY, string="Port Category", copy=False)
    icd_connected = fields.Selection(selection=YES_OR_NO, string="Is ICD Connected", copy=False)
    icdport_id = fields.Many2one(CM_PORT, string="ICD Port Name", copy=False, ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port')]")
    sea_connected = fields.Selection(selection=YES_OR_NO, string="Is Seaport Connected", copy=False)
    seaport_id = fields.Many2one(CM_PORT, string="Seaport Name", copy=False, ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'seaport')]")
    free_zone = fields.Selection(selection=YES_OR_NO, string="Is Free Zone Port", copy=False)
    sanctioned_port = fields.Selection(selection=YES_OR_NO, string="Sanctioned Port", copy=False, default='yes')
    agent_type = fields.Selection(selection=AGENT_TYPE, string="Agent Type", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customs_note = fields.Text(string="Customs Notes", copy=False)
    sec_msure_note = fields.Text(string="Security Measure Notes", copy=False)
    port_auth_regul = fields.Text(string="Port Authority Regulations", copy=False)
    discount_provision = fields.Selection(selection=YES_OR_NO, string="Discount Provision", copy=False)
    emergency_plan = fields.Selection(selection=YES_OR_NO, string="Emergency Plan", copy=False)

    contact_person = fields.Char(string="Contact Person", size=50)
    designation = fields.Char(string="Designation", copy=False, size=50)
    mobile_no = fields.Char(string="Mobile No", copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)
    email = fields.Char(string="Email", copy=False, size=252)
    skype = fields.Char(string="Skype ID", copy=False, size=50)
    fax = fields.Char(string="Fax", copy=False, size=12)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one('cm.city', string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")

    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])


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

    line_ids = fields.One2many('cm.port.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.port.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in port name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_port where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Port name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env, self.short_name):
                raise UserError(_("Special character is not allowed in port code field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_port where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Port code must be unique"))

    @api.constrains('edi_code')
    def edi_code_validation(self):
        if self.edi_code:
            if is_special_char(self.env, self.edi_code):
                raise UserError(_("Special character is not allowed in EDI code field"))

            edi_code = self.edi_code.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(edi_code)
            from cm_port where upper(REPLACE(edi_code, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(edi_code, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Port EDI code must be unique"))

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

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        if self.mobile_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
                    raise UserError(_(f"Mobile number(IN) is  invalid. Please enter correct mobile number, Ref : {self.mobile_no}"))
            if not valid_mobile_no(self.mobile_no):
                raise UserError(_(f"Mobile number is  invalid. Please enter correct mobile number, Ref : {self.mobile_no}"))

    @api.constrains('whatsapp_no')
    def whatsapp_no_validation(self):
        if self.whatsapp_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.whatsapp_no)) == 10 and self.whatsapp_no.isdigit() == True):
                    raise UserError(_("WhatsApp number(IN) is invalid. Please enter correct whatsapp number"))
            if not valid_mobile_no(self.whatsapp_no):
                raise UserError(_("Whatsapp number is invalid. Please enter correct whatsapp number"))

    @api.constrains('email')
    def email_validation(self):
        if self.email and not valid_email(self.email):
            raise UserError(_(f"Email is invalid. Please enter the correct email, Ref : {self.email}"))
    
    @api.constrains('phone_no')
    def phone_validation(self):
        if self.phone_no and not valid_phone_no(self.phone_no):
            raise UserError(_(f"Landline No / Ext is invalid. Please enter the correct landline no / ext with sdd code, Ref : {self.phone_no}"))

    @api.constrains('street')
    def street_validation(self):
        if self.street and is_special_char(self.env,self.street):
            raise UserError(_("Special character is not allowed in address line 1 field"))                

    @api.constrains('street1')
    def street1_validation(self):
        if self.street1 and is_special_char(self.env,self.street1):
            raise UserError(_("Special character is not allowed in address line 2 field"))

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
    
    @api.onchange('port_category')
    def onchange_port_category(self):
        self.icd_connected = False
        self.icdport_id = False
        self.sea_connected = False
        self.seaport_id = False

    @api.onchange('icd_connected')
    def onchange_icd_connected(self):
        self.icdport_id = False

    @api.onchange('sea_connected')
    def onchange_sea_connected(self):
        self.seaport_id = False

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.currency_id = self.country_id.currency_id
        else:
            self.currency_id = False

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
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
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
        return super(CmPort, self).write(vals)
     
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
        
        cm_port = self.env[CM_PORT]
        result['all_draft'] = cm_port.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_port.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_port.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_port.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_port.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_port.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_port.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_port.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_port.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_port.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_port.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_port.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
