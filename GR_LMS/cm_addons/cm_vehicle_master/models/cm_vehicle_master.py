# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_cin_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
RES_COMPANY = 'res.company'
IR_ATTACHMENT = 'ir.attachment'
CM_VEHICLE_MASTER='cm.vehicle.master'
CM_CITY = 'cm.city'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('not_in_use', 'Not In Use'),
        ('under_maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

GST_OPTIONS = [('registered', 'Registered'), ('un_registered', 'Un Registered')]

FUEL_TYPE_OPTION = [('diesel', 'Diesel'), ('petrol', 'Petrol'), ('gasoline', 'Gasoline'), ('electric', 'Electric')]

TRANSMISSION_OPTION = [('auto', 'Auto'), ('manual', 'Manual'), ('both', 'Both')]

AXLE_OPTION = [('single', 'Single'), ('multi', 'Multi'), ('double', 'Double'), ('Trible', 'Trible')]

APPLICABLE_OPTION = [('applicable', 'Applicable'),('not_applicable', 'Not Applicable')]
 
class CmVehicleMaster(models.Model):
    _name = 'cm.vehicle.master'
    _description = 'Vehicle Master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True, copy=False)    
    vehicle_type_id = fields.Many2one('cm.vehicle.type', string="Vehicle Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vehicle_make_id = fields.Many2one('cm.vehicle.make', string="Vehicle Make", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    model = fields.Integer(string="Model (Year)", copy=False)
    purchase_date = fields.Date(string="Purchase Date", copy=False)
    vehicle_age = fields.Integer(string="Vehicle Age", copy=False)
    engine_no = fields.Char(string="Engine No", size=252)
    chassis_no = fields.Char(string="Chassis Number", size=252)
    fuel_type = fields.Selection(selection=FUEL_TYPE_OPTION, string="Fuel Type", copy=False)
    transmission = fields.Selection(selection=TRANSMISSION_OPTION, string="Transmission", copy=False)
    axle = fields.Selection(selection=AXLE_OPTION, string="Axle", copy=False) 
    engine_capacity = fields.Integer(string="Engine Capacity", copy=False)
    vehicle_tare_weight = fields.Integer(string="Vehicle Tare Weight", copy=False)
    vehicle_gross_weight = fields.Integer(string="Vehicle Gross Weight", copy=False)
    standard_mileage = fields.Integer(string="Standard Mileage", copy=False)
    gps_enabled = fields.Selection(selection=YES_OR_NO, string="GPS Enabled", copy=False)
    location = fields.Char(string="Location", copy=False, size=50)    
    date_time = fields.Datetime(string="Date & Time", copy=False, readonly=True)    
    first_aid_box = fields.Selection(selection=YES_OR_NO, string="First Aid Box", copy=False)
    driver_mon_sys = fields.Selection(selection=YES_OR_NO, string="Driver Monitoring System", copy=False)
    fire_ext = fields.Selection(selection=YES_OR_NO, string="Fire Extinguisher In Vehicle", copy=False)
    ppe_kit = fields.Selection(selection=YES_OR_NO, string="PPE Kits In Vehicle", copy=False)
    diesel_tk_saft_gurd = fields.Selection(selection=YES_OR_NO, string="Diesel Tank Safety Guard", copy=False)
    battery_saft_gurd = fields.Selection(selection=YES_OR_NO, string="Battery Safety Guard", copy=False)
    spill_kit = fields.Selection(selection=YES_OR_NO, string="Spill Kit", copy=False)
    mudguard = fields.Selection(selection=YES_OR_NO, string="Mudguard", copy=False)
   

    #RC Account Details
    company_name_id = fields.Many2one(RES_COMPANY,string="Company Name", copy=False, ondelete='restrict')
    attachment_ids = fields.Many2many(IR_ATTACHMENT, string="RC Document", ondelete='restrict', check_company=True)
    
    #Insurance Details
    insurance = fields.Selection(selection=APPLICABLE_OPTION, string="Insurance", copy=False)
    ins_company_name = fields.Char(string="Insurance Company Name", size=252)
    from_date = fields.Date(string="From Date")
    validity_months = fields.Integer(string="Validity (Months)", copy=False)
    validity_days = fields.Integer(string="Validity (Days)", copy=False)
    to_date = fields.Date(string="To Date")
    ins_doc_ids = fields.Many2many(IR_ATTACHMENT,'insurance_doc_m2m', string="Insurance Doc 1", ondelete='restrict', check_company=True)
    other_doc_ids = fields.Many2many(IR_ATTACHMENT,'insurance_others_m2m', string="Others", ondelete='restrict', check_company=True)
    escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")

    #State Permit Details
    permit = fields.Selection(selection=APPLICABLE_OPTION, string="Permit", copy=False)
    state_from_date = fields.Date(string="From Date")
    state_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    state_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    state_to_date = fields.Date(string="To Date")
    permit_doc_ids = fields.Many2many(IR_ATTACHMENT,'permit_doc_m2m', string="Permit Certificate", ondelete='restrict', check_company=True)
    state_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'permit_others_m2m', string="Others", ondelete='restrict', check_company=True)
    state_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")
    
    #National Permit Details
    national_permit = fields.Selection(selection=APPLICABLE_OPTION, string="Permit", copy=False)
    national_from_date = fields.Date(string="From Date")
    nat_validity_month = fields.Integer(string="Validity (Months)", copy=False)
    nat_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    national_to_date = fields.Date(string="To Date")
    nat_doc_ids = fields.Many2many(IR_ATTACHMENT,'national_permit_doc_m2m', string="Permit Certificate", ondelete='restrict', check_company=True)
    nat_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'national_permit_others_m2m', string="Others", ondelete='restrict', check_company=True)
    nat_esc_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")    
    
    
    #Fitness Details(FC)
    fc = fields.Selection(selection=APPLICABLE_OPTION, string="FC", copy=False)
    last_fc_date = fields.Date(string="Last FC Date")
    fc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    fc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    next_fc_date = fields.Date(string="Next FC Date")
    next_inspection_date = fields.Date(string="Next Inspection Date")
    fc_doc_ids = fields.Many2many(IR_ATTACHMENT,'fc_certificate_ids_doc_m2m', string="FC Certificate", ondelete='restrict', check_company=True)
    fc_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'fc_oth_doc_ids_m2m', string="Others", ondelete='restrict', check_company=True)
    fc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")

    #Road Tax Details
    road_tax = fields.Selection(selection=APPLICABLE_OPTION, string="Road Tax", copy=False) 
    road_tax_paid_date = fields.Date(string="Road Tax Paid Date")
    rt_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    rt_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    rt_validity_to_date = fields.Date(string="Validity To Date")
    road_tax_doc_ids = fields.Many2many(IR_ATTACHMENT,'road_tax_doc_ids_m2m', string="Road Tax Certificate", ondelete='restrict', check_company=True)
    rt_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'road_tax_doc_ids_m2m', string="Others", ondelete='restrict', check_company=True)
    rt_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")

    #PUC Details
    puc = fields.Selection(selection=APPLICABLE_OPTION, string="PUC", copy=False)
    puc_from_date = fields.Date(string="From Date")
    puc_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    puc_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    puc_to_date = fields.Date(string="To Date")
    puc_doc_ids = fields.Many2many(IR_ATTACHMENT,'puc_doc_m2m', string="PUC Certificate", ondelete='restrict', check_company=True)
    puc_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'puc_others_m2m', string="Others", ondelete='restrict', check_company=True)
    puc_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")
    
    #Green Tax Details
    green_tax = fields.Selection(selection=APPLICABLE_OPTION, string="Green Tax", copy=False)
    green_tax_from_date = fields.Date(string="From Date")
    green_tax_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    green_tax_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    green_tax_to_date = fields.Date(string="To Date")
    gre_tax_doc_ids = fields.Many2many(IR_ATTACHMENT,'green_tax_doc_m2m', string="Green Tax Certificate", ondelete='restrict', check_company=True)
    gre_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'green_tax_others_m2m', string="Others", ondelete='restrict', check_company=True)
    green_tax_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")    
    
    #Speed Govener Details
    speed_govener = fields.Selection(selection=APPLICABLE_OPTION, string="Speed Govener", copy=False)
    speed_limit_per = fields.Integer(string="Speed Limit Per Hr.", copy=False)
    spd_gov_from_date = fields.Date(string="From Date")
    speed_govener_validity_months = fields.Integer(string="Validity (Months)", copy=False)
    speed_govener_validity_days = fields.Integer(string="Validity (Days)", copy=False)
    spd_gov_to_date = fields.Date(string="To Date")
    spd_gov_doc_ids = fields.Many2many(IR_ATTACHMENT,'speed_govener_doc_m2m', string="Speed Governor Certificate", ondelete='restrict', check_company=True)
    spd_gov_oth_doc_ids = fields.Many2many(IR_ATTACHMENT,'speed_govener_others_m2m', string="Others", ondelete='restrict', check_company=True)
    speed_govener_escalation_mail_days = fields.Integer(string="Escalation Mail Days", copy=False, default="15")    
    
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    

    contact_person = fields.Char(string="Contact Person", size=50)

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


    line_ids = fields.One2many('cm.vehicle.master.line', 'header_id', string="Additional Contact Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.vehicle.master.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_vehicle_master where upper(REPLACE(name, ' ', ''))  = '%s' 
            and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Vehicle Master name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_vehicle_master where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Vehicle Master short name must be unique"))

    @api.onchange('same_as_bill_address')
    def onchange_same_as_bill_address(self):
        if self.same_as_bill_address:
            billing_lines = []
            bill_values = {
                'name': self.name,
                'short_name': self.short_name,
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
        return super(CmVehicleMaster, self).write(vals)
     
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
        
        
        cm_vehicle_master = self.env[CM_VEHICLE_MASTER]
        result['all_draft'] = cm_vehicle_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_vehicle_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_vehicle_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_vehicle_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_vehicle_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_vehicle_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_vehicle_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_vehicle_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_vehicle_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_vehicle_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_vehicle_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_vehicle_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
