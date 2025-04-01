# -*- coding: utf-8 -*-

from odoo import models, fields

class CtSalesReturnAccessoriesDetailsLine(models.Model):
    _name = 'ct.sales.return.acc.details.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.sales.return.acc.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    accessories_id = fields.Many2one('product.template', string="Accessories Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_accessories')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))

    return_lot_ids = fields.Many2many('ct.stock.lot', 'sales_return_details_lot_id', 'return_id', 'lot_id', string="Return Serial No", domain="[('product_id','=',accessories_id)]")
    dc_lot_ids = fields.Many2many('ct.stock.lot', 'dc_sales_return_details_lot_id', 'dc_id', 'lot_id', string="DC Serial No", domain="[('product_id','=',accessories_id)]")

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    serial_no_req = fields.Selection(related='accessories_id.serial_no_req', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)