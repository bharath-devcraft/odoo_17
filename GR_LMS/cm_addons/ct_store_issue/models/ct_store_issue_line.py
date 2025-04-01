# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

ISSUE_TYPE=[('material', 'Material'),('service', 'Service')]

class CtStoreIssueLine(models.Model):
    _name = 'ct.store.issue.line'
    _description = 'Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.store.issue', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one(CM_MASTER, string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    from_location=fields.Char(string="From Location",copy=False)
    to_location=fields.Char(string="To Location",copy=False)
    issue_type = fields.Selection(selection=ISSUE_TYPE, string = "Issue Type", required=True, default="material")
    grn_line_id = fields.Many2one('ct.grn.line', 'GRN Line')
    stock_qty = fields.Float("Available Stock",compute='_get_stock_qty',store=True, digits=(12, 3))
    price_unit = fields.Float('Unit Price', digits=(12, 2))
    pending_qty = fields.Float('Pending Quantity', digits=(12, 3))
    remarks = fields.Text('Remarks')

    lot_ids = fields.Many2many('ct.stock.lot', string="Lot Entry", domain="[('product_id','=',product_id),('store_pend_qty','>',0),('po_pend_qty','>',0)]")
    line_ids = fields.One2many('ct.item.wise.issue.line', 'header_id', string='Utilize Number', copy=True, c_rule=True)

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id if self.product_id.uom_id else ''
            self.lot_ids=False
            self.line_ids=False
    
    @api.onchange('uom_id')
    def onchange_uom(self):
        if self.uom_id and self.product_id and self.product_id.uom_po_id and self.product_id.uom_id:
            if self.uom_id not in {self.product_id.uom_po_id, self.product_id.uom_id}:
                raise UserError(_("UOM is mismatch. Kindly check product master and choose."))
    
    @api.depends('product_id')
    def _get_stock_qty(self):
        if self.product_id:
            self.stock_qty = sum(self.env['ct.stock.lot'].search([('product_id', '=', self.product_id.id)]).mapped('store_pend_qty'))
            

        