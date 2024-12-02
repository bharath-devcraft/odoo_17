# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_EMPLOYEE = 'cm.employee'
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

class CmEmployee(models.Model):
	_name = 'cm.employee'
	_description = 'Employee'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_order = 'name asc'


	name = fields.Char(string="Employee Name", index=True, copy=False, c_rule=True)
	short_name = fields.Char(string="Employee Code", copy=False, help="Maximum 15 char is allowed and will accept upper case only", size=15, c_rule=True)
	status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
	inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
	remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
	company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	sub_department_id = fields.Many2one('cm.department', string="Sub Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
	whatsapp_no = fields.Char(string="WhatsApp No", size=15, copy=False)
	mb_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	wh_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	sc_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	email = fields.Char(string="Email", copy=False, size=252)
	secondary_mobile_no = fields.Char(string="Secondary Contact No", size=15, copy=False)
	reporting_id = fields.Many2one(CM_EMPLOYEE, string="Reporting To", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	designation_id = fields.Many2one('cm.designation', string="Designation", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)

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

	line_ids = fields.One2many('cm.employee.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	
	@api.constrains('name')
	def name_validation(self):
		if self.name:
			if is_special_char(self.env, self.name):
				raise UserError(_("Special character is not allowed in name field"))

			name = self.name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(name)
			from cm_employee where upper(REPLACE(name, ' ', ''))  = '%s'
			and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Employee name must be unique"))

	@api.constrains('short_name')
	def short_name_validation(self):
		if self.short_name:
			if is_special_char(self.env, self.short_name):
				raise UserError(_("Special character is not allowed in short name field"))

			short_name = self.short_name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(short_name)
			from cm_employee where upper(REPLACE(short_name, ' ', ''))  = '%s'
			and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Employee short name must be unique"))

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
		return super(CmEmployee, self).write(vals)
	 
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
		
		cm_employee = self.env[CM_EMPLOYEE]
		result['all_draft'] = cm_employee.search_count([('status', '=', 'draft')])
		result['all_active'] = cm_employee.search_count([('status', '=', 'active')])
		result['all_inactive'] = cm_employee.search_count([('status', '=', 'inactive')])
		result['all_editable'] = cm_employee.search_count([('status', '=', 'editable')])
		result['my_draft'] = cm_employee.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
		result['my_active'] = cm_employee.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
		result['my_inactive'] = cm_employee.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
		result['my_editable'] = cm_employee.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
			  
		result['all_today_count'] = cm_employee.search_count([('crt_date', '>=', fields.Date.today())])
		result['all_month_count'] = cm_employee.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
		result['my_today_count'] = cm_employee.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
		result['my_month_count'] = cm_employee.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

		return result
