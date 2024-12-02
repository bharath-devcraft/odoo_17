# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_RAIL_TARIFF = 'cm.rail.tariff'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
CM_PORT = 'cm.port'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

CARGO_CATEGORY =  [('dg','DG'), ('non_dg', 'Non DG'), ('both', 'Both')]

CONTAINER_SIZE = [('20_feet_tk','20 Feet TK')]

class CmRailTariff(models.Model):
    _name = 'cm.rail.tariff'
    _description = 'Rail Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    def _get_dynamic_domain(self):
        cur_rec = self.env['res.currency'].search([('short_name', '=', 'INR'),('status', '=', 'active'),('active_trans', '=', True)], limit=1)
        return cur_rec.id if cur_rec else None

    name = fields.Char(string="Name", index=True, copy=False)
    eff_from_date = fields.Date(string="Effective From Date", copy=False)
    pol_port_id = fields.Many2one(CM_PORT, string="POL", copy=False, ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True)]")
    pod_port_id = fields.Many2one(CM_PORT, string="POD", copy=False, ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_category', '=', 'dry_port')]")
    fpod_port_id = fields.Many2one(CM_PORT, string="FPOD", copy=False, ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True)]")
    distance = fields.Integer(string="Distance(KM)", copy=False)
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Container Category", copy=False)
    cargo_category = fields.Selection(selection=CARGO_CATEGORY, string="Cargo Category", copy=False) 
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", copy=False, default='20_feet_tk', c_rule=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True, default=_get_dynamic_domain, required=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    actual_cost = fields.Float(string="Actual Cost", copy=False)
    busy_season_cost = fields.Float(string="Busy Season Cost", copy=False)
    gr_cost = fields.Float(string="GR Cost", copy=False)
    laden_dg_extra = fields.Float(string="Laden DG Extra(%)", copy=False)
    over_wt_limit = fields.Float(string="Over Wt Limit(MT)", copy=False)
    surcharge_per = fields.Float(string="Over Wt Surcharge MT(%)", copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])



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

    line_ids_a = fields.One2many('cm.rail.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.rail.tariff.laden.charges.line', 'header_id', string="Laden Charges", copy=True, c_rule=True)

    @api.onchange('container_category')
    def onchange_container_category(self):
        if self.container_category:
            if self.container_category == 'empty':
                self.cargo_category = 'both'
                self.laden_dg_extra = False
                self.over_wt_limit = False
                self.surcharge_per = False
                self.line_ids_b = [(5, 0, 0)]
            elif self.container_category == 'laden':
                self.cargo_category = 'non_dg'
                self.actual_cost = False
                self.busy_season_cost = False
                self.gr_cost = False
        else:
            self.cargo_category = False
            self.actual_cost = False
            self.busy_season_cost = False
            self.gr_cost = False
            self.laden_dg_extra = False
            self.over_wt_limit = False
            self.surcharge_per = False
            self.line_ids_b = [(5, 0, 0)]
    
    @api.onchange('pol_port_id', 'pod_port_id')
    def onchange_pol_pod(self):
        if self.pol_port_id and self.pod_port_id:
            self.name = f"{self.pol_port_id.name} - {self.pod_port_id.name}"
        else:
            self.name = False

    def validations(self):
        warning_msg = []
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if not self.laden_dg_extra or self.laden_dg_extra <= 0:
            warning_msg.append("Laden DG Extra(%) should be greater than zero")
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
        return super(CmRailTariff, self).write(vals)
     
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
        
        rail_tariff = self.env[CM_RAIL_TARIFF]
        result['all_draft'] = rail_tariff.search_count([('status', '=', 'draft')])
        result['all_active'] = rail_tariff.search_count([('status', '=', 'active')])
        result['all_inactive'] = rail_tariff.search_count([('status', '=', 'inactive')])
        result['all_editable'] = rail_tariff.search_count([('status', '=', 'editable')])
        result['my_draft'] = rail_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = rail_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = rail_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = rail_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = rail_tariff.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = rail_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = rail_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = rail_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
