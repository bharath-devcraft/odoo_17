# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_EXCHANGE_RATE = 'cm.exchange.rate'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
		('draft', 'Draft'),
		('editable', 'Editable'),
		('active', 'Active'),
		('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
			   ('auto', 'Auto')]

class CmExchangeRate(models.Model):
	_name = 'cm.exchange.rate'
	_description = 'Exchange Rate'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_order = 'name asc'


	name = fields.Char(string="Source", index=True, copy=False, c_rule=True)
	status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
	inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
	remarks = fields.Text(string="Remarks", copy=False)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	entry_date = fields.Date(string="Date", copy=False)
	country_id = fields.Many2one('res.country', string="Country", ondelete='restrict',default=lambda self: self.env.ref('base.in', raise_if_not_found=False).id if self.env.ref('base.in', raise_if_not_found=False) else False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
	currency_id = fields.Many2one('res.currency', string="Base Currency", copy=False, ondelete='restrict', readonly=True, tracking=True)

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

	line_ids = fields.One2many('cm.exchange.rate.line', 'header_id', string="Details", copy=True, c_rule=True)
	line_ids_a = fields.One2many('cm.exchange.rate.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	
	@api.constrains('name')
	def name_validation(self):
		if self.name:
			if is_special_char(self.env, self.name):
				raise UserError(_("Special character is not allowed in Source field"))

			name = self.name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(name)
			from cm_exchange_rate where upper(REPLACE(name, ' ', ''))  = '%s'
			and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Exchange Rate Source must be unique"))

	def validations(self):
		warning_msg = []
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

	@api.onchange('country_id')
	def onchange_country_id(self):
		if self.country_id:
			self.currency_id = self.country_id.currency_id.id
		else:
			self.currency_id = False

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
		return super(CmExchangeRate, self).write(vals)

	def convert_to_base_currency(self, base_currency_code, convert_currency_code, convert_value):
		base_currency = self.env['res.currency'].search([
			('name', '=', base_currency_code),
			('status', '=', 'active'),
			('active_trans', '=', True)
		], limit=1)
		
		if not base_currency:
			raise UserError(_(f"Base currency({base_currency_code}) not found in the system."))

		convert_currency = self.env['res.currency'].search([
			('name', '=', convert_currency_code),
			('status', '=', 'active'),
			('active_trans', '=', True)
		], limit=1)
		
		if not convert_currency:
			raise UserError(_(f"Convert currency({convert_currency_code}) not found in the system."))

		convert_currency_rec = self.env['cm.exchange.rate'].search([
			('status', '=', 'active'),
			('active_trans', '=', True),
			('currency_id', '=', base_currency.id)
		], order='entry_date desc', limit=1)

		if not convert_currency_rec:
			raise UserError(_(f"No entry found for the base currency({base_currency_code}) in the exchange rate master."))

		convert_exchange_line = convert_currency_rec.line_ids.filtered_domain([('currency_id', '=', convert_currency.id)])
		convert_exchange_rate = convert_exchange_line.exchange_rate if convert_exchange_line else None

		if convert_exchange_rate is None:
			raise UserError(_(f"Exchange rate value not found for convert currency({convert_currency_code})."))

		converted_value = convert_value * convert_exchange_rate

		return {'exchange_rate':convert_exchange_rate, 'converted_value': round(converted_value, 2)}

	@api.model
	def retrieve_dashboard(self):
		result = {}
		
		cm_exchange_rate = self.env[CM_EXCHANGE_RATE]
		result['all_draft'] = cm_exchange_rate.search_count([('status', '=', 'draft')])
		result['all_active'] = cm_exchange_rate.search_count([('status', '=', 'active')])
		result['all_inactive'] = cm_exchange_rate.search_count([('status', '=', 'inactive')])
		result['all_editable'] = cm_exchange_rate.search_count([('status', '=', 'editable')])
		result['my_draft'] = cm_exchange_rate.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
		result['my_active'] = cm_exchange_rate.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
		result['my_inactive'] = cm_exchange_rate.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
		result['my_editable'] = cm_exchange_rate.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
			  
		result['all_today_count'] = cm_exchange_rate.search_count([('crt_date', '>=', fields.Date.today())])
		result['all_month_count'] = cm_exchange_rate.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
		result['my_today_count'] = cm_exchange_rate.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
		result['my_month_count'] = cm_exchange_rate.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

		return result
