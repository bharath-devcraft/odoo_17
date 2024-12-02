# -*- coding: utf-8 -*-

from odoo import models, fields

class CtEnquiryDetailsLine(models.Model):
    _name = 'ct.enquiry.details.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.enquiry.flexi.acc.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    is_select = fields.Boolean(string="Select", default=True)
    accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))	
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
