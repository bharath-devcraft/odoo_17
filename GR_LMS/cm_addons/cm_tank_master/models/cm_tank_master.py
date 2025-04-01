# -*- coding: utf-8 -*-
import time
import re
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
        ('on_hire', 'On Hire / Service'),
        ('off_hire', 'Off Hire / Service'),
        ('sold', 'Sold'),
        ('inactive', 'Inactive')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

RESTRICTION_FLAG = [('white', 'White'), ('grey', 'Grey')]

INVENTORY_CONTROL = [('gmpl_group', 'GMPL'), ('gscs', 'GSCS'), ('soc', 'SOC'), ('other', 'Other Operator')]

SUB_TYPE = [('liquid','Liquid'),
            ('gas', 'Gas'),
            ('cryogenic', 'Cryogenic')]

SUB_TYPE2 = [('swap_body','Swap Body'),
            ('baffle', 'Baffle'),
            ('foodgrade', 'Foodgrade'),
            ('industrial', 'Industrial')]

SRV_TYPE =  [('pressure','Pressure'),('vaccum', 'Vacuum'),('Both', 'Both')]

SRV_FIX_TYPE =  [('Threaded','Threaded'),('flange', 'Flange')]

FRAME_TYPE =  [('box','Box'),('beam', 'Beam'),('spider', 'Spider')]

QUALITY_RANK =  [('a','A'),('b', 'B'),('c', 'C'),('d', 'D')]

TOP_DIS_ASSEMBLY =  [('blank','Blank'),('valve', 'Valve')]

PITTING_TYPE =  [('type_a','Type A'),('type_b', 'Type B'),('pitting_free', 'Pitting Free'),('buffed', 'Buffed')]

PERIODIC_INS =  [('required','Required'),('not_required', 'Not Required')]

CONTAINER_SIZE = [('20_teu', '20 TEU'), ('40_teu', '40 TEU'), ('both', 'Both')]

LOCATION = [('pan_india', 'Domestic'), ('exim', 'Exim(Global)')]

TEST_CATEGORY = [('hydraulic_test', 'Hydraulic Test'), ('pneumatic_test', 'Pneumatic Test')]

OWNERSHIP_TYPE = [('own', 'Own'), ('loan', 'Loan'), ('lease', 'Lease'), ('rent', 'Hire Purchase')]

MFG_WARRANTY =  [('no_warranty','No Warranty'),('limited', 'Limited'),('perpetual', 'Perpetual/Life Time'),('expired', 'Expired')]

EXT_CLAD =  [('frp','FRP'),('grp', 'GRP'),('aluminium', 'Aluminium'),('no', 'No')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

Coated_Not_Coated =  [('coated','Coated'),
               ('non_coated', 'Non Coated')]

DG_NON_DG = [('yes', 'DG'), ('no', 'Non DG')]

class CmTankMaster(models.Model):
    _name = 'cm.tank.master'
    _description = 'Tank Master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False, size=11)
    short_name = fields.Char(string="Short Name", copy=False, size=4, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    tank_operator_id= fields.Many2one('cm.tank.operator', string="Tank Operator Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id= fields.Many2one('cm.vendor.master', string="Owner / Lessor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    owner_name= fields.Char(string="Original Owner Name", index=True, copy=False)
    ownership_type = fields.Selection(selection=OWNERSHIP_TYPE, string="Ownership Type")
    tank_tcode_id = fields.Many2one('cm.tank.tcode', string="Tank T Code", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    sub_type = fields.Selection(selection=SUB_TYPE, string="Sub Type") 
    sub_type2 = fields.Selection(selection=SUB_TYPE2, string="Sub Type 2") 
    bus_location = fields.Selection(selection=LOCATION, string="Business Location") 
    dom_applicable = fields.Selection(selection=YES_OR_NO, string="Domestication Applicable")
    dom_date = fields.Date(string="Domesticated Date", copy=False) 

    iso_code = fields.Char(string="ISO Code", copy=False, size=252)
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False, default='20_teu')
    size_dim = fields.Char( string="Size And Dimensions(LWH)") 
    capacity = fields.Integer( string="Capacity(Ltr)") 
    max_cross_wgt = fields.Integer( string="Max Gross Weight(Kgs)") 
    tare_wgt = fields.Integer( string="Tare Weight(Kgs)") 
    pay_cap = fields.Integer( string="Payload Capacity(Kgs)") 
    moc_shell = fields.Char( string="MOC Of Shell") 
    shell_thickness= fields.Float( string="Shell Thickness(mm)")
    tank_mawp = fields.Integer( string="Tank MAWP(Bar)")
    test_test_pres = fields.Integer( string="Tank Test Pressure(Bar)")
    steam_mawp = fields.Integer( string="Steam MAWP(Bar)")
    steam_test_pres = fields.Integer( string="Steam Test Pressure(Bar)")
    baffle = fields.Selection(selection=YES_OR_NO, string="Baffle")
    heat_area = fields.Integer( string="Effective Heating Area(Sqm)")
    tube_assembly_in = fields.Float( string="Steam Tube Assembly Inlet(Inch)")
    tube_assembly_out = fields.Float( string="Steam Tube Assembly Outlet(Inch)")
    steam_runs = fields.Integer( string="No. Of Steam Runs")
    no_of_closure = fields.Integer( string="No. Of Closure")
    bot_dis_assembly = fields.Selection(selection=YES_OR_NO, string="Bottom Discharge Assembly")
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
    steam_work_con = fields.Selection(selection=YES_OR_NO, string="Steam Tube Working Condition")
    hand_rail = fields.Selection(selection=YES_OR_NO, string="Hand Rail")

    ext_clad = fields.Selection(selection=EXT_CLAD, string="Exterior Cladding")
    type_walkway = fields.Char( string="Type Of Walkway")
    mfg_vendor_id= fields.Many2one('cm.vendor.master', string="Tank Manufacturer Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mfg_vendor = fields.Char(string="New Manufacturer")
    tank_mfg_serial_no = fields.Integer( string="Tank Mfg Serial No")
    mfg_date = fields.Date(string="Manufacturing Date", copy=False)
    age = fields.Integer( string="Age(Yrs.)", compute='_compute_age', store=True)
    mfg_warranty = fields.Selection(selection=MFG_WARRANTY, string="Manufacturer Warranty")
    valid_from_date = fields.Date(string="Validity From Date", copy=False)
    valid_to_date = fields.Date(string="Validity To Date", copy=False)
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    on_hire_date = fields.Date(string="On Service Date", copy=False)
    on_hire_location = fields.Char(string="On Service Location", copy=False)
    off_hire_date = fields.Date(string="Off Service Date", copy=False)
    off_location = fields.Char(string="Off Service Location", copy=False)
    reason = fields.Char(string="Off Service Reason", copy=False)
    periodic_ins = fields.Selection(selection=PERIODIC_INS, string="Periodic Inspection", default='required')
    ins_inspection_date = fields.Date(string="Initial Test Date", copy=False)
    last_inspection_date = fields.Date(string="Last Test Date", copy=False)
    next_inspection_date = fields.Date(string="Next Test Date", copy=False)
    hyd_test_date = fields.Date(string="Hydraulic Test Date", copy=False)
    test_category = fields.Selection(selection=TEST_CATEGORY, string="Test Category")
    buffing = fields.Selection(selection=YES_OR_NO, string="Buffing")
    coated_not_coated = fields.Selection(selection=Coated_Not_Coated, string="Coated / Not Coated")
    coating_type= fields.Many2one('cm.coating.type', string="Coating Type", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    percentage = fields.Integer(string="Percentage(%)",size=3)
    
    product_name = fields.Char( string="Product Name")
    dg_product = fields.Selection(selection=DG_NON_DG, string="Product Type")
    
    quality_rank = fields.Selection(selection=QUALITY_RANK, string="Quality Rank")
    depot_id = fields.Many2one('cm.depot.location', string="Current Depot Location", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    
    refu_applicable = fields.Selection(selection=YES_OR_NO, string="Refurbished Applicable")
    pitting_type = fields.Selection(selection=PITTING_TYPE, string="Pitting Type")
    refu_date = fields.Date(string="Refurbished Date", copy=False)
    non_trans = fields.Boolean(string="Non Transferable")
    Both = fields.Boolean(string="Both")
    none = fields.Boolean(string="None")

    attachment_ids = fields.Many2many('ir.attachment', string="Testing Certificate", ondelete='restrict', check_company=True)
    attachment_ids_2 = fields.Many2many('ir.attachment', 'm2m_clean_certificate_rel', 'tank_id' ,'attach_id', string="Cleaning Certificate", ondelete='restrict', check_company=True)
    attachment_ids_3 = fields.Many2many('ir.attachment', 'm2m_con_survey_rel', 'tank_id' ,'attach_id', string="Condition Survey ", ondelete='restrict', check_company=True)


    restriction_flag = fields.Selection(selection=RESTRICTION_FLAG, string="Restriction Flag", default='white')
    inven_control = fields.Selection(selection=INVENTORY_CONTROL, string="Inventory Control")
    active = fields.Boolean(string="Visible in View", default=True)
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
    line_ids_d = fields.One2many('cm.tank.master.mandatory.doc.line', 'header_id', string="Mandatory Certificates", copy=True, c_rule=True)

    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper()
            pattern = r"^[A-Za-z]{4}\d{5,7}$"
            if not re.match(pattern, name):
                raise UserError(_("Tank Master number not valid kindly enter valid number")) 
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
        
        if self.line_ids_d:
            docs=[line.doc_name for line in self.line_ids_d]
            if 'test' not in docs :
                warning_msg.append("Test Certificate is mandatory in mandatory certificates tab")

        else:
            warning_msg.append("Mandatory certificates are not attached in mandatory certificates tab")

            
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(_(formatted_messages))
        
        return True
    
    @api.constrains('last_inspection_date','next_inspection_date')
    def inspection_date_validations(self):
        if self.last_inspection_date and self.next_inspection_date and self.periodic_ins == 'required':
            if self.last_inspection_date > self.next_inspection_date:
                raise UserError(_("Last inspection date should be less than next inspection date"))
    
    @api.constrains('percentage')
    def percentage_validations(self):
        if self.percentage >100 or self.percentage < 0:
            raise UserError(_("Percentage should be in the range of 0 to 100"))
    
    @api.constrains('mfg_vendor_id','mfg_vendor')
    def mfg_vendor_validations(self):
        if self.inven_control in ('gmpl_group','gscs'):
            if (self.mfg_vendor_id and self.mfg_vendor) or not any([self.mfg_vendor_id , self.mfg_vendor]):
                raise UserError(_("Either tank manufacturer name or manufacturer vendor is must not both"))
    
    @api.depends('mfg_date')
    def _compute_age(self):
        for record in self:
            if record.mfg_date:
                today = fields.Date.today()
                mfg_date = record.mfg_date
                record.age = today.year - mfg_date.year - ((today.month, today.day) < (mfg_date.month, mfg_date.day))
            else:
                record.age = 0
                
    @api.onchange('line_ids_d')
    def onchange_line_ids_d(self):
        if self.line_ids_d:
            line_rec = self.line_ids_d.sorted(lambda line: line.create_date or fields.Datetime.now(), reverse=True)[:1]
            if line_rec:
                self.last_inspection_date = line_rec[0].test_date
                self.next_inspection_date = line_rec[0].valid_to_date

    @api.onchange('tank_operator_id')
    def onchange_tank_operator_id(self):
        if self.tank_operator_id:
            self.short_name = self.tank_operator_id.short_name
        else:
            self.short_name = False
    
    @api.onchange('periodic_ins')
    def onchange_periodic_ins(self):
        if self.periodic_ins != "required":
            self.next_inspection_date = False
            self.last_inspection_date = False
            self.ins_inspection_date = False

    @api.onchange('mfg_warranty')
    def onchange_mfg_warranty(self):
        if self.mfg_warranty != "limited":
            self.valid_from_date = False
            self.valid_to_date = False

    @api.onchange('bus_location')
    def onchange_bus_location(self):
        self.pitting_type = False
        self.non_trans = False
        self.Both = False
        self.none = False
        self.dom_applicable = False
        self.dom_date = False
    
    @api.onchange('dom_applicable')
    def onchange_dom_applicable(self):
        self.dom_date = False

    @api.onchange('bot_dis_assembly')
    def onchange_bot_dis_assembly(self):
        self.no_of_closure = False

    @api.onchange('refu_applicable')
    def onchange_refu_applicable(self):
        self.refu_date = False
    
    @api.onchange('coated_not_coated')
    def onchange_coated_not_coated(self):
        self.coating_type = False

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
        result = {}
        
        cm_tank_master = self.env[CM_TANK_MASTER]
        result['all_draft'] = cm_tank_master.search_count([('status', '=', 'draft'),('inven_control', '=', 'gmpl_group')])
        result['all_active'] = cm_tank_master.search_count([('status', '=', 'active'),('inven_control', '=', 'gmpl_group')])
        result['all_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'),('inven_control', '=', 'gmpl_group')])
        result['all_editable'] = cm_tank_master.search_count([('status', '=', 'editable'),('inven_control', '=', 'gmpl_group')])
        result['my_draft'] = cm_tank_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gmpl_group')])
        result['my_active'] = cm_tank_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gmpl_group')])
        result['my_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gmpl_group')])
        result['my_editable'] = cm_tank_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gmpl_group')])
              
        result['all_today_count'] = cm_tank_master.search_count([('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'gmpl_group')])
        result['all_month_count'] = cm_tank_master.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('inven_control', '=', 'gmpl_group')])
        result['my_today_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'gmpl_group')])
        result['my_month_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('inven_control', '=', 'gmpl_group')])

        return result
    
    @api.model
    def gscs_retrieve_dashboard(self):
        result = {}
        
        cm_tank_master = self.env[CM_TANK_MASTER]
        result['all_draft'] = cm_tank_master.search_count([('status', '=', 'draft'),('inven_control', '=', 'gscs')])
        result['all_active'] = cm_tank_master.search_count([('status', '=', 'active'),('inven_control', '=', 'gscs')])
        result['all_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'),('inven_control', '=', 'gscs')])
        result['all_editable'] = cm_tank_master.search_count([('status', '=', 'editable'),('inven_control', '=', 'gscs')])
        result['my_draft'] = cm_tank_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gscs')])
        result['my_active'] = cm_tank_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gscs')])
        result['my_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gscs')])
        result['my_editable'] = cm_tank_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('inven_control', '=', 'gscs')])
              
        result['all_today_count'] = cm_tank_master.search_count([('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'gscs')])
        result['all_month_count'] = cm_tank_master.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('inven_control', '=', 'gscs')])
        result['my_today_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'gscs')])
        result['my_month_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('inven_control', '=', 'gscs')])

        return result
    @api.model
    def soc_retrieve_dashboard(self):
        result = {}
        
        cm_tank_master = self.env[CM_TANK_MASTER]
        result['all_draft'] = cm_tank_master.search_count([('status', '=', 'draft'),('inven_control', '=', 'soc')])
        result['all_active'] = cm_tank_master.search_count([('status', '=', 'active'),('inven_control', '=', 'soc')])
        result['all_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'),('inven_control', '=', 'soc')])
        result['all_editable'] = cm_tank_master.search_count([('status', '=', 'editable'),('inven_control', '=', 'soc')])
        result['my_draft'] = cm_tank_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('inven_control', '=', 'soc')])
        result['my_active'] = cm_tank_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('inven_control', '=', 'soc')])
        result['my_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('inven_control', '=', 'soc')])
        result['my_editable'] = cm_tank_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('inven_control', '=', 'soc')])
              
        result['all_today_count'] = cm_tank_master.search_count([('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'soc')])
        result['all_month_count'] = cm_tank_master.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('inven_control', '=', 'soc')])
        result['my_today_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'soc')])
        result['my_month_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('inven_control', '=', 'soc')])

        return result
    
    @api.model
    def ot_op_retrieve_dashboard(self):
        result = {}
        
        cm_tank_master = self.env[CM_TANK_MASTER]
        result['all_draft'] = cm_tank_master.search_count([('status', '=', 'draft'),('inven_control', '=', 'other')])
        result['all_active'] = cm_tank_master.search_count([('status', '=', 'active'),('inven_control', '=', 'other')])
        result['all_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'),('inven_control', '=', 'other')])
        result['all_editable'] = cm_tank_master.search_count([('status', '=', 'editable'),('inven_control', '=', 'other')])
        result['my_draft'] = cm_tank_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('inven_control', '=', 'other')])
        result['my_active'] = cm_tank_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('inven_control', '=', 'other')])
        result['my_inactive'] = cm_tank_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('inven_control', '=', 'other')])
        result['my_editable'] = cm_tank_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('inven_control', '=', 'other')])
              
        result['all_today_count'] = cm_tank_master.search_count([('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'other')])
        result['all_month_count'] = cm_tank_master.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('inven_control', '=', 'other')])
        result['my_today_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('inven_control', '=', 'other')])
        result['my_month_count'] = cm_tank_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('inven_control', '=', 'other')])

        return result
