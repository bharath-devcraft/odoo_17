# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_AGENT_COMMISSION = 'cm.agent.commission'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

IMPORT_EXPORT =  [('import','Import'), ('export', 'Export'), ('t_s', 'T/S'), ('booking_party', 'Booking Party')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmAgentCommission(models.Model):
    _name = 'cm.agent.commission'
    _description = 'Agent Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden")
    eff_from_date = fields.Date(string="Effective From Date")
    port_id = fields.Many2one('cm.port', string="Port Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    actual_cost = fields.Float(string="Commission Value")
    charges_id = fields.Many2one('cm.charges.heads', string="Charge Head", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    import_export = fields.Selection(selection=IMPORT_EXPORT, string="Shipment Type")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])              

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

    line_ids = fields.One2many('cm.agent.commission.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    # @api.constrains('name', 'port_id', 'container_category','import_export') 
    def duplicate_validation(self):
        if self.name and self.port_id and self.container_category and self.import_export:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))
            self.env.cr.execute(""" select id
            from cm_agent_commission where port_id = %s
            and id != %s and container_category = '%s' and import_export = '%s' and company_id = %s and status != 'inactive'""" %(self.port_id.id, self.id, self.container_category, self.import_export, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Agent Commission name must be unique"))
            
    @api.onchange('port_id')
    def onchange_port_id(self):
        if self.port_id:
            self.name = self.port_id.name
        else:
            self.name = False


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
        return super(CmAgentCommission, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_agent_commission = self.env[CM_AGENT_COMMISSION]
        result['all_draft'] = cm_agent_commission.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_agent_commission.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_agent_commission.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_agent_commission.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_agent_commission.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_agent_commission.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_agent_commission.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_agent_commission.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_agent_commission.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_agent_commission.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_agent_commission.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_agent_commission.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
