# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char,valid_pin_code
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_PORT = 'cm.port'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('blacklist', 'Blacklist'),
        ('suspension', 'Suspension'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

PORT_TYPE = [('seaport', 'Seaport'), ('airport', 'Airport'), ('dry_port', 'Dry port'), ('idc', 'ICD')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

AGENT_AVAILABILITY = [('internal', 'Internal'), ('external', 'External')]

class CmPort(models.Model):
    _name = 'cm.port'
    _description = 'Port'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 5 char is allowed and will accept upper case only", size=5, c_rule=True)
    edi_code = fields.Char(string="EDI Code", index=True, copy=False)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    pin_code = fields.Char(string="Pin Code", copy=False, size=10)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    port_type = fields.Selection(selection=PORT_TYPE, string="Port Type", copy=False)
    agent_availability = fields.Selection(selection=AGENT_AVAILABILITY, string="Agent Availability", copy=False)
    is_free_zone_port = fields.Selection(selection=YES_OR_NO, string="Is Free Zone Port", copy=False)
    document_ids = fields.Many2many('ir.attachment', string="Documents", ondelete='restrict', check_company=True)
    others_ids = fields.Many2many('ir.attachment', relation='cm_port_others_ir_attachment_rel', string="Others", ondelete='restrict', check_company=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    customs_note = fields.Html(string="Customs Notes", copy=False, sanitize=False)
    security_measure_note = fields.Html(string="Security Measure Notes", copy=False, sanitize=False)
    port_authority_regulations = fields.Html(string="Port Authority Regulations", copy=False, sanitize=False)
    note = fields.Html(string="Notes", copy=False, sanitize=False)
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

    line_ids = fields.One2many('cm.port.line', 'header_id', string="Additional Contact Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.port.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in port name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_port where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Port name must be unique"))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env, self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_port where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Port Code must be unique"))
            
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
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.country_id
        else:
            self.state_id = False
            self.country_id = False

    def validations(self):
        warning_msg = []
        if not self.line_ids:
            warning_msg.append("System not allow to approve with empty port contact info")
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
        return super(CmPort, self).write(vals)
     
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
        
        cm_port = self.env[CM_PORT]
        result['all_draft'] = cm_port.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_port.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_port.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_port.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_port.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_port.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_port.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_port.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_port.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_port.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_port.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_port.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
