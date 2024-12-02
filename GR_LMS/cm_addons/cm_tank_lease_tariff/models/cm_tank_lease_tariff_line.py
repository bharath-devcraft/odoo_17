# -*- coding: utf-8 -*-
from odoo import models, fields, api

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

class CmTankLeaseTariffLine(models.Model):
	_name = 'cm.tank.lease.tariff.line'
	_description = 'Charges Details'
	_order = 'id asc'

	header_id = fields.Many2one('cm.tank.lease.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	charges_id = fields.Many2one('cm.charges.heads', string="Charge Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
	mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", copy=False, default="yes", tracking=True)
	currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
	tax_ids = fields.Many2many('account.tax', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
	unit_value = fields.Float(string="Value", copy=False)
	note = fields.Html(string="Notes", copy=False, sanitize=False)
	company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('charges_id')
	def onchange_charges_id(self):
		if self.charges_id:
			self.tax_ids = self.charges_id.tax_ids
		else:
			self.tax_ids = [(5, 0, 0)]
