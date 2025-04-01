# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_CARRIER_SEA_FREIGHT_RATE = 'cm.carrier.sea.freight.rate'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
CM_PORT = 'cm.port'
RES_CURRENCY = 'res.currency'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]


CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

CONTAINER_CATEGORY =  [('laden','Laden'),
                       ('empty', 'Empty')]

ROUTING = [('direct', 'Direct'), ('through', 'Through'), ('ts', 'T/S')]
CONTAINER_TYPE = [('tk_20', 'TK20'), ('tk_40', 'TK40'), ('gp', 'GP')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto'),('imported', 'Imported')]

class CmCarrierSeaFreightRate(models.Model):
    _name = 'cm.carrier.sea.freight.rate'
    _description = 'Carrier Sea Freight Rate'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", compute='_compute_name',index=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    note = fields.Text(string="Notes")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    carrier_id= fields.Many2one('cm.carrier', string="Carrier Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    carrier_name = fields.Char(string="New Carrier Name")
    vendor_id= fields.Many2one('cm.vendor.master', string="Vendor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    carrier_type = fields.Selection(selection=CARRIER_TYPE_OPTIONS, string="Carrier Type")
    container_type = fields.Selection(selection=CONTAINER_TYPE, string="Container Type", default='tk_20')
    currency_id = fields.Many2one(RES_CURRENCY, string="Base Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden")
    service_name = fields.Char(string="Service Name")
    routing = fields.Selection(selection=ROUTING, string="Routing")
    ts_1_port_id = fields.Many2one(CM_PORT, string="T/S Port 1", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ts_2_port_id = fields.Many2one(CM_PORT, string="T/S Port 2", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    carrier_term_id = fields.Many2one('cm.carrier.terms', string="Carrier Term", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    
    pol_country_id = fields.Many2one('res.country', string="POL Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pol_port_id = fields.Many2one(CM_PORT, string="POL", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', pol_country_id)]")
    
    pod_country_id = fields.Many2one('res.country', string="POD Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pod_port_id = fields.Many2one(CM_PORT, string="POD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', pod_country_id)]")
    
    
    transit_time = fields.Integer(string="T/T Days")
    pol_free_days = fields.Integer(string="POL Free Days")
    pod_free_days = fields.Integer(string="POD Free Days")
    sf_laden = fields.Float(string="Sea Freight(Non DG)")	
    
    dg_charge = fields.Float(string="DG Charge")	
    pack_type1 = fields.Float(string="Packing Type I")	
    pack_type2 = fields.Float(string="Packing Type II")	
    pack_type3 = fields.Float(string="Packing Type III")

    imo_class_1 = fields.Float(string="Class 1")	
    imo_class_2 = fields.Float(string="Class 2")	
    imo_class_3 = fields.Float(string="Class 3")	
    imo_class_4 = fields.Float(string="Class 4")	
    imo_class_5 = fields.Float(string="Class 5")	
    imo_class_6 = fields.Float(string="Class 6")	
    imo_class_7 = fields.Float(string="Class 7")	
    imo_class_8 = fields.Float(string="Class 8")	
    imo_class_9 = fields.Float(string="Class 9")
    imo_currency_id_1 = fields.Many2one(RES_CURRENCY, string="IMO Currency 1", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_2 = fields.Many2one(RES_CURRENCY, string="IMO Currency 2", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_3 = fields.Many2one(RES_CURRENCY, string="IMO Currency 3", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_4 = fields.Many2one(RES_CURRENCY, string="IMO Currency 4", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_5 = fields.Many2one(RES_CURRENCY, string="IMO Currency 5", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_6 = fields.Many2one(RES_CURRENCY, string="IMO Currency 6", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_7 = fields.Many2one(RES_CURRENCY, string="IMO Currency 7", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_8 = fields.Many2one(RES_CURRENCY, string="IMO Currency 8", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    imo_currency_id_9 = fields.Many2one(RES_CURRENCY, string="IMO Currency 9", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    baf = fields.Float(string="BAF")	
    lss = fields.Float(string="LSS")	
    efs = fields.Float(string="EFS")	
    ecrs = fields.Float(string="ECRS")	
    pcs = fields.Float(string="PCS")	
    ewrs = fields.Float(string="EWRS")	
    ens = fields.Float(string="ENS ")	
    ips = fields.Float(string="IPS ")	
    smd = fields.Float(string="SMD")	
    ows = fields.Float(string="OWS")	
    tank_surcharge = fields.Float(string="Tank Surcharge")	
    others = fields.Float(string="Others")

    baf_currency_id = fields.Many2one(RES_CURRENCY, string="BAF Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    lss_currency_id = fields.Many2one(RES_CURRENCY, string="LSS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    efs_currency_id = fields.Many2one(RES_CURRENCY, string="EFS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ecrs_currency_id = fields.Many2one(RES_CURRENCY, string="ECRS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    pcs_currency_id = fields.Many2one(RES_CURRENCY, string="PCS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ewrs_currency_id = fields.Many2one(RES_CURRENCY, string="EWRS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ens_currency_id = fields.Many2one(RES_CURRENCY, string="ENS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ips_currency_id = fields.Many2one(RES_CURRENCY, string="IPS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    smd_currency_id = fields.Many2one(RES_CURRENCY, string="SMD Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ows_currency_id = fields.Many2one(RES_CURRENCY, string="OWS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    t_s_currency_id = fields.Many2one(RES_CURRENCY, string="Tank Surcharge Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ot_currency_id = fields.Many2one(RES_CURRENCY, string="Others Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    

    afr = fields.Float(string="AFR")
    ets = fields.Float(string="ETS")
    acd = fields.Float(string="ACD")
    ems = fields.Float(string="EMS")
    bl_others = fields.Float(string="Others")
    afr_currency_id = fields.Many2one(RES_CURRENCY, string=" AFR Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ets_currency_id = fields.Many2one(RES_CURRENCY, string=" ETS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    acd_currency_id = fields.Many2one(RES_CURRENCY, string=" ACD Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    ems_currency_id = fields.Many2one(RES_CURRENCY, string=" EMS Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	
    bl_ot_currency_id = fields.Many2one(RES_CURRENCY, string=" BL Others Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])	

    tot_laden = fields.Float(string="Non DG Total", compute='_compute_tot_laden', store=True)	
    tot_laden_dg = fields.Float(string="DG Total", compute='_compute_tot_laden_dg', store=True)	

    valid_from_date = fields.Date(string="Validity From Date")
    valid_to_date = fields.Date(string="Validity To Date")
    contract_no = fields.Char(string="Contract No", index=True)
    received_from = fields.Char(string="Received From", index=True)


    
    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    

    @api.constrains('valid_from_date','valid_to_date')
    def validity_validations(self):
        if self.valid_from_date and self.valid_to_date:
            if self.valid_from_date > self.valid_to_date:
                raise UserError(_("Validity from date should be less than validity to date"))
            
    @api.depends('baf', 'lss', 'efs', 'ecrs', 'pcs', 'ewrs', 'ets', 'ips', 'smd', 'ows', 'tank_surcharge', 'others', 'sf_laden', 'currency_id', 'baf_currency_id', 'lss_currency_id', 'efs_currency_id', 'ecrs_currency_id', 'pcs_currency_id', 'ewrs_currency_id', 'ets_currency_id', 'ips_currency_id', 'smd_currency_id', 'ows_currency_id', 't_s_currency_id', 'ot_currency_id')
    def _compute_tot_laden(self):
        exchange_rate = self.env['cm.exchange.rate']
        for record in self:
            tot_laden=record.sf_laden
            
            def convert_if_needed(amount, amount_currency, base_currency):
                if amount and amount_currency and base_currency:
                    if amount_currency.name == base_currency.name:
                        return amount
                    return exchange_rate.convert_to_base_currency(base_currency.name, amount_currency.name, amount)['converted_value']
                return 0 
        
            fields_with_currency = [
                ('baf', 'baf_currency_id'),
                ('lss', 'lss_currency_id'),
                ('efs', 'efs_currency_id'),
                ('ecrs', 'ecrs_currency_id'),
                ('pcs', 'pcs_currency_id'),
                ('ewrs', 'ewrs_currency_id'),
                ('ets', 'ets_currency_id'),
                ('ips', 'ips_currency_id'),
                ('smd', 'smd_currency_id'),
                ('ows', 'ows_currency_id'),
                ('tank_surcharge', 't_s_currency_id'),
                ('others', 'ot_currency_id'),
            ]
            
            for field, currency_field in fields_with_currency:
                tot_laden += convert_if_needed(getattr(record, field), getattr(record, currency_field), record.currency_id)
            
            record.tot_laden = tot_laden 
             

    @api.depends('tot_laden','dg_charge','pack_type1', 'pack_type2','pack_type3','imo_class_1','imo_class_2','imo_class_3','imo_class_4','imo_class_5','imo_class_6','imo_class_7','imo_class_8','imo_class_9')
    def _compute_tot_laden_dg(self):
        for record in self:
            dg_surcharge= record.dg_charge or record.pack_type1 or record.pack_type2 or record.pack_type3 or 0
            imo_charge = record.imo_class_1 or record.imo_class_2 or record.imo_class_3 or record.imo_class_4 or record.imo_class_5 or record.imo_class_6 or record.imo_class_7 or record.imo_class_8 or record.imo_class_9 or 0 
            record.tot_laden_dg = record.tot_laden + dg_surcharge or imo_charge
    
    @api.constrains('dg_charge','pack_type1', 'pack_type2','pack_type3','imo_class_1','imo_class_2','imo_class_3','imo_class_4','imo_class_5','imo_class_6','imo_class_7','imo_class_8','imo_class_9')
    def dg_charge_validation(self):
        for record in self:
            fields = [record.dg_charge,record.pack_type1, record.pack_type2, 
                record.pack_type3, record.imo_class_1, record.imo_class_2, record.imo_class_3, 
                record.imo_class_4, record.imo_class_5, record.imo_class_6, record.imo_class_7, 
                record.imo_class_8, record.imo_class_9] 
            filtered_fields = list(filter(lambda x:x not in (None,0),fields))
            
            if len(filtered_fields)==0:
                raise UserError(_("DG Charge, Packing Types, or IMO Classes either one is must"))
            
            if len(filtered_fields)>1:
                raise UserError(_("Please ensure that only one field is filled. You cannot have values in more than one of the following fields: DG Charge, Packing Types, or IMO Classes"))

    def validate_negative_value(self, field_name, field_value):
        if field_value and field_value < 0:
            raise UserError(_(f"Negative value should not allow in {field_name}, Ref: {field_value}"))
        
    # @api.constrains('sf_laden', 'baf_laden', 'ecrs_laden','ewrs_laden','ens_laden','ips_laden','oth_laden')
    # def per_tank_validation(self):
    #     self.validate_negative_value('laden', self.sf_laden)
    #     self.validate_negative_value('laden', self.baf_laden)
    #     self.validate_negative_value('laden', self.ecrs_laden)
    #     self.validate_negative_value('laden', self.ewrs_laden)
    #     self.validate_negative_value('laden', self.ens_laden)
    #     self.validate_negative_value('laden', self.ips_laden)
    #     self.validate_negative_value('laden', self.oth_laden)

        
    @api.constrains('afr', 'ets', 'acd')
    def per_bl_validation(self):
        self.validate_negative_value('AFR', self.afr)
        self.validate_negative_value('ETS', self.ets)
        self.validate_negative_value('ACD', self.acd)
        
    @api.constrains('carrier_id','carrier_name')
    def carrier_validation(self):
        if self.entry_mode != 'imported':
            if not (self.carrier_id or self.carrier_name):
                raise UserError(_("Carrier Name or New Carrier Name is mandatory"))
            if self.carrier_id and self.carrier_name:
                raise UserError(_("Please enter either Carrier Name or New Carrier Name, but not both"))

    @api.depends('carrier_id','carrier_name')
    def _compute_name(self):
        if self.carrier_id:
            self.name = self.carrier_id.name
        elif self.carrier_name:
            self.name = self.carrier_name
            if self.entry_mode == 'imported':
                carrier_id = self.env['cm.carrier'].search([('name','=',self.carrier_name.strip()),('status','=','active')],limit=1)
                self.ap_rej_date = time.strftime(TIME_FORMAT)
                self.ap_rej_user_id = self.env.user.id
                if carrier_id:
                    self.carrier_name=False
                    self.carrier_id=carrier_id.id
                
        else:
            self.name = False

    def validations(self):
        warning_msg = []
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        
        if not self.transit_time:
            warning_msg.append("T/T days value should be greater than zero.")
            
        if not self.sf_laden:
            warning_msg.append("Sea Freight(Non DG) value should be greater than zero.")

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
        return super(CmCarrierSeaFreightRate, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_carrier_sea_freight_rate = self.env[CM_CARRIER_SEA_FREIGHT_RATE]
        result['all_draft'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_carrier_sea_freight_rate.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_carrier_sea_freight_rate.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_carrier_sea_freight_rate.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_carrier_sea_freight_rate.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_carrier_sea_freight_rate.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
