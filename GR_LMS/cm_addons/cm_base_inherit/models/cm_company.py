# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError


ENTRY_TYPE =  [('new','New'),
			   ('name_change', 'Name Change')]
	   
YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

class CmCompany(models.Model):
	"""User"""
	_name = "res.company"
	_inherit = ['res.company','mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_description = "Companies"

	
	code = fields.Char('Short Name', size=128)
	entry_mode = fields.Selection([('auto', 'Auto'), ('manual', 'Manual')],'Entry Mode',readonly=True,default='manual')
	status = fields.Selection([
		('draft', 'Draft'),
		('active', 'Active'),
		('inactive', 'Inactvie'),
		('editable', 'Editable'),], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
	
	inactive_remark = fields.Text('Inactive Remark')
	note = fields.Text('Notes', tracking=True)
	
	## New fields added
	entry_type = fields.Selection(selection=ENTRY_TYPE, string="Entry Type", copy=False, default="new", tracking=True)
	parent_company_id = fields.Many2one('res.company', string="Parent Company", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	is_registered_company = fields.Selection(selection=YES_OR_NO, string="Is Registered Company", default="yes", copy=False)
	cin_no = fields.Char(string="Company Reg No(CIN)", copy=False, size=21)
	tax_reg_no = fields.Char(string="Tax Reg No(TRC)", size=20)
	usci_no = fields.Char(string="USCI No", size=20)
	fmc_no = fields.Char(string="FMC No", size=20)
	vat_no = fields.Char(string="VAT No", size=20)
	gst_no = fields.Char(string="GST No", copy=False, size=15)
	iec_no = fields.Char(string="IEC No", size=20)
	dpd = fields.Char(string="DPD", size=20)
	dpd_cfs = fields.Char(string="DPD - CFS", size=20)
	pan_no = fields.Char(string="PAN No", copy=False, size=10)
	aadhaar_no = fields.Char(string="Aadhaar No", copy=False, size=12, tracking=True) 
	working_day_hrs = fields.Char(string="Working Day / Hrs", size=60)
	contact_person = fields.Char(string="Contact Person", size=50)
	designation = fields.Char(string="Designation", size=50)
	phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
	email = fields.Char(string="Email", copy=False, size=252)
	skype = fields.Char(string="Skype ID", size=50)
	whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)	
	fax = fields.Char(string="Fax", copy=False, size=12)    
	street = fields.Char(string="Address Line 1", size=252)
	street1 = fields.Char(string="Address Line 2", size=252)    
	pin_code = fields.Char(string="Zip Code", copy=False, size=10)
	city_id = fields.Many2one('cm.city', string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
	state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_code = fields.Char(string="Country Code", copy=False, size=252)
	mb_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	wh_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	ph_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	same_as_bill_address = fields.Boolean(string="Same as Billing Address", default=False)
	same_as_del_address = fields.Boolean(string="Same as Delivery Address", default=False)		
			
	
	#Entry info
	active = fields.Boolean('Visible', default=True)
	active_rpt = fields.Boolean('Visible in Report', default=True)
	active_trans = fields.Boolean('Visible in Transactions', default=True)
	entry_mode = fields.Selection(
		[('auto', 'Auto'), ('manual', 'Manual')],
		'Entry Mode',
		readonly=True,
		default='manual')
	crt_date = fields.Datetime(
		'Creation Date',
		readonly=True,
		default=lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'))
	user_id = fields.Many2one(
		'res.users',
		'Created By',
		readonly=True,
		default=lambda self: self.env.user.id)
	ap_rej_date = fields.Datetime('Approved Date', readonly=True)
	ap_rej_user_id = fields.Many2one(
		'res.users', 'Approved By', readonly=True)
	inactive_date = fields.Datetime('Inactivated Date', readonly=True)
	inactive_user_id = fields.Many2one(
		'res.users', 'Inactivated By', readonly=True)
	update_date = fields.Datetime('Last Updated Date', readonly=True)
	update_user_id = fields.Many2one(
		'res.users', 'Last Updated By', readonly=True)
		
	line_ids = fields.One2many('cm.company.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
	line_ids_a = fields.One2many('cm.company.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	line_ids_b = fields.One2many('cm.company.billing.address.line', 'header_id', string="Billing Address", copy=True, c_rule=True)
	line_ids_c = fields.One2many('cm.company.bank.details.line', 'header_id', string="Bank Details", copy=True, c_rule=True)
	line_ids_d = fields.One2many('cm.company.delivery.address.line', 'header_id', string="Delivery Address", copy=True, c_rule=True)

	
	#constrains
	@api.constrains('name')
	def name_validation(self):
		""" name_validation """

		if self.name:
			if is_special_char(self.env, self.name):
				raise UserError(_('Special character is not allowed in Name field'))            
		return True
	
	@api.onchange('same_as_bill_address')
	def onchange_same_as_bill_address(self):
		if self.same_as_bill_address:
			billing_lines = []
			bill_values = {				
				'street': self.street,
				'street1': self.street1,
				'city_id': self.city_id.id,
				'state_id': self.state_id.id,
				'country_id': self.country_id.id,
				'pin_code': self.pin_code,
				
			}
			billing_lines.append((0, 0, bill_values))
			self.line_ids_b = billing_lines
		else:
			self.line_ids_b = [(5, 0, 0)]

	@api.onchange('same_as_del_address')
	def onchange_same_as_del_address(self):
		if self.same_as_del_address:
			delivery_lines = []
			del_values = {
				'street': self.street,
				'street1': self.street1,
				'city_id': self.city_id.id,
				'state_id': self.state_id.id,
				'country_id': self.country_id.id,
				'pin_code': self.pin_code,			
			}
			delivery_lines.append((0, 0, del_values))
			self.line_ids_d = delivery_lines
		else:
			self.line_ids_d = [(5, 0, 0)]
	
	@api.onchange('country_id')
	def onchange_country_id(self):
		if self.country_id:
			self.country_code = self.country_id.code
			self.mb_cc_id = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1).id
			self.wh_cc_id = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1).id
			self.ph_cc_id = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1).id
			self.city_id = False
			self.state_id = False
		else:
			self.country_code = False
			self.city_id = False
			self.state_id = False
			self.mb_cc_id = False
			self.wh_cc_id = False
			self.ph_cc_id = False
	
	@api.onchange('city_id')
	def onchange_city_id(self):
		if self.city_id:
			self.state_id = self.city_id.state_id
		else:
			self.state_id = False
	
	@validation    
	def entry_approve(self):
		""" entry_approve """
		if self.status in ('draft','editable'):
			self.write({'status': 'active',
						'ap_rej_user_id': self.env.user.id,
						'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')
						})
		return True

	def entry_draft(self):
		""" entry_draft """
		self.write({'status': 'editable'})
		return True

	def entry_inactive(self):
		""" entry_inactive """
		if self.status == 'active':
			if self.inactive_remark:
				if self.inactive_remark.strip():
					if len(self.inactive_remark.strip())>= 10:
						self.write({'status':'inactive',
									'active':False,
									'inactive_user_id': self.env.user.id,
									'inactive_date': time.strftime('%Y-%m-%d %H:%M:%S')})
					else:
						raise UserError(
							_('Minimum 10 characters are required for Inactive Remarks.'))
			else:
				raise UserError(
					_('Inactive remark is must !!, Enter the remarks in Inactive Remark field.'))
		else:
			raise UserError(
					_('Unable to inactive other than active entry.'))

		
	def unlink(self):
		""" Unlink """
		for rec in self:
			if rec.status not in ('draft') or rec.entry_mode == 'auto':
				raise UserError("You can't delete other than manually created draft entries.")
			if rec.status in ('draft'):
				res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.del_draft_entry')
				is_mgmt = self.env['res.users'].has_group('cm_user_mgmt.group_mgmt_admin')
				if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
					raise UserError("You can't delete other users draft entries")
				models.Model.unlink(rec)
		return True
	
	def write(self, vals):
		""" write """       
		vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
					 'update_user_id': self.env.user.id})
		return super(CmCompany, self).write(vals)
		
	@api.model
	def retrieve_dashboard(self):
		""" This function returns the values to populate the custom dashboard in
			the transaction views.
		"""

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
		
		
		#counts
		cm_user = self.env['res.company']
		result['all_draft'] = cm_user.search_count([('status', '=', 'draft')])
		result['all_active'] = cm_user.search_count([('status', '=', 'active')])
		result['all_inactive'] = cm_user.search_count([('status', '=', 'inactive')])
		result['all_editable'] = cm_user.search_count([('status', '=', 'editable')])
		result['my_draft'] = cm_user.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
		result['my_active'] = cm_user.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
		result['my_inactive'] = cm_user.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
		result['my_editable'] = cm_user.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
			  
		result['all_today_count'] = cm_user.search_count([('crt_date', '>=', fields.Date.today())])
		result['all_month_count'] = cm_user.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
		result['my_today_count'] = cm_user.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
		result['my_month_count'] = cm_user.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

		return result   
		
	

