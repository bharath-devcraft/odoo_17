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

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]


CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

ROUTING = [('direct', 'Direct'), ('through', 'Through'), ('ts', 'T/S')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmCarrierSeaFreightRate(models.Model):
    _name = 'cm.carrier.sea.freight.rate'
    _description = 'Carrier Sea Freight Rate'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    carrier_id= fields.Many2one('cm.carrier', string="Carrier Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id= fields.Many2one('cm.vendor.master', string="Vendor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    carrier_type = fields.Selection(selection=CARRIER_TYPE_OPTIONS, string="Carrier Type", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ves_serv_route_id= fields.Many2one('cm.vessel.service.route', string="Service Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    routing = fields.Selection(selection=ROUTING, string="Routing", copy=False)
    
    pol_ship_term_id = fields.Many2one('cm.shipment.term', string="Term", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pol_country_id = fields.Many2one('res.country', string="POL Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pol_port_id = fields.Many2one('cm.port', string="POL", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', pol_country_id)]")
    
    pod_ship_term_id = fields.Many2one('cm.shipment.term', string="Term", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pod_country_id = fields.Many2one('res.country', string="POD Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    pod_port_id = fields.Many2one('cm.port', string="POD", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', pod_country_id)]")
    pod_terminal_id = fields.Many2one('cm.port.terminal', string="POD Terminal", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', pod_port_id)]")
    
    
    transit_time = fields.Integer(string="Transit Time(Days)", copy=False)
    sf_laden = fields.Float(string="Laden", copy=False)	
    sf_mty = fields.Float(string="MTY", copy=False)
    
    pack_type1 = fields.Float(string="Packing Type I", copy=False)	
    pack_type2 = fields.Float(string="Packing Type II", copy=False)	
    pack_type3 = fields.Float(string="Packing Type III", copy=False)

    baf_laden = fields.Float(string="Laden", copy=False)	
    baf_mty = fields.Float(string="MTY", copy=False)

    ecrs_laden = fields.Float(string="Laden", copy=False)	
    ecrs_mty = fields.Float(string="MTY", copy=False)
    
    ewrs_laden = fields.Float(string="Laden", copy=False)	
    ewrs_mty = fields.Float(string="MTY", copy=False) 
    
    ens_laden = fields.Float(string="Laden", copy=False)	
    ens_mty = fields.Float(string="MTY", copy=False)
    
    ips_laden = fields.Float(string="Laden", copy=False)	
    ips_mty = fields.Float(string="MTY", copy=False)
    
    oth_laden = fields.Float(string="Laden", copy=False)	
    oth_mty = fields.Float(string="MTY", copy=False)

    afr = fields.Float(string="AFR(Per BL)", copy=False)
    ets = fields.Float(string="ETS(Per BL)", copy=False)
    acd = fields.Float(string="ACD(Per BL)", copy=False)
    flexi_surcharge = fields.Float(string="Flexi Surcharge", copy=False)
    tank_surcharge = fields.Float(string="Tank Surcharge(Laden)", copy=False)
    over_wgt_surcharge = fields.Float(string="Over Weight Surcharge", copy=False)
    haz = fields.Float(string="HAZ - 5.1 / 5.2", copy=False)

    tot_laden = fields.Float(string="Laden", compute='_compute_tot_laden', store=True, copy=False)	
    tot_laden_dg = fields.Float(string="Laden(DG)", compute='_compute_tot_laden_dg', store=True, copy=False)	
    tot_mty = fields.Float(string="MTY", compute='_compute_tot_mty', store=True, copy=False)

    valid_from_date = fields.Date(string="Validity From Date", copy=False)
    valid_to_date = fields.Date(string="Validity To Date", copy=False)
    contract_no = fields.Char(string="Contract No", index=True, copy=False)
    fre_pay_center = fields.Char(string="Freight Payment Center", index=True, copy=False)
    received_from = fields.Char(string="Received From", index=True, copy=False)
    rate_received_date = fields.Date(string="Rate Received Date", copy=False)   


    
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
    
    # @api.constrains('name')
    # def name_validation(self):
    #     if self.name:
    #         if is_special_char(self.env, self.name):
    #             raise UserError(_("Special character is not allowed in name field"))

    #         name = self.name.upper().replace(" ", "")
    #         self.env.cr.execute(""" select upper(name)
    #         from cm_carrier_sea_freight_rate where upper(REPLACE(name, ' ', ''))  = '%s'
    #         and id != %s and company_id = %s and status != 'inactive' """ %(name, self.id, self.company_id.id))
    #         if self.env.cr.fetchone():
    #             raise UserError(_("Carrier Sea Freight Rate name must be unique"))

    @api.constrains('valid_from_date','valid_to_date')
    def validity_validations(self):
        if self.valid_from_date and self.valid_to_date:
            if self.valid_from_date > self.valid_to_date:
                raise UserError(_("Validity from date should be less than validity to date"))
            
    @api.depends('sf_laden', 'baf_laden', 'ecrs_laden','ewrs_laden','ens_laden','ips_laden','oth_laden')
    def _compute_tot_laden(self):
        for record in self:
            record.tot_laden = record.sf_laden + record.baf_laden + record.ecrs_laden + record.ewrs_laden + record.ens_laden + record.ips_laden + record.oth_laden
    
    @api.depends('tot_laden', 'pack_type1', 'pack_type2','pack_type3')
    def _compute_tot_laden_dg(self):
        for record in self:
            record.tot_laden_dg = record.tot_laden + record.pack_type1 + record.pack_type2 + record.pack_type3 
    
    @api.depends('sf_mty', 'baf_mty', 'ecrs_mty','ewrs_mty','ens_mty','ips_mty','oth_mty')
    def _compute_tot_mty(self):
        for record in self:
            record.tot_mty = record.sf_mty + record.baf_mty + record.ecrs_mty + record.ewrs_mty + record.ens_mty + record.ips_mty + record.oth_mty
    
    def validate_laden_mty(self, field_name, field_value):
        if field_value and field_value < 0:
            raise UserError(_(f"Negative value should not allow in {field_name}, Ref: {field_value}"))
        
    @api.constrains('sf_laden', 'baf_laden', 'ecrs_laden','ewrs_laden','ens_laden','ips_laden','oth_laden')
    def laden_validation(self):
        self.validate_laden_mty('laden', self.sf_laden)
        self.validate_laden_mty('laden', self.baf_laden)
        self.validate_laden_mty('laden', self.ecrs_laden)
        self.validate_laden_mty('laden', self.ewrs_laden)
        self.validate_laden_mty('laden', self.ens_laden)
        self.validate_laden_mty('laden', self.ips_laden)
        self.validate_laden_mty('laden', self.oth_laden)
    
    @api.constrains('sf_mty', 'sf_mty', 'ecrs_mty','ewrs_mty','ens_mty','ips_mty','oth_mty')
    def mty_validation(self):
        self.validate_laden_mty('MTY', self.sf_mty)
        self.validate_laden_mty('MTY', self.sf_mty)
        self.validate_laden_mty('MTY', self.ecrs_mty)
        self.validate_laden_mty('MTY', self.ewrs_mty)
        self.validate_laden_mty('MTY', self.ens_mty)
        self.validate_laden_mty('MTY', self.ips_mty)
        self.validate_laden_mty('MTY', self.oth_mty)
    
    @api.constrains('afr', 'ets', 'acd','flexi_surcharge','tank_surcharge','over_wgt_surcharge','haz')
    def mty_validation(self):
        self.validate_laden_mty('AFR(Per BL)', self.afr)
        self.validate_laden_mty('ETS(Per BL)', self.ets)
        self.validate_laden_mty('ACD(Per BL)', self.acd)
        self.validate_laden_mty('Flexi Surcharge', self.flexi_surcharge)
        self.validate_laden_mty('Tank Surcharge(Laden)', self.tank_surcharge)
        self.validate_laden_mty('Over Weight Surcharge', self.over_wgt_surcharge)
        self.validate_laden_mty('HAZ - 5.1 / 5.2', self.haz)
            
    @api.onchange('carrier_id')
    def onchange_carrier_id(self):
        if self.carrier_id:
            self.name = self.carrier_id.name
        else:
            self.name = False

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
        return super(CmCarrierSeaFreightRate, self).write(vals)
     
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
