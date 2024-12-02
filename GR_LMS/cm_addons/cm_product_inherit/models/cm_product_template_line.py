# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmProductTemplateLine(models.Model):
    _name = 'cm.product.template.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('product.template', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    
