# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_SURVEYOR_TARIFF = 'cm.surveyor.tariff'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
RES_COUNTRY = 'res.country'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('revised', 'Revised'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

LOCATION = [('pan_india', 'PAN India'), ('exim', 'Exim(Global)')]

CHARGES_CATEGORY = [('container_basis', 'Container Basis')]

PRICE_OWNER = [('agent', 'Agent'),('operator', 'Operator')]

class CmSurveyorTariff(models.Model):
    _name = 'cm.surveyor.tariff'
    _description = 'Surveyor Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    surveyor_id = fields.Many2one('cm.surveyor.master', string="Surveyor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bus_location = fields.Selection(selection=LOCATION, string="Location")
    country_id = fields.Many2one(RES_COUNTRY, string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", size=252)
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    charges_category = fields.Selection(selection=CHARGES_CATEGORY, string="Charges Category", default='container_basis')
    eff_from_date = fields.Date(string="Effective From Date")
    price_owner = fields.Selection(selection=PRICE_OWNER, string="Price Owner")
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

    line_ids = fields.One2many('cm.surveyor.tariff.line', 'header_id', string="Charges Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.surveyor.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.depends('line_ids')
    def _compute_all_line(self):
        for rec in self:
            rec.tot_amt =  sum(rec.line_ids.mapped('gr_cost'))

    def duplicate_validation(self):
        if self.surveyor_id and self.bus_location  and self.charges_category and self.country_id and self.state_id and self.price_owner:
            self.env.cr.execute(""" select surveyor_id
            from cm_surveyor_tariff where surveyor_id  = %s
            and id != %s and company_id = %s and bus_location = '%s' and charges_category = '%s' 
            and country_id = %s and state_id =%s and status != 'inactive' and price_owner = '%s' """ %(self.surveyor_id.id, 
            self.id, self.company_id.id,self.bus_location,self.charges_category,self.country_id.id, self.state_id.id, self.price_owner))
            if self.env.cr.fetchone():
                raise UserError(_("Surveyor tariff must be unique in state wise for PAN India else country wise unique"))
        
    
    @api.onchange('surveyor_id')
    def onchange_surveyor_id(self):
        if self.surveyor_id:
            self.name = self.surveyor_id.name
            self.bus_location = self.surveyor_id.bus_location
            if self.bus_location == 'pan_india':
                self.country_id = self.env['res.country'].search([('name', '=', 'India')], limit=1)
                self.country_code = self.country_id.code
        else:
            self.name = False
            self.bus_location = False
            self.country_id = False
            self.country_code = False

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code
            self.state_id = False
        else:
            self.country_code = False
            self.state_id = False

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
        return super(CmSurveyorTariff, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_surveyor_tariff = self.env[CM_SURVEYOR_TARIFF]
        result['all_draft'] = cm_surveyor_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'agent')])
        result['all_active'] = cm_surveyor_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'agent')])
        result['all_inactive'] = cm_surveyor_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'agent')])
        result['all_editable'] = cm_surveyor_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'agent')])
        result['my_draft'] = cm_surveyor_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_active'] = cm_surveyor_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_inactive'] = cm_surveyor_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_editable'] = cm_surveyor_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
              
        result['all_today_count'] = cm_surveyor_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
        result['all_month_count'] = cm_surveyor_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])
        result['my_today_count'] = cm_surveyor_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
        result['my_month_count'] = cm_surveyor_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])

        return result
    
    @api.model
    def retrieve_op_dashboard(self):
        result = {}
        
        cm_surveyor_tariff = self.env[CM_SURVEYOR_TARIFF]
        result['all_draft'] = cm_surveyor_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'operator')])
        result['all_active'] = cm_surveyor_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'operator')])
        result['all_inactive'] = cm_surveyor_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'operator')])
        result['all_editable'] = cm_surveyor_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'operator')])
        result['my_draft'] = cm_surveyor_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_active'] = cm_surveyor_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_inactive'] = cm_surveyor_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_editable'] = cm_surveyor_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
              
        result['all_today_count'] = cm_surveyor_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
        result['all_month_count'] = cm_surveyor_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])
        result['my_today_count'] = cm_surveyor_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
        result['my_month_count'] = cm_surveyor_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])

        return result
