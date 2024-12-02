# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_TANK_MASTER = 'cm.tank.master'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('on_hire', 'On Hire'),
        ('off_hire', 'Off Hire'),
        ('sold', 'Sold'),
        ('inactive', 'Inactive')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

RESTRICTION_FLAG = [('white', 'White'), ('grey', 'Grey')]

TANK_T_CODE = [('t1','T1'),('t2','T2'),('t3','T3'),('t4','T4'),('t5','T5'),('t6','T6'),('t7','T7'),('t8','T8'),('t9','T9'),('t10','T10'),
               ('t11', 'T11'),('t12', 'T12'),('t13', 'T13'),('t14', 'T14'),('t15', 'T16'),('t17', 'T17'),('t18', 'T18'),('t19', 'T19'),('t20', 'T20'),
               ('t21', 'T21'),('t22', 'T22'),('t23', 'T23'),('t50', 'T50'),('t75', 'T75')]

SUB_TYPE = [('liquid','Liquid'),
            ('gas', 'Gas'),
            ('cryogenic', 'Cryogenic')]

SUB_TYPE2 = [('swap_body','Swap Body'),
            ('baffle', 'Baffle'),
            ('foodgrade', 'Foodgrade'),
            ('industrial', 'Industrial')]

SRV_TYPE =  [('pressure','Pressure'),('vaccum', 'Vaccum'),('Both', 'Both')]

SRV_FIX_TYPE =  [('Threaded','Threaded'),('flange', 'Flange')]

FRAME_TYPE =  [('box','Box'),('beam', 'Beam')]

TOP_DIS_ASSEMBLY =  [('blank','Blank'),('valve', 'Valve')]

PERIODIC_INS =  [('required','Required'),('not_required', 'Not Required')]

CONTAINER_SIZE = [('20_teu', '20 TEU'), ('40_teu', '40 TEU'), ('both', 'Both')]

LOCATION = [('pan_india', 'PAN India'), ('exim', 'Exim(Global)')]

OWNERSHIP_TYPE = [('own', 'Own'), ('loan', 'Loan(HP)'), ('lease', 'Lease'), ('rent', 'Rent'), ('soc', 'SOC'), ('other', 'Other Operators')]

MFG_WARRANTY =  [('no_warranty','No Warranty'),('limited', 'Limited'),('perpetual', 'Perpetual'),('expired', 'Expired')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmTankMaster(models.Model):
    _name = 'cm.tank.master'
    _description = 'Tank Master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    tank_operator_id= fields.Many2one('cm.tank.operator', string="Tank Operator Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id= fields.Many2one('cm.vendor.master', string="Owner / Lessor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    owner_name= fields.Char(string="Original Owner Name", index=True, copy=False)
    ownership_type = fields.Selection(selection=OWNERSHIP_TYPE, string="Ownership Type")
    tank_t_code = fields.Selection(selection=TANK_T_CODE, string="Tank T Code")
    sub_type = fields.Selection(selection=SUB_TYPE, string="Sub Type") 
    sub_type2 = fields.Selection(selection=SUB_TYPE2, string="Sub Type 2") 
    bus_location = fields.Selection(selection=LOCATION, string="Business Location") 

    iso_code = fields.Char(string="ISO Code", copy=False, size=252)
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False, default='20_teu')
    size_dim = fields.Char( string="Size And Dimensions(LWH)") 
    capacity = fields.Integer( string="Capacity(KL)") 
    max_cross_wgt = fields.Integer( string="Max Cross Weight(Kgs)") 
    tare_wgt = fields.Integer( string="Tare Weight(Kgs)") 
    gross_wgt = fields.Integer( string="Gross Weight(Kgs)") 
    pay_cap = fields.Integer( string="Payload Capacity(Kgs)") 
    moc_shell = fields.Char( string="MOC Of Shell") 
    tank_mawp = fields.Integer( string="Tank Mawp(Bar)")
    test_test_pres = fields.Integer( string="Tank Test Pressure(Bar)")
    steam_mawp = fields.Integer( string="Steam Mawp(Bar)")
    steam_test_pres = fields.Integer( string="Steam Test Pressure(Bar)")
    baffle = fields.Selection(selection=YES_OR_NO, string="Baffle")
    heat_area = fields.Integer( string="Effective Heating Area(Sqm)")
    tube_assembly = fields.Char( string="Steam Tube Assembly - Inlet And Outlet")
    steam_runs = fields.Integer( string="No. Of Steam Runs")
    bot_dis_assembly = fields.Char( string="Bottom Discharge Assembly")
    top_dis_assembly = fields.Selection(selection=TOP_DIS_ASSEMBLY, string="Top Discharge Assembly")
    air_assembly = fields.Char( string="Airline Assembly - Size & Type")
    srv_type = fields.Selection(selection=SRV_TYPE, string="SRV Type")
    srv_fix_type = fields.Selection(selection=SRV_FIX_TYPE, string="SRV Fixture Type")
    srv_work_pres = fields.Float( string="SRV Working Pressure(Bar)")
    srv_work_vac = fields.Float( string="SRV Working Vacuum(Bar)")
    rup_disc = fields.Selection(selection=YES_OR_NO, string="Rupture Disc")
    bot_out_hous = fields.Selection(selection=YES_OR_NO, string="Bottom Outlet Housing")
    spill_box_cover = fields.Selection(selection=YES_OR_NO, string="Spill Box Cover")
    shyp_tube = fields.Selection(selection=YES_OR_NO, string="Shyphon Tube")
    frame_type = fields.Selection(selection=FRAME_TYPE, string="Frame Type")
    hand_rail = fields.Selection(selection=YES_OR_NO, string="Hand Rail")

    ext_clad = fields.Char( string="Exterior Cladding")
    vacuum_valve = fields.Selection(selection=YES_OR_NO, string="Vacuum Valve")
    type_walkway = fields.Char( string="Type Of Walkway")
    mfg_vendor_id= fields.Many2one('cm.vendor.master', string="Manufacturer Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mfg_date = fields.Date(string="Manufacturing Date", copy=False)
    age = fields.Integer( string="Age(Yrs.)", compute='_compute_age', store=True)
    mfg_warranty = fields.Selection(selection=MFG_WARRANTY, string="Manufacturer Warranty")
    valid_from_date = fields.Date(string="Validity From Date", copy=False)
    valid_to_date = fields.Date(string="Validity To Date", copy=False)
    port_id = fields.Many2one('cm.port', string="On Hire Location", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    on_hire_date = fields.Date(string="On Hire Date", copy=False)
    off_hire_date = fields.Date(string="Off Hire Date", copy=False)
    off_location = fields.Char(string="Off Hire Location", copy=False)
    reason = fields.Char(string="Off Hire Reason", copy=False)
    periodic_ins = fields.Selection(selection=PERIODIC_INS, string="Periodic Inspection")
    interval = fields.Integer( string="Interval(Months)")
    last_inspection_date = fields.Date(string="Last Inspection Date", copy=False)
    next_inspection_date = fields.Date(string="Next Inspection Date", copy=False)
    hyd_test_date = fields.Date(string="Hydraulic Test Date", copy=False)
    pneu_test = fields.Selection(selection=YES_OR_NO, string="Pneumatic Test")

    
    restriction_flag = fields.Selection(selection=RESTRICTION_FLAG, string="Restriction Flag", default='white')
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

    line_ids = fields.One2many('cm.tank.master.line', 'header_id', string="Surveyor Inspection Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.tank.master.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.tank.master.insurance.details.line', 'header_id', string="Insurance Details", copy=True, c_rule=True)
    line_ids_c = fields.One2many('cm.tank.master.recently.used.product.line', 'header_id', string="Recently used Product", copy=True, c_rule=True)

    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_tank_master where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Tank Master number must be unique"))

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
    
    @api.depends('mfg_date')
    def _compute_age(self):
        for record in self:
            if record.mfg_date:
                today = fields.Date.today()
                mfg_date = record.mfg_date
                record.age = today.year - mfg_date.year - ((today.month, today.day) < (mfg_date.month, mfg_date.day))
            else:
                record.age = 0

    @api.onchange('tank_operator_id')
    def onchange_tank_operator_id(self):
        if self.tank_operator_id:
            self.short_name = self.tank_operator_id.short_name
        else:
            self.short_name = False
    
    @api.onchange('periodic_ins')
    def onchange_periodic_ins(self):
        if self.periodic_ins != "required":
            self.interval = False
            self.next_inspection_date = False
            self.last_inspection_date = False

    @api.onchange('mfg_warranty')
    def onchange_mfg_warranty(self):
        if self.mfg_warranty != "limited":
            self.valid_from_date = False
            self.valid_to_date = False
    
    @api.onchange('ownership_type')
    def onchange_ownership_type(self):
        if self.ownership_type not in ("soc","other"):
            self.on_hire_date = False
            self.port_id = False
            

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
        return super(CmTankMaster, self).write(vals)
     
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
        
        cm_tank_master = self.env[CM_TANK_MASTER]
        result['all_draft'] = cm_tank_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_tank_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_tank_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_tank_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_tank_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_tank_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_tank_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_tank_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
