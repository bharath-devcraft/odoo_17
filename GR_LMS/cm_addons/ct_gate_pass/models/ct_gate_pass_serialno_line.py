# -*- coding: utf-8 -*-

from odoo import models, fields

class CtGatePassSerialnoLine(models.Model):
    _name = 'ct.gate.pass.serialno.line'
    _description = 'Serial Number'
    _order = 'id asc'

    header_id = fields.Many2one('ct.gate.pass.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', related='header_id.product_id', string="Product Name", index=True, ondelete='restrict',store=True)
    serial_no_id = fields.Many2one('ct.stock.lot', string="Serial No", required=True, domain="[('product_id','=',product_id)]")
    qty = fields.Float(string="Quantity", digits=(2, 3),default=1)
    warranty_details = fields.Text(string="Warranty Details")
    warranty_status = fields.Selection([('purchase',
                                         'Under Warranty - Purchase'),
                                        ('service',
                                         'Under Warranty - Service'),
                                        ('expired',
                                         'Expired')],
                                       'Warranty Status')
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
