# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_pin_code
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmCompanyDeliveryAddressLine(models.Model):
	_name = 'cm.company.delivery.address.line'
	_description = 'Delivery Address'
	_order = 'id asc'

	header_id = fields.Many2one('res.company', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	eff_from_date = fields.Date(string="Effective From Date", default=fields.Date.today)
	street = fields.Char(string="Street", size=252)
	street1 = fields.Char(string="Street1", size=252)
	pin_code = fields.Char(string="Zip Code", copy=False, size=10)
	city_id = fields.Many2one('cm.city', string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
	state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
	country_code = fields.Char(string="Country Code", copy=False, size=252)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	
	def validate_special_char(self, field_name, field_value):
		if field_value and is_special_char(self.env, field_value):
			raise UserError(_(f"Special character is not allowed in {field_name} field in delivery address tab, Ref: {field_value}"))
	
	@api.constrains('street', 'street1')
	def validate_fields(self):
		for line in self:
			line.validate_special_char('street', line.street)
			line.validate_special_char('street1', line.street1)

	@api.constrains('pin_code')
	def pin_code_validation(self):
		for line in self:
			if line.pin_code:
				if line.country_id.code == 'IN' and not(len(str(line.pin_code)) == 6 and line.pin_code.isdigit() == True):
					raise UserError(_(f"Invalid Pin Code(IN). Please enter the correct 6 digit pin code in delivery address tab, Ref : {line.pin_code}") )
				else:
					if not valid_pin_code(line.pin_code):
						raise UserError(_(f"Invalid Pin Code. Please enter the correct pin code in delivery address tab, Ref : {line.pin_code}") )
					line.validate_special_char('Pin Code', line.pin_code)

	@api.constrains('eff_from_date')
	def eff_from_date_validation(self):
		for line in self:
			if line.eff_from_date:
				duplicate_count = line.search_count([('eff_from_date', '=', line.eff_from_date), ('header_id', '=', line.header_id.id)])
				if duplicate_count > 1:
					raise UserError(_("Multiple billing addresses with the same effective from date are not allowed"))


	@api.onchange('country_id')
	def onchange_country_id(self):
		if self.country_id:
			self.country_code = self.country_id.code
			self.city_id = False
			self.state_id = False
		else:
			self.country_code = False
			self.city_id = False
			self.state_id = False
	
	@api.onchange('city_id')
	def onchange_city_id(self):
		if self.city_id:
			self.state_id = self.city_id.state_id
		else:
			self.state_id = False
