# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_FLEXI_TARIFF = 'cm.flexi.tariff'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'
ACCOUNT_TAX ='account.tax'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('revised', 'Revised'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

FLEXI_TYPE = [('tltd', 'TLTD'), ('tlbd', 'TLBD'), ('blbd', 'BLBD')]
LAYER_TYPE = [('3_layer', '3+1 Layer'), ('4_layer', '4+1 Layer'), ('5_layer', '5+1 Layer')]
CAPACITY = [('16kl', '16 KL'), ('18kl', '18 KL'), ('20kl', '20 KL'), ('22kl', '22 KL'), ('24kl', '24 KL')]

class CmFlexiTariff(models.Model):
    _name = 'cm.flexi.tariff'
    _description = 'Flexi Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    markup_val = fields.Float(string="Markup(%)")
    short_name = fields.Char(string="Short Name", help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    eff_from_date = fields.Date(string="Effective From Date")
    standard_price = fields.Float(string="Cost Price")
    list_price = fields.Float(string="Sales Price", help="Sales price without tax", compute='_compute_list_price', store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type", help='TLTD (Top Loading Top Discharge),TLBD (Top Loading Bottom Discharge),BLBD (Bottom Load Bottom Discharge)')
    layer_type_id = fields.Many2one('cm.flexi.layer.type', string="Layer Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    capacity_id = fields.Many2one('cm.flexi.capacity', string="Capacity", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')

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

    line_ids = fields.One2many('cm.flexi.tariff.line', 'header_id', string="Charges Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.flexi.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.depends('line_ids')
    def _compute_all_line(self):
        for rec in self:
            rec.tot_amt =  sum(rec.line_ids.mapped('gr_cost'))

    # @api.constrains('flexi_type','city_id','layer_type_id','capacity_id','vendor_id')
    def duplicate_validation(self):
        if self.flexi_type and self.vendor_id and self.city_id and self.layer_type_id and self.capacity_id:
            self.env.cr.execute(""" select id
            from cm_flexi_tariff where flexi_type  = '%s' and city_id  = '%s'
            and layer_type_id  = '%s' and capacity_id  = %s and vendor_id  = %s
            and id != %s and company_id = %s and status != 'inactive' """ %(self.flexi_type, self.city_id.id, self.layer_type_id.id, self.capacity_id.id, self.vendor_id.id, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Flexi bag type must be unique"))
            
    @api.constrains('markup_val')
    def markup_val_validation(self):
        if self.markup_val and self.markup_val < 0:
            raise UserError(_("Markup(%) should not allow negative value"))
    
    @api.onchange('flexi_type')
    def onchange_flexi_type(self):
        if self.flexi_type:
            self.name = dict(self._fields['flexi_type'].selection).get(self.flexi_type)  
        else:
            self.name = False

    @api.depends('markup_val', 'standard_price')
    def _compute_list_price(self):
        for record in self:
            if record.standard_price:
                markup_value = (record.standard_price * record.markup_val)/100
                record.list_price = record.standard_price + markup_value 
            else:
                record.list_price = 0
    
    def validations(self):
        warning_msg = []
        self.duplicate_validation()
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
        return super(CmFlexiTariff, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_flexi_tariff = self.env[CM_FLEXI_TARIFF]
        result['all_draft'] = cm_flexi_tariff.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_flexi_tariff.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_flexi_tariff.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_flexi_tariff.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_flexi_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_flexi_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_flexi_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_flexi_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_flexi_tariff.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_flexi_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_flexi_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_flexi_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
