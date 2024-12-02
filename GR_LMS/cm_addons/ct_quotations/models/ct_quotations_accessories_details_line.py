# -*- coding: utf-8 -*-

from odoo import models, fields

class CtQuotationsAccessoriesDetailsLine(models.Model):
    _name = 'ct.quotations.acc.details.line'
    _description = 'Accessories Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations.flexi.bag.pricing.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    is_select = fields.Boolean(string="Select", default=True)
    accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))	
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)