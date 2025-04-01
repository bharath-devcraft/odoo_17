# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

COSTING_TYPE =  [('per_tank','Per Tank'),
				 ('per_document', 'Per Document'),
				 ('per_hour', 'Per Hour'),
				 ('per_day', 'Per Day')]

class CmRepairTariffLine(models.Model):
	_name = 'cm.repair.tariff.line'
	_description = 'Details'
	_order = 'id asc'

	header_id = fields.Many2one('cm.repair.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)    
	repair_id = fields.Many2one('cm.repair.code', string="Repair Code", ondelete='restrict', tracking=True, domain="[('status', '=', 'active'), ('active_trans', '=', True)]")
	currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
	costing_type = fields.Selection(selection=COSTING_TYPE, string="Costing Type", default="per_tank")
	labour_time = fields.Float(string="Labour Time(Hrs.)")
	desc = fields.Char(string="Description", size=252)
	apply_special_labour = fields.Boolean(string="Apply Special Labour")
	labour_cost = fields.Float(string="Labour Cost")
	material_cost = fields.Float(string="Material Cost")
	actual_cost = fields.Float(string="Total Actual Cost")
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
	
	
	
	@api.constrains('repair_id')
	def _check_unique_damage_repair_combination(self):
		for record in self:
			duplicate = self.search([
				('repair_id', '=', record.repair_id.id),
				('header_id', '=', record.header_id.id)])
			if len(duplicate) > 1:
				raise UserError(
					_("Duplicate found for Repair Code: %s") %
					(record.repair_id.name))
	
	
	@api.onchange('labour_time','apply_special_labour')
	def onchange_labour_time(self):
		if self.labour_time > 0:
			if self.apply_special_labour == True:
				lobour_tot_cost = self.labour_time * self.header_id.spl_labour_cost			
				self.labour_cost = lobour_tot_cost 
				self.actual_cost = lobour_tot_cost + self.material_cost

			else:	
				lobour_tot_cost = self.labour_time * self.header_id.labour_cost			
				self.labour_cost = lobour_tot_cost 
				self.actual_cost = lobour_tot_cost + self.material_cost
		else:
			self.labour_cost = 0.00
			
	@api.onchange('material_cost')
	def onchange_material_cost(self):
		if self.material_cost > 0:
			self.actual_cost = self.material_cost + self.labour_cost
		else:
			self.actual_cost = 0.00
