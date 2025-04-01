# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('part_in', 'Part-Inward'),
    ('closed', 'Closed'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

class CtPurchaseRequestLine(models.Model):
    _name = 'ct.purchase.request.line'
    _description = 'Purchase Request Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.purchase.request', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('custom_type', '=', 'consumables'),('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    brand_id = fields.Many2one('cm.master', string="Brand", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))
    flag_used = fields.Boolean(string="Data Used", default=False)
    pending_qty = fields.Float(string="Pending Quantity", digits=(2, 3))
    po_pending_qty = fields.Float(string="PO Pending Quantity", digits=(2, 3))
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", compute="_compute_status", store=True, c_rule=True)
    request_no = fields.Char(related='header_id.name',string="Request No", store=True, c_rule=True)
    entry_date = fields.Date(related='header_id.entry_date',string="Entry Date", store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

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
            
    @api.depends('pending_qty')
    def _compute_status(self):
        for record in self:
            if record.status in ('approved','part_in'):
                if record.pending_qty == 0:
                    record.status = 'closed'
                elif record.pending_qty < record.qty:
                    record.status = 'part_in'
