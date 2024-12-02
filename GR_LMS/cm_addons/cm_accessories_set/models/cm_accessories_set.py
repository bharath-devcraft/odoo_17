# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_ACCESSORIES_SET = 'cm.accessories.set'
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

class CmAccessoriesSet(models.Model):
	_name = 'cm.accessories.set'
	_description = 'Accessories Set'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_order = 'name asc'


	name = fields.Char(string="Flexi Bag Type", index=True, copy=False)
	flexi_bag_id = fields.Many2one('product.template', string="Flexi Bag Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_bag')])
	status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
	inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
	remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	qty = fields.Integer(string="Quantity(Set)", copy=False, default=1, readonly=True)
	line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
	tot_amt = fields.Float(string="Total Cost Price", copy=False, store=True, compute='_compute_all_line')
	markup = fields.Float(string="Markup(%)", copy=False)
	tot_sale_amt = fields.Float(string="Sales Price", copy=False, store=True, compute='_compute_all_line')

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

	line_ids = fields.One2many('cm.accessories.set.line', 'header_id', string="Details", copy=True, c_rule=True)
	line_ids_a = fields.One2many('cm.accessories.set.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	
	@api.constrains('name')
	def name_validation(self):
		if self.name:
			if is_special_char(self.env, self.name):
				raise UserError(_("Special character is not allowed in name field"))

			name = self.name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(name)
			from cm_accessories_set where upper(REPLACE(name, ' ', ''))  = '%s'
			and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Flexi Bag Type name must be unique"))

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
	
	@api.depends('line_ids')
	def _compute_all_line(self):
		for data in self:
			data.line_count = len(data.line_ids)
			data.tot_amt = sum(line.tot_amt for line in data.line_ids)
			if data.markup > 0.00:
				data.tot_sale_amt = sum(line.tot_amt for line in data.line_ids) + ((sum(line.tot_amt for line in data.line_ids) * data.markup ) / 100)
			else:
				data.tot_sale_amt = sum(line.tot_amt for line in data.line_ids)
	
	@api.onchange('markup')
	def onchange_markup(self):
		for data in self:
			if data.markup > 0.00:
				data.tot_sale_amt =  sum(line.tot_amt for line in data.line_ids) + ((sum(line.tot_amt for line in data.line_ids) * data.markup ) / 100)
			else:
				data.tot_sale_amt = sum(line.tot_amt for line in data.line_ids)
	
	@api.onchange('flexi_bag_id')
	def onchange_flexi_bag_id(self):
		if self.flexi_bag_id:
			self.name = self.flexi_bag_id.name
		else:
			self.name = False
	
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
		return super(CmAccessoriesSet, self).write(vals)
	 
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
		
		cm_accessories_set = self.env[CM_ACCESSORIES_SET]
		result['all_draft'] = cm_accessories_set.search_count([('status', '=', 'draft')])
		result['all_active'] = cm_accessories_set.search_count([('status', '=', 'active')])
		result['all_inactive'] = cm_accessories_set.search_count([('status', '=', 'inactive')])
		result['all_editable'] = cm_accessories_set.search_count([('status', '=', 'editable')])
		result['my_draft'] = cm_accessories_set.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
		result['my_active'] = cm_accessories_set.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
		result['my_inactive'] = cm_accessories_set.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
		result['my_editable'] = cm_accessories_set.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
			  
		result['all_today_count'] = cm_accessories_set.search_count([('crt_date', '>=', fields.Date.today())])
		result['all_month_count'] = cm_accessories_set.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
		result['my_today_count'] = cm_accessories_set.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
		result['my_month_count'] = cm_accessories_set.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

		return result
