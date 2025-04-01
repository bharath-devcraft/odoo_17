# -*- coding: utf-8 -*-

from odoo import models, fields

class CtItemWiseIssueLine(models.Model):
    _name = 'ct.item.wise.issue.line'
    _description = 'Serial Number'
    _order = 'id asc'

    header_id = fields.Many2one('ct.store.issue.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    
    issue_line_id = fields.Many2one(
        'ct.store.issue.line',
        'Store Issue Line Entry')
    ct_grn_moves = fields.Many2many(
        'ct.stock.lot',
        string="GRN Entry",
        domain="[('product_id','=',product_id)]")
    product_id = fields.Many2one('product.template', string="Product", required=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    uom_id = fields.Many2one('uom.uom', string="UOM", readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)]) 
    grn_qty = fields.Integer(string="'GRN Quantity", required=True, digits=(12, 3))
    issue_qty = fields.Integer(string="'Utilized Quantity", digits=(12, 3))
    price_unit = fields.Float(string="Price Unit", digits=(12, 2))
    issue_date = fields.Date(string="Issue Date")
    lot_id = fields.Many2one('stock.lot', 'Lot Id')
    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
