# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CtRfqLine(models.Model):
    _name = 'ct.rfq.line'
    _description = 'RFQ Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.rfq', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('custom_type', '=', 'consumables'),('status', '=', 'active'),('active_trans', '=', True)])
    pr_line_id = fields.Many2one('ct.purchase.request.line', string="Purchase Request Line", index=True, ondelete='restrict')
    description = fields.Char(string="Description", size=252)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    brand_id = fields.Many2one('cm.master', string="Brand", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))
    request_qty = fields.Float(string="Request Quantity", digits=(2, 3))
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    due_date = fields.Date(related='header_id.due_date',string="Due Date", store=True, c_rule=True)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    line_ids = fields.One2many('ct.rfq.partner', 'header_id', string="Vendor Details", copy=True, c_rule=True)
	
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_po_id if self.product_id.uom_po_id else ''
    
    @api.onchange('uom_id')
    def onchange_uom(self):
        if self.uom_id and self.product_id and self.product_id.uom_po_id and self.product_id.uom_id:
            if self.uom_id not in {self.product_id.uom_po_id, self.product_id.uom_id}:
                raise UserError(_("UOM is mismatch. Kindly check product master and choose."))
