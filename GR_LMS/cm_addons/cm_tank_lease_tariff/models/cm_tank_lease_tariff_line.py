# -*- coding: utf-8 -*-
from odoo import models, fields, api

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COSTING_TYPE =  [('per_tank','Per Tank'),
                 ('per_document', 'Per Document'),
                 ('per_hour', 'Per Hour'),
                 ('per_day', 'Per Day')]

class CmTankLeaseTariffLine(models.Model):
	_name = 'cm.tank.lease.tariff.line'
	_description = 'Charges Details'
	_order = 'id asc'

	header_id = fields.Many2one('cm.tank.lease.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	charges_id = fields.Many2one('cm.charges.heads', string="Charge Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
	mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", default="yes", tracking=True)
	currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
	costing_type = fields.Selection(selection=COSTING_TYPE, string="Costing Type")
	unit_value = fields.Float(string="Value")
	note = fields.Html(string="Notes", sanitize=False)
	company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('charges_id')
	def onchange_charges_id(self):
		if self.charges_id:
			self.costing_type = self.charges_id.costing_type
		else:
			self.costing_type = ''
