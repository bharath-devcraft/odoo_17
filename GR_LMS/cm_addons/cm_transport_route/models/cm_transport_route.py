# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_TRANSPORT_ROUTE = 'cm.transport.route'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('temporarily_stopped', 'Temporarily Stopped'),
        ('restricted', 'Restricted'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual', 'Manual'),
               ('auto', 'Auto')]

TOLL_PLAZA_OPTIONS = [('available', 'Available'),
                   ('not_available', 'Not Available')]

BORDER_ENTRY_FEE = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

class CmTransportRoute(models.Model):
    _name = 'cm.transport.route'
    _description = 'Transport Route'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Route Name", index=True, copy=False)
    from_location_id = fields.Many2one('cm.transport.location', string="From Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_location_id = fields.Many2one('cm.transport.location', string="To Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)]) 
    trip_days = fields.Integer(string="Total Trip Days", copy=False, compute='_compute_line_total_trip_days')
    toll_plaza = fields.Selection(selection=TOLL_PLAZA_OPTIONS, string="Toll Plaza", copy=False)
    border_entry_fee = fields.Selection(selection=BORDER_ENTRY_FEE, string="Border Entry Fee", copy=False)
    total_trip = fields.Integer(string="Total Trip(Km)", copy=False,  compute='_compute_line_total_distance', store=True )
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
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

    line_ids = fields.One2many('cm.transport.route.line', 'header_id', string="Route Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.transport.route.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.transport.route.charges.line', 'header_id', string="Charges Details", copy=True, c_rule=True)
    
        
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))
            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_transport_route where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Transport Route name must be unique"))
            
    @api.depends('line_ids')
    def _compute_line_total_trip_days(self):
        for header in self:
            header.trip_days = sum(header.line_ids.mapped('transit_days'))
            
    @api.depends('line_ids')
    def _compute_line_total_distance(self):
        for header in self:
            header.total_trip = sum(header.line_ids.mapped('distance'))

    @api.constrains('short_name')
    def short_name_validation(self):
        if self.short_name:
            if is_special_char(self.env, self.short_name):
                raise UserError(_("Special character is not allowed in short name field"))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_transport_route where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Transport Route short name must be unique"))
    
    @api.onchange('from_location_id','to_location_id')
    def onchange_border_entry_fee(self):
        if self.from_location_id and self.to_location_id:
            if self.from_location_id == self.to_location_id:
                self.border_entry_fee = 'not_applicable'
            else:
                self.border_entry_fee = 'applicable'
        else:
            self.border_entry_fee = ''

	
    def validations(self):
        warning_msg = []
        if not self.line_ids:
            warning_msg.append("System not allow to confirm/approve with empty line details")        
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if (self.from_location_id.state_id.id != self.to_location_id.state_id.id) and not self.total_trip:
            warning_msg.append("Without Total Trip(Km) system not allow to approve the entry, Because from location state and to location state is deferent.")
        
        if self.toll_plaza == 'available' and self.border_entry_fee == 'applicable':
            if len(self.line_ids_b) < 2:
                raise UserError(_("Kindly add or verify toll charge and border entry fee. Its required as per route configuration."))
        if self.toll_plaza == 'available':
            if len(self.line_ids_b) < 1:
                raise UserError(_("Kindly add or verify toll charge. Its required as per route configuration."))
        if self.border_entry_fee == 'applicable':
            if len(self.line_ids_b) < 1:
                raise UserError(_("Kindly add or verify border entry fee. Its required as per route configuration."))
        
        if self.from_location_id:
            self.env.cr.execute(""" select from_location_id
            from cm_transport_route where from_location_id = '%s' and to_location_id = '%s'
            and id != %s and company_id = %s""" %(self.from_location_id.id,self.to_location_id.id, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("From and To Location must be unique"))
                                
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
        return super(CmTransportRoute, self).write(vals)
     
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
        
        cm_transport_route = self.env[CM_TRANSPORT_ROUTE]
        result['all_draft'] = cm_transport_route.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_transport_route.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_transport_route.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_transport_route.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_transport_route.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_transport_route.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_transport_route.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_transport_route.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_transport_route.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_transport_route.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_transport_route.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_transport_route.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
