# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_pan_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
CM_TRANSPORT_VENDOR='cm.transport.vendor'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('temporarily_blocked', 'Temporarily Blocked'),
        ('black_listed', 'Black Listed'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

ENTRY_MODE_OPTIONS = [('new', 'New'), ('name_change', 'Name Change')]

TYPE_OF_COMPANY_OPTION = [('private_Ltd', 'Private Ltd'),('public_ltd', 'Public Ltd')]

CONTRACT_STATUS = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

class CmTransportVendor(models.Model):
    _name = 'cm.transport.vendor'
    _description = 'Transport Vendor'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    entry_type = fields.Selection(selection=ENTRY_MODE_OPTIONS,default="new", string="Entry Type", copy=False, tracking=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    
    #Company Information
    type_of_company = fields.Selection(selection=TYPE_OF_COMPANY_OPTION, string="Type Of Company", copy=False)
    pan_no = fields.Char(string="PAN No", copy=False, size=10)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    msme_no = fields.Integer(string="MSME No", copy=False)
    iso_certified = fields.Selection(selection=YES_OR_NO, string="ISO Certified", copy=False)
    certification_no = fields.Char(string="Certification No", copy=False, size=15)
    no_of_employees = fields.Integer(string="No. Of Employees", copy=False)
    own_trailer_count = fields.Integer(string="Own Trailer Count", copy=False)
    attached_trailer_count = fields.Integer(string="Attached Trailer Count", copy=False)
    is_gps_enabled = fields.Selection(selection=YES_OR_NO, string="Is GPS Enabled", copy=False)
    dg_trained_drivers = fields.Selection(selection=YES_OR_NO, string="DG Trained Drivers", copy=False)
    driver_periodic_mhc = fields.Selection(selection=YES_OR_NO, string="Driver Periodic Health Checkup", copy=False)
    safty_tra_prog = fields.Selection(selection=YES_OR_NO, string="Safety Training Program", copy=False)
    ppe_kit = fields.Selection(selection=YES_OR_NO, string="PPE Kit In Vehicle", copy=False)
    first_aid_box_in_vehicle = fields.Selection(selection=YES_OR_NO, string="First Aid Box In Vehicle", copy=False)
    fire_ext = fields.Selection(selection=YES_OR_NO, string="Fire Extinguisher In Vehicle", copy=False)
    driver_mon_sys = fields.Selection(selection=YES_OR_NO, string="Driver Monitoring System", copy=False)
    own_parking_place = fields.Selection(selection=YES_OR_NO, string="Own Parking Place", copy=False)
    parking_name = fields.Text(string="Name Of The Parking Places", copy=False)
    depot_service = fields.Selection(selection=YES_OR_NO, string="Depot Service", copy=False)
    depot_vendor_id = fields.Many2one('cm.master', string="Deport Vendor Name", ondelete='restrict')

    #Contact Details
    contact_person = fields.Char(string="Contact Person", size=50)
    designation = fields.Char(string="Designation", size=252)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)    
    phone_no = fields.Char(string="Landline No / Ext", copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    skype = fields.Char(string="Skype ID", size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False,  ondelete='restrict', readonly=True, tracking=True)    

    #Business Information
    contract = fields.Selection(selection=CONTRACT_STATUS, string="Contract / Agreement", copy=False)
    validity_from_date = fields.Date(string="Validity From Date", copy=False)
    validity_to_date = fields.Date(string="Validity To Date", copy=False)
    
    same_as_bill_address = fields.Boolean(string="Same as Billing Address", default=False)

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

    line_ids = fields.One2many('cm.transport.vendor.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.transport.vendor.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.transport.vendor.billing.address.line', 'header_id', string="Billing Address", copy=True, c_rule=True)
    line_ids_c = fields.One2many('cm.transport.vendor.bank.details.line', 'header_id', string="Bank Details", copy=True, c_rule=True)
    line_ids_d = fields.One2many('cm.transport.vendor.client.details.line', 'header_id', string="Client Details", copy=True, c_rule=True)
    line_ids_e = fields.One2many('cm.transport.vendor.service.feedback.line', 'header_id', string="Service Feedback", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_transport_vendor where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Transport Vendor name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_transport_vendor where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Transport Vendor short name must be unique"))

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
            existing_record = self.env[CM_TRANSPORT_VENDOR].search_count([('pan_no', '=', self.pan_no),('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
            if existing_record:
                raise UserError(_("PAN number must be unique"))

    @api.constrains('gst_no')
    def gst_no_validation(self):
        if self.gst_no:
            if not valid_gst_no(self.gst_no):
                raise UserError(_("Invalid GST number. Please enter the correct GST number"))



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
                'fax': self.fax,
                'gst_no': self.gst_no,
            }
            billing_lines.append((0, 0, bill_values))
            self.line_ids_b = billing_lines
        else:
            self.line_ids_b = [(5, 0, 0)]

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
        return super(CmTransportVendor, self).write(vals)
     
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
        
        
        cm_transport_vendor = self.env[CM_TRANSPORT_VENDOR]
        result['all_draft'] = cm_transport_vendor.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_transport_vendor.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_transport_vendor.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_transport_vendor.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_transport_vendor.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_transport_vendor.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_transport_vendor.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_transport_vendor.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_transport_vendor.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_transport_vendor.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_transport_vendor.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_transport_vendor.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
