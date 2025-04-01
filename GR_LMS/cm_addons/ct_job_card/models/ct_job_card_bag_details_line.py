# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CtJobCardBagDetailsLine(models.Model):
    _name = 'ct.job.card.bag.details.line'
    _description = 'Bag Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.job.card', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    flexi_bag_id = fields.Many2one('product.template', string="Bag Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_bag')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    vendor_id = fields.Many2one('cm.vendor.master', string="Preferred Vendor", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Qty", digits=(2, 3), default=1)
    notes = fields.Text(string="Notes", copy=False)

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
