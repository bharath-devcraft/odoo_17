# -*- coding: utf-8 -*-

from odoo import models, fields

class CtDeliveryChallanAccessoriesDetailsLine(models.Model):
    _name = 'ct.delivery.challan.acc.details.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.delivery.challan.acc.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))
    lot_ids = fields.Many2many('ct.stock.lot', string="Serial No", domain="[('product_id','=',accessories_id),('store_pend_qty','>',0),('po_pend_qty','>',0)]")
 
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    entry_mode = fields.Selection(related='header_id.entry_mode', store=True)
    serial_no_req = fields.Selection(related='accessories_id.serial_no_req', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)