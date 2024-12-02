# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website, valid_tin_no, valid_pan_no, valid_tan_no, valid_cst_no,valid_aadhaar_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
CM_PROFILE_MASTER='cm.profile.master'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COMPANY_TYPE_OPTIONS = [('person', 'Individual'), ('company', 'Company')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

class CmProfileMaster(models.Model):
    _name = 'cm.profile.master'
    _description = 'Profile Master Template'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    

    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    landmark = fields.Char(string="Landmark", size=252)
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    
    tds = fields.Selection(selection=YES_OR_NO, string="TDS Applicable", copy=False)
    tan_no = fields.Char(string="TAN", size=20)
    cst_no = fields.Char(string="CST No", copy=False, size=20)
    tin_no = fields.Char(string="TIN No", copy=False, size=18)
    cheque_favor = fields.Char(string="Cheque In Favor Of", copy=False, size=252, tracking=True)
    company_type = fields.Selection(selection=COMPANY_TYPE_OPTIONS, string="Company Type", copy=False)
    pan_no = fields.Char(string="PAN No", copy=False, size=10)
    aadhaar_no = fields.Char(string="Aadhaar No", copy=False, size=12, tracking=True)
    gst_category = fields.Selection(selection=GST_OPTIONS, string="GST Category", copy=False)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    cin_no = fields.Char(string="CIN No", copy=False, size=21)
    same_as_bill_address = fields.Boolean(string="Same as Billing Address", default=False)
    same_as_del_address = fields.Boolean(string="Same as Delivery Address", default=False)

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


    line_ids = fields.One2many('cm.profile.master.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.profile.master.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.profile.master.billing.address.line', 'header_id', string="Billing Address", copy=True, c_rule=True)
    line_ids_c = fields.One2many('cm.profile.master.bank.details.line', 'header_id', string="Bank Details", copy=True, c_rule=True)
    line_ids_d = fields.One2many('cm.profile.master.delivery.address.line', 'header_id', string="Delivery Address", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_profile_master where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Profile master name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_profile_master where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Profile master short name must be unique"))
        
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

    @api.constrains('tin_no')
    def tin_no_validation(self):
        if self.tin_no:
            if not valid_tin_no(self.tin_no):
                raise UserError(_("Invalid TIN number. Please enter the correct TIN number"))
            rec_ids = self.env[CM_PROFILE_MASTER].with_context(active_test=False).search_count([('tin_no', '=', self.tin_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
            if rec_ids:
                raise UserError(_("TIN number must be Unique"))

    @api.constrains('pan_no')
    def pan_no_validation(self):
        if self.pan_no:
            if not valid_pan_no(self.pan_no):
                raise UserError(_("Invalid PAN number. Please enter the correct PAN number"))
            existing_record = self.env[CM_PROFILE_MASTER].search_count([('pan_no', '=', self.pan_no),('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
            if existing_record:
                raise UserError(_("PAN number must be unique"))

    @api.constrains('tan_no')
    def tan_no_validation(self):
        if self.tan_no:
            if not valid_tan_no(self.tan_no):
                raise UserError(_("Invalid TAN number. Please enter the correct TAN number"))
            if self.env[CM_PROFILE_MASTER].search_count([('tan_no', '=', self.tan_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)]):
                raise UserError(_("TAN number must be unique"))

    @api.constrains('cst_no')
    def cst_no_validation(self):
        if self.cst_no and not valid_cst_no(self.cst_no):
            raise UserError(_("Invalid CST number. Please enter the correct CST number"))

    @api.constrains('website')
    def website_validation(self):
        if self.website and not valid_website(self.website):
            raise UserError(_("Website is invalid. Please enter the correct website"))

    @api.constrains('aadhaar_no')
    def aadhaar_no_validation(self):
        if self.aadhaar_no:
            if not valid_aadhaar_no(self.aadhaar_no):
                raise UserError(_("Invalid Aadhaar number. Please enter the correct Aadhaar number"))
            if self.env[CM_PROFILE_MASTER].search_count([('aadhaar_no', '=', self.aadhaar_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)]):
                    raise UserError(_("Aadhaar number must be unique"))

    @api.constrains('gst_no')
    def gst_no_validation(self):
        if self.gst_no:
            if not valid_gst_no(self.gst_no):
                raise UserError(_("Invalid GST number. Please enter the correct GST number"))
            
            if self.gst_category == 'yes':
                existing_gst = self.env[CM_PROFILE_MASTER].search_count([('gst_no', '=', self.gst_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
                if existing_gst > 0:
                    raise UserError(_("GST number must be unique"))
    
    @api.constrains('cin_no')
    def cin_no_validation(self):
        if self.cin_no:
            if is_special_char(self.env,  self.cin_no):
                raise UserError(_(f"Special character is not allowed in CIN number field"))
            if ' ' in self.cin_no:
                raise UserError(_(f"Space is not allowed in CIN number field in delivery address tab, Ref: {self.cin_no}"))


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

    @api.onchange('same_as_bill_address')
    def onchange_same_as_bill_address(self):
        if self.same_as_bill_address:
            billing_lines = []
            bill_values = {
                'name': self.name,
                'short_name': self.short_name,
                'street': self.street,
                'street1': self.street1,
                'city_id': self.city_id.id,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
                'pin_code': self.pin_code,
                'email': self.email,
                'phone_no': self.phone_no,
                'fax': self.fax,
                'website': self.website,
                'gst_no': self.gst_no,
            }
            billing_lines.append((0, 0, bill_values))
            self.line_ids_b = billing_lines
        else:
            self.line_ids_b = [(5, 0, 0)]

    @api.onchange('same_as_del_address')
    def onchange_same_as_del_address(self):
        if self.same_as_del_address:
            delivery_lines = []
            del_values = {
                'name': self.name,
                'short_name': self.short_name,
                'street': self.street,
                'street1': self.street1,
                'city_id': self.city_id.id,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
                'pin_code': self.pin_code,
                'email': self.email,
                'phone_no': self.phone_no,
                'fax': self.fax,
                'website': self.website,
                'gst_no': self.gst_no,
            }
            delivery_lines.append((0, 0, del_values))
            self.line_ids_d = delivery_lines
        else:
            self.line_ids_d = [(5, 0, 0)]

    def validations(self):
        warning_msg = []
        if not self.line_ids:
            warning_msg.append("System not allow to approve with empty additional contact details")
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
        return super(CmProfileMaster, self).write(vals)
     
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
        
        
        cm_profile_master = self.env[CM_PROFILE_MASTER]
        result['all_draft'] = cm_profile_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_profile_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_profile_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_profile_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_profile_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_profile_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_profile_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_profile_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_profile_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_profile_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_profile_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_profile_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
