# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char, valid_mobile_no, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_pan_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_BRANCH = 'cm.branch'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
CM_COUNTRY_CODE = 'cm.country.code'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmBranch(models.Model):
    _name = 'cm.branch'
    _description = 'Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Branch Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    description = fields.Char(string="Description", size=252)
    
    designation = fields.Char(string="Designation", size=50)
    skype = fields.Char(string="Skype ID", size=50)
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)    
    street = fields.Char(string="Street", size=252)
    street1 = fields.Char(string="Street1", size=252)    
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    city_id = fields.Many2one('cm.city', string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mb_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Mobile Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    wh_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Whatsapp Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ph_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Phone Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    same_as_mobile = fields.Boolean(string="Same as Mobile No", default=False, help="Click to apply same mobile number to whatsapp number")
    
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    pan_no = fields.Char(string="PAN No", copy=False, size=10)
    branch_country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    branch_country_code = fields.Char(string="Country Code", copy=False, size=252)
    branch_state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    branch_company_id = fields.Many2one(RES_COMPANY, string="Company", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True, readonly=True)
    sys_ref = fields.Char(string="System Ref", copy=False, size=252)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)

    line_ids = fields.One2many('cm.branch.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.branch.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_branch where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Branch name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env, self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_branch where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Branch short name must be unique"))
    
    @api.constrains('line_ids_a','email','mobile_no')
    def contact_details_validations(self):
        mobile_nos = {self.mobile_no}
        emails = {self.email.replace(" ", "").upper() if self.email else self.email}
        for item in self.line_ids_a:
            if item.email:
                emails.add(item.email.replace(" ", "").upper())
            if item.mobile_no:
                mobile_nos.add(item.mobile_no)
        if self.mobile_no:
            if len(mobile_nos) < (1 + len([item for item in self.line_ids_a if item.mobile_no])):
                raise UserError(_("Duplicate mobile numbers are not allowed within the provided contact details"))
        if self.email:
            if len(emails) < (1 + len([item for item in self.line_ids_a if item.email])):
                raise UserError(_("Duplicate emails are not allowed within the provided contact details"))
    
    @api.constrains('phone_no')
    def phone_validation(self):
        if self.phone_no  and not valid_phone_no(self.phone_no):
           raise UserError(_("Phone number is invalid. Please enter the correct phone number with SDD code"))

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        if self.mobile_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
                    raise UserError(_("Mobile number(IN) is invalid. Please enter correct mobile number"))
            if not valid_mobile_no(self.mobile_no):
                raise UserError(_("Mobile number is invalid. Please enter correct mobile number"))
                
    @api.constrains('whatsapp_no')
    def whatsapp_no_validation(self):
        if self.whatsapp_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.whatsapp_no)) == 10 and self.whatsapp_no.isdigit() == True):
                    raise UserError(_("Whatsapp number(IN) is invalid. Please enter correct whatsapp number"))
            if not valid_mobile_no(self.whatsapp_no):
                raise UserError(_("Whatsapp number is invalid. Please enter correct whatsapp number"))

    @api.constrains('email')
    def email_validation(self):
        if self.email  and not valid_email(self.email):
            raise UserError(_("Email is invalid. Please enter the correct email"))
    

    @api.constrains('street')
    def street_validation(self):
        if self.street and is_special_char(self.env,self.street):
            raise UserError(_("Special character is not allowed in street field"))                

    @api.constrains('street1')
    def street1_validation(self):
        if self.street1 and is_special_char(self.env,self.street1):
            raise UserError(_("Special character is not allowed in street1 field"))

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

    @api.constrains('gst_no')
    def gst_no_validation(self):
        if self.gst_no:
            if not valid_gst_no(self.gst_no):
                raise UserError(_("Invalid GST number. Please enter the correct GST number"))           
            
            existing_gst = self.env[CM_BRANCH].search_count([('gst_no', '=', self.gst_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
            if existing_gst > 0:
                raise UserError(_("GST number must be unique"))
    
    
    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code    
            self.city_id = False
            self.state_id = False
            record = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1)
            c_code = record.id if record else False
            self.mb_cc_id = c_code
            self.wh_cc_id = c_code
            self.ph_cc_id = c_code
            
        else:
            self.country_code = False
            self.city_id = False
            self.state_id = False
            self.mb_cc_id = False
            self.wh_cc_id = False
            self.ph_cc_id = False
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
        else:
            self.state_id = False
    
    @api.onchange('branch_country_id')
    def onchange_branch_country_id(self):
        if self.branch_country_id:
            self.branch_country_code = self.branch_country_id.code
            self.branch_state_id = False
        else:
            self.branch_country_code = False
    
    @api.onchange('branch_company_id')
    def onchange_branch_company_id(self):
        if self.branch_company_id:
            self.pan_no = self.branch_company_id.pan_no
        else:
            self.pan_no = False
            
    @api.onchange('same_as_mobile','mobile_no')
    def onchange_same_as_mobile(self):
        if self.same_as_mobile:
            self.whatsapp_no = self.mobile_no
        else:
            self.whatsapp_no = False
            
    @api.onchange('branch_state_id','pan_no')
    def onchange_gst_category(self):
        if self.branch_state_id and self.pan_no:
            print("!!!!!!!!!!!!!!!!!!!!!",self.branch_state_id)
            self.gst_no = str(self.branch_state_id.short_name) + str(self.pan_no)
        else:
            self.gst_no = False
    
	
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
        return super(CmBranch, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_branch = self.env[CM_BRANCH]
        result['all_draft'] = cm_branch.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_branch.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_branch.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_branch.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_branch.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_branch.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_branch.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_branch.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_branch.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_branch.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_branch.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_branch.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
