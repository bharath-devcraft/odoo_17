# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_phone_no, valid_email, valid_pin_code
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
CM_DEPORT_LOCATION='cm.depot.location'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('temporarily_closed', 'Temporarily Closed')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

CONTAINER_TYPE = [('tank_only', 'Tank Only'), ('dry', 'Dry'), ('all', 'All')]

CONTAINER_SIZE = [('20_teu', '20 TEU'), ('40_teu', '40 TEU'), ('both', 'Both')]

CARGO_CATEGORY = [('dg', 'DG'), ('non_dg', 'Non DG'), ('both', 'Both')]

PAVER_BLOCKED = [('full', 'Full'), ('partially', 'Partially')]

CONTRACT_TYPE = [('own', 'Own'), ('lease', 'Lease'), ('rent', 'Rent')]

RENTAL_TYPE = [('per_day', 'Per Day Basis'), ('container', ' Container Basis'), ('monthly', 'Monthly Basis')]

CONTRACT_AGREE = [('no_contract', 'No Contract'), ('active', 'Active'), ('expired', 'Expired')]


APPLICABLE_OPTION = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]

VALIDITY_RANGE = [('perpetual', 'Perpetual'), ('limited', 'Limited')]

WEEK_DAYS = [('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday')]

class CmDepotLocation(models.Model):
    _name = 'cm.depot.location'
    _description = 'Profile Master Template'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
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
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict',domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    designation = fields.Char(string="Designation", copy=False, size=50)
    skype = fields.Char(string="Skype ID", copy=False)

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    sun = fields.Boolean(string="Sun", copy=False, default=False)
    mon = fields.Boolean(string="Mon", copy=False, default=False)
    tue = fields.Boolean(string="Tue", copy=False, default=False)
    wed = fields.Boolean(string="Wed", copy=False, default=False)
    thu = fields.Boolean(string="Thu", copy=False, default=False)
    fri = fields.Boolean(string="Fri", copy=False, default=False)
    sat = fields.Boolean(string="Sat", copy=False, default=False)
    total_area = fields.Integer(string="Total Area(Sqft)", copy=False)
    operating_hrs_start = fields.Float(string="Operating Hrs Start", copy=False)
    operating_hrs_end = fields.Float(string="Operating Hrs End", copy=False)
    

    container_type = fields.Selection(selection=CONTAINER_TYPE, string="Container Type", copy=False)
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False)
    cargo_category = fields.Selection(selection=CARGO_CATEGORY, string="Cargo Category", copy=False) 
    paver_blocked = fields.Selection(selection=PAVER_BLOCKED, string="Paver Blocked", copy=False)
    package_deal = fields.Selection(selection=APPLICABLE_OPTION, string="Package Deal")
    surveillance_systems = fields.Selection(selection=YES_OR_NO, string="Surveillance Systems", copy=False)
    pub_transport_avl = fields.Selection(selection=YES_OR_NO, string="Public Transport Availability", copy=False)
    inv_track_sys = fields.Selection(selection=YES_OR_NO, string="Inventory Tracking System", copy=False)
    eva_procedure = fields.Selection(selection=YES_OR_NO, string="Evacuation Procedures", copy=False)
    waste_disp_procedure = fields.Selection(selection=YES_OR_NO, string="Waste Disposal Procedures", copy=False)
    steam_heat_fac = fields.Selection(selection=YES_OR_NO, string="Steam Heating Facility", copy=False)
    laden_storage_fac = fields.Selection(selection=YES_OR_NO, string="Laden Storage Facility", copy=False)
    degas_fac = fields.Selection(selection=YES_OR_NO, string="De-Gassing Facility", copy=False)
    halal_wash = fields.Selection(selection=YES_OR_NO, string="Halal Wash", copy=False)
    kosher_wash = fields.Selection(selection=YES_OR_NO, string="Kosher Wash", copy=False)
    emergency_plan = fields.Selection(selection=YES_OR_NO, string="Emergency Plan", copy=False)
    compt_cert = fields.Selection(selection=YES_OR_NO, string="Competence Certificate", copy=False)
    etp= fields.Selection(selection=YES_OR_NO, string="ETP( Effluent Treatment Plants )", copy=False)
    other_facility = fields.Char(string="Other Facility", copy=False, size=252)

    periodic_audit = fields.Selection(selection=APPLICABLE_OPTION, string="Periodic Audit", copy=False)
    interval = fields.Integer(string="Interval(Months)", copy=False)    
    last_audit_date = fields.Date(string="Last Audit Date", copy=False)
    next_audit_date = fields.Date(string="Next Audit Date", copy=False)
    escalation_days = fields.Integer(string="Escalation Days", copy=False, default=15)
    attachment_ids = fields.Many2many('ir.attachment', string="Latest Audit Report", ondelete='restrict', check_company=True)

    contract_type = fields.Selection(selection=CONTRACT_TYPE, string="Contract Type", copy=False)
    rental_type = fields.Selection(selection=RENTAL_TYPE, string="Rental Type")
    contract_agree = fields.Selection(selection=CONTRACT_AGREE, string="Maintenance Contract", copy=False, c_rule=True)
    lease_duration = fields.Integer(string="Lease Duration(Months)", copy=False)
    ls_valid_from_date = fields.Date(string="Validity From Date", copy=False)
    ls_valid_to_date = fields.Date(string="Validity To Date", copy=False)
    valid_from_date = fields.Date(string="Validity From Date", copy=False)
    valid_to_date = fields.Date(string="Validity To Date", copy=False)
    rental_value = fields.Integer(string="Rental Value", copy=False)
    expiry_date = fields.Date(string="Expiry Date", copy=False)

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


    line_ids = fields.One2many('cm.depot.location.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.depot.location.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.depot.location.audit.checklist.line', 'header_id', string="Audit Checklist", copy=True, c_rule=True)
    line_ids_c = fields.One2many('cm.depot.location.nearby.port.details.line', 'header_id', string="Near By Ports", copy=True, c_rule=True)
    line_ids_d = fields.One2many('cm.depot.location.nearby.depot.locations.line', 'header_id', string="Near By Depots", copy=True, c_rule=True)
    
    @api.constrains('name','pin_code')
    def name_validation(self):
        if self.name and self.pin_code:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_depot_location where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s and pin_code = '%s'""" %(name, self.id,self.company_id.id,self.pin_code))
            if self.env.cr.fetchone():
                raise UserError(_("Depot Location name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_depot_location where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Depot location short name must be unique"))
        
    @api.constrains('phone_no')
    def phone_validation(self):
        if self.phone_no  and not valid_phone_no(self.phone_no):
           raise UserError(_("Landline No / Ext is invalid. Please enter the correctLandline No / Ext with SDD code"))

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
            
    @api.constrains('valid_from_date','valid_to_date')
    def validity_validations(self):
        if self.valid_from_date and self.valid_to_date and self.contract_agree == 'active':
            if self.valid_from_date > self.valid_to_date:
                raise UserError(_("Validity from date should be less than validity to date"))

    @api.constrains('ls_valid_from_date','ls_valid_to_date')
    def lease_validity_validations(self):
        if self.ls_valid_from_date and self.ls_valid_to_date and self.contract_type == 'lease':
            if self.ls_valid_from_date > self.ls_valid_to_date:
                raise UserError(_("Lease validity from date should be less than validity to date"))
            
    @api.constrains('last_audit_date','next_audit_date')
    def audit_date_validations(self):
        if self.last_audit_date and self.next_audit_date and self.periodic_audit == 'applicable':
            if self.last_audit_date > self.next_audit_date:
                raise UserError(_("Last audit date should be less than next audit date"))
    
    @api.onchange('contract_agree')
    def onchange_contract_agree(self):
        if self.contract_agree != 'active':
            self.valid_from_date = False
            self.valid_to_date = False
            
    @api.onchange('contract_type')
    def onchange_contract_type(self):
        if self.contract_type != 'lease':
            self.ls_valid_from_date = False
            self.ls_valid_to_date = False
            self.lease_duration = False
        if self.contract_type != 'rent':
            self.rental_type = False
            self.rental_value = False

    @api.onchange('periodic_audit')
    def onchange_periodic_audit(self):
        if self.periodic_audit != 'applicable':
            self.interval = False
            self.last_audit_date = False
            self.next_audit_date = False
            
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
        return super(CmDepotLocation, self).write(vals)
     
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
        
        
        cm_depot_location = self.env[CM_DEPORT_LOCATION]
        result['all_draft'] = cm_depot_location.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_depot_location.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_depot_location.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_depot_location.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_depot_location.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_depot_location.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_depot_location.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_depot_location.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_depot_location.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_depot_location.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_depot_location.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_depot_location.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
