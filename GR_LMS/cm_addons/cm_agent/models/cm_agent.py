# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation, is_special_char, valid_mobile_no, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_pan_no,  valid_aadhaar_no
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS='res.users'
CM_AGENT='cm.agent'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
		('draft', 'Draft'),
		('editable', 'Editable'),		
		('active', 'Active'),
		('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
			   ('auto', 'Auto')]
			   
ENTRY_TYPE =  [('new','New'),
			   ('name_change', 'Name Change')]
			   
YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]
			   
AGENT_CATEGORY = [('external', 'External'), ('internal', 'Internal')]

VALIDITY_RANGE = [('perpetual', 'Perpetual'), ('limited', 'Limited')]

PROVIDING_SERVICES =  [('transportation','Transportation'),
			   ('warehousing', 'Warehousing'),
			   ('custom_clearance', 'Customs Clearance'),
			   ('shipment', 'Shipment')]

class CmAgent(models.Model):
	_name = 'cm.agent'
	_description = 'Agent Master'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
	_order = 'name asc'

	name = fields.Char(string="Name", index=True, copy=False)
	short_name = fields.Char(string="Short Name", copy=False, help="Maximum 15 char is allowed and will accept upper case only", size=15)
	status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
	inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
	remarks = fields.Html(string="Remarks", copy=False, sanitize=False)

	contact_person = fields.Char(string="Contact Person", size=50)
	mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
	phone_no = fields.Char(string="Phone No", size=12, copy=False)
	email = fields.Char(string="Email", copy=False, size=252)
	fax = fields.Char(string="Fax", copy=False, size=12)    
	street = fields.Char(string="Street", size=252)
	street1 = fields.Char(string="Street1", size=252)    
	pin_code = fields.Char(string="Zip Code", copy=False, size=10)
	city_id = fields.Many2one('cm.city', string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
	state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	mb_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	wh_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	ph_cc_id = fields.Many2one('cm.country.code', string="Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_code = fields.Char(string="Country Code", copy=False, size=252)
	currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
	
	pan_no = fields.Char(string="PAN No", copy=False, size=10)
	aadhaar_no = fields.Char(string="Aadhaar No", copy=False, size=12, tracking=True)    
	gst_no = fields.Char(string="GST No", copy=False, size=15)
	
	### New Fields Added
	entry_type = fields.Selection(selection=ENTRY_TYPE, string="Entry Type", copy=False, default="new", tracking=True)	
	is_registered = fields.Selection(selection=YES_OR_NO, string="Is Registered Company", default="yes", copy=False)
	cin_no = fields.Char(string="Company Reg No", copy=False, size=21)
	usci_no = fields.Char(string="USCI No", size=20)
	tax_reg_no = fields.Char(string="Tax Reg No(TRC)", size=20)
	gst_category = fields.Selection(selection=YES_OR_NO, string="GST Applicable", copy=False)	
	vat_no = fields.Char(string="VAT No", size=20)
	fmc_no = fields.Char(string="FMC No", size=20)	
	designation = fields.Char(string="Designation", size=50)
	skype = fields.Char(string="Skype ID", size=50)		
	whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)	
	agent_category = fields.Selection(selection=AGENT_CATEGORY, string="Agent Category", copy=False)
	exp_years = fields.Char(string="Industry Experience(Yrs)", size=15)
	providing_services = fields.Selection(selection=PROVIDING_SERVICES, string="Providing Services", copy=False)
	port_ids = fields.Many2many('cm.port', string="Servicing Ports", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	contract_agree = fields.Selection(selection=YES_OR_NO, string="Contractual Agreements", copy=False)
	validity_range = fields.Selection(selection=VALIDITY_RANGE, string="Validity Range", copy=False)	
	from_date = fields.Date(string="From Date", copy=False)
	to_date = fields.Date(string="To Date", copy=False)	
	past_legal_action = fields.Selection(selection=YES_OR_NO, string="Past Legal Actions", copy=False)
	legal_details = fields.Text(string="Legal Details", copy=False)

	company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
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


	line_ids = fields.One2many('cm.agent.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
	line_ids_a = fields.One2many('cm.agent.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
	line_ids_b = fields.One2many('cm.agent.bank.details.line', 'header_id', string="Bank Details", copy=True, c_rule=True)
	
	@api.constrains('name')
	def name_validation(self):
		if self.name:
			if is_special_char(self.env,self.name):
				raise UserError(_("Special character is not allowed in name field"))

			name = self.name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(name)
			from cm_agent where upper(REPLACE(name, ' ', ''))  = '%s' 
			and id != %s and company_id = %s""" %(name, self.id,self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Agent name must be unique"))

	@api.constrains('short_name')
	def short_name_validation(self):
		if self.short_name:
			if is_special_char(self.env,self.short_name):
				raise UserError(_("Special character is not allowed in Agent ID field"))

			short_name = self.short_name.upper().replace(" ", "")
			self.env.cr.execute(""" select upper(short_name)
			from cm_agent where upper(REPLACE(short_name, ' ', ''))  = '%s'
			and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
			if self.env.cr.fetchone():
				raise UserError(_("Agent ID must be unique"))
		
	@api.constrains('phone_no')
	def phone_validation(self):
		if self.phone_no  and not valid_phone_no(self.phone_no):
		   raise UserError(_("Phone number is invalid. Please enter the correct phone number with SDD code"))

	@api.constrains('mobile_no')
	def mobile_no_validation(self):
		if self.mobile_no and self.country_id:
			if self.country_id.code == 'IN':
				if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
					raise UserError(_("Mobile number(IN) is invalid. Please enter correct mobile number"))
			if not valid_mobile_no(self.mobile_no):
				raise UserError(_("Mobile number is invalid. Please enter correct mobile number"))

	@api.constrains('email')
	def email_validation(self):
		if self.email  and not valid_email(self.email):
			raise UserError(_("Email is invalid. Please enter the correct email"))
	

	@api.constrains('street')
	def street_validation(self):
		if self.street and is_special_char(self.env,self.street):
			raise UserError(_("Special character is not allowed in street field"))                

	@api.constrains('street1')
	def street1_validation(self):
		if self.street1 and is_special_char(self.env,self.street1):
			raise UserError(_("Special character is not allowed in street1 field"))

	@api.constrains('pin_code')
	def pin_code_validation(self):
		if self.pin_code:
			if self.country_id.code == 'IN':
				if not(len(str(self.pin_code)) == 6 and self.pin_code.isdigit() == True):
					raise UserError(_("Invalid pin code(IN). Please enter the correct 6 digit pin code"))
			else:
				if not valid_pin_code(self.pin_code):
					raise UserError(_("Invalid pin code. Please enter the correct pin code"))
				if is_special_char(self.env,self.pin_code):
					raise UserError(_("Special character is not allowed in pin code field"))



	@api.constrains('pan_no')
	def pan_no_validation(self):
		if self.pan_no:
			if not valid_pan_no(self.pan_no):
				raise UserError(_("Invalid PAN number. Please enter the correct PAN number"))
			existing_record = self.env[CM_AGENT].search_count([('pan_no', '=', self.pan_no),('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
			if existing_record:
				raise UserError(_("PAN number must be unique"))


	@api.constrains('aadhaar_no')
	def aadhaar_no_validation(self):
		if self.aadhaar_no and not valid_aadhaar_no(self.aadhaar_no):
			raise UserError(_("Invalid Aadhaar number. Please enter the correct Aadhaar number"))
			if self.env[CM_AGENT].search_count([('aadhaar_no', '=', self.aadhaar_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)]):
				raise UserError(_("Aadhaar number must be unique"))

	@api.constrains('gst_no')
	def gst_no_validation(self):
		if self.gst_no:
			if not valid_gst_no(self.gst_no):
				raise UserError(_("Invalid GST number. Please enter the correct GST number"))			
			
			existing_gst = self.env[CM_AGENT].search_count([('gst_no', '=', self.gst_no), ('id', '!=', self.id), ('company_id', '=', self.company_id.id)])
			if existing_gst > 0:
				raise UserError(_("GST number must be unique"))


	@api.constrains('line_ids','email','mobile_no')
	def contact_details_validations(self):
		mobile_nos = {self.mobile_no}
		emails = {self.email.replace(" ", "").upper() if self.email else self.email}
		for item in self.line_ids:
			if item.email:
				emails.add(item.email.replace(" ", "").upper())
			if item.mobile_no:
				mobile_nos.add(item.mobile_no)
		if self.mobile_no:
			if len(mobile_nos) < (1 + len([item for item in self.line_ids if item.mobile_no])):
				raise UserError(_("Duplicate mobile numbers are not allowed within the provided contact details"))
		if self.email:
			if len(emails) < (1 + len([item for item in self.line_ids if item.email])):
				raise UserError(_("Duplicate emails are not allowed within the provided contact details"))
	
	@api.onchange('contract_agree')
	def onchange_contract_agree(self):
		if self.contract_agree != 'yes':
			self.validity_range = False
			self.from_date = False
			self.to_date = False
	
	@api.onchange('validity_range')
	def onchange_validity_range(self):
		if self.validity_range:
			self.from_date = False
			self.to_date = False
	
	@api.onchange('past_legal_action')
	def onchange_past_legal_action(self):
		if self.past_legal_action:
			self.legal_details = ''
	
	
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
	
	@api.onchange('agent_category')
	def onchange_agent_category(self):
		if self.agent_category == 'internal':
			self.contract_agree = 'no'
		else:
			self.contract_agree = ''
	
	@api.onchange('city_id')
	def onchange_city_id(self):
		if self.city_id:
			self.state_id = self.city_id.state_id
		else:
			self.state_id = False

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

	def validations(self):
		warning_msg = []
		is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
		if self.from_date and self.to_date and self.from_date >= self.to_date:
			raise UserError("Validity From Date should not be less than or Equal to Validity To Date")		
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
			if not self.short_name:
				self.short_name = self.name[:4].upper() + self.country_id.name.upper()	
			self.write({'status': 'active',
						'ap_rej_user_id': self.env.user.id,
						'ap_rej_date': time.strftime(TIME_FORMAT)})
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
		return super(CmAgent, self).write(vals)
	 
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
		
		
		cm_agent = self.env[CM_AGENT]
		result['all_draft'] = cm_agent.search_count([('status', '=', 'draft')])
		result['all_active'] = cm_agent.search_count([('status', '=', 'active')])
		result['all_inactive'] = cm_agent.search_count([('status', '=', 'inactive')])
		result['all_editable'] = cm_agent.search_count([('status', '=', 'editable')])
		result['my_draft'] = cm_agent.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
		result['my_active'] = cm_agent.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
		result['my_inactive'] = cm_agent.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
		result['my_editable'] = cm_agent.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
			  
		result['all_today_count'] = cm_agent.search_count([('crt_date', '>=', fields.Date.today())])
		result['all_month_count'] = cm_agent.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
		result['my_today_count'] = cm_agent.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
		result['my_month_count'] = cm_agent.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

		return result
