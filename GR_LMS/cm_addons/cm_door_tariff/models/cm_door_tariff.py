# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
		('draft', 'Draft'),
		('editable', 'Editable'),
		('active', 'Active'),
		('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
			   ('auto', 'Auto')]

PRICE_OWNER = [('agent', 'Agent'),('operator', 'Operator')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

class CmDoorTariff(models.Model):
	_name = 'cm.door.tariff'
	_description = 'Door Tariff'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_order = 'name asc'


	name = fields.Char(string="Name", index=True)
	status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
	inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
	remarks = fields.Text(string="Remarks")
	company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	eff_from_date = fields.Date(string="Effective From Date")
	country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
	port_id = fields.Many2one('cm.port', string="Port Name", ondelete='restrict', domain="[('country_id', '=', country_id), ('status', '=', 'active'), ('active_trans', '=', True)]", tracking=True)
	ship_term_id = fields.Many2one('cm.shipment.term', string="Shipment Term", domain=[('status', '=', 'active'),('active_trans', '=', True)])
	terminal_id = fields.Many2one('cm.port.terminal', string="Terminal Name", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', port_id)]")
	service_id= fields.Many2one('cm.service', string="Service Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
	price_owner = fields.Selection(selection=PRICE_OWNER, string="Price Owner")
	tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')
	container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden", default="laden")
	
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

	line_ids = fields.One2many('cm.door.tariff.line', 'header_id', string="Charges", copy=True, c_rule=True)
	line_ids_a = fields.One2many('cm.door.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	
	
	@api.depends('line_ids')
	def _compute_all_line(self):
		for rec in self:
			rec.tot_amt =  sum(rec.line_ids.mapped('gr_cost'))
	
	def duplicate_validation(self):
		if (self.port_id and self.terminal_id and self.ship_term_id 
			and self.price_owner):
			self.env.cr.execute(""" select id
			from cm_door_tariff where port_id  = %s
			and terminal_id = %s and ship_term_id = '%s'            
			and price_owner = '%s'
			and id != %s and company_id = %s""" %(self.port_id.id,self.terminal_id.id,
												self.ship_term_id.id,self.price_owner,self.id,
												self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Duplicate entry are not allowed"))
	

	@api.onchange('port_id')
	def onchange_port(self):
		if self.port_id:
			self.name = self.port_id.name
			terminal_recs = self.env['cm.port.terminal'].search([
				('port_id', '=', self.port_id.id),
				('company_id', '=', self.company_id.id)
			])
			if len(terminal_recs) == 1:  
				self.terminal_id = terminal_recs.id
			else:
				self.terminal_id = False
		else:
			self.terminal_id = False
			self.name = ""
				
	def validations(self):
		warning_msg = []
		self.duplicate_validation()
		if not self.line_ids:
			warning_msg.append("System not allow to approve with empty line details")
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
		return super(CmDoorTariff, self).write(vals)
	 
	@api.model
	def retrieve_dashboard(self):
		result = {}
		
		cm_door_tariff = self.env['cm.door.tariff']
		result['all_draft'] = cm_door_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'agent')])
		result['all_active'] = cm_door_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'agent')])
		result['all_inactive'] = cm_door_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'agent')])
		result['all_editable'] = cm_door_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'agent')])
		result['my_draft'] = cm_door_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
		result['my_active'] = cm_door_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
		result['my_inactive'] = cm_door_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
		result['my_editable'] = cm_door_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
			  
		result['all_today_count'] = cm_door_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
		result['all_month_count'] = cm_door_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])
		result['my_today_count'] = cm_door_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
		result['my_month_count'] = cm_door_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])

		return result

	@api.model
	def retrieve_op_dashboard(self):
		result = {}
		
		cm_door_tariff = self.env['cm.door.tariff']
		result['all_draft'] = cm_door_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'operator')])
		result['all_active'] = cm_door_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'operator')])
		result['all_inactive'] = cm_door_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'operator')])
		result['all_editable'] = cm_door_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'operator')])
		result['my_draft'] = cm_door_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
		result['my_active'] = cm_door_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
		result['my_inactive'] = cm_door_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
		result['my_editable'] = cm_door_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
			  
		result['all_today_count'] = cm_door_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
		result['all_month_count'] = cm_door_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])
		result['my_today_count'] = cm_door_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
		result['my_month_count'] = cm_door_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])

		return result
