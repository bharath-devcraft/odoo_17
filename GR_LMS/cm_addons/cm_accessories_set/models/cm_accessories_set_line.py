# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmAccessoriesSetLine(models.Model):
	_name = 'cm.accessories.set.line'
	_description = 'Details'
	_order = 'id asc'

	header_id = fields.Many2one('cm.accessories.set', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
	accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
	uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict', tracking=True)
	qty = fields.Integer(string="Quantity", copy=False)
	unit_price = fields.Float(string="Unit Price", copy=False)
	tot_amt = fields.Float(string="Total Value", copy=False)
	note = fields.Html(string="Notes", copy=False, sanitize=False)
	company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

	@api.onchange('accessories_id','qty')
	def onchange_accessories_id(self):
		if self.accessories_id:
			self.uom_id = self.accessories_id.uom_id
			self.unit_price = self.accessories_id.standard_price
			self.tot_amt = self.accessories_id.standard_price * self.qty
		else:
			self.uom_id = False
			self.unit_price = 0.00
			self.tot_amt = 0.00
