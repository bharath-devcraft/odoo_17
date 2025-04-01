# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('part_in', 'Part-Inward'),
    ('closed', 'Closed'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

class CtPurchaseOrderLine(models.Model):
    _name = 'ct.purchase.order.line'
    _description = 'Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.purchase.order', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('custom_type', '=', 'consumables'),('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one(CM_MASTER, string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))
    unit_price = fields.Float(string="Unit Price")
    disc_per = fields.Float(string="Discount(%)")
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    unitprice_wt = fields.Float(string="Unit Price(WT)", help="Unit price with Taxes", store=True, compute='_compute_all_line')	
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')
    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')
    line_tot_amt = fields.Float(string="Line Total", store=True, compute='_compute_all_line')
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", compute="_compute_status", store=True, c_rule=True)
    
    flag_used = fields.Boolean(string="Data Used", default=False)
    pi_qty = fields.Float('PI Qty', digits=(12, 3))
    pending_qty = fields.Float('Pending Qty', digits=(12, 3))
    received_qty = fields.Float('Received Qty', store=True, compute='_compute_received_qty')
    entry_type = fields.Selection(related='header_id.entry_type', store=True)
    entry_mode = fields.Selection(related='header_id.entry_mode', store=True)
    pr_line_id = fields.Many2one('ct.purchase.request.line', string="Purchase Request Line", index=True)
    qc_id = fields.Many2one('ct.quotation.comparison', string="Comparison No", readonly = True)
    
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.depends('qty', 'unit_price', 'tax_ids', 'disc_per')
    def _compute_all_line(self):
        for line in self:
            line.disc_amt = (line.qty * line.unit_price * line.disc_per) / 100
            amount_tax = 0
            if line.tax_ids and line.unit_price > 0:
                tax_results = self.env[ACCOUNT_TAX]._compute_taxes([line._convert_to_tax_base_line_dict()])
                totals = next(iter(tax_results['totals'].values()))
                amount_tax = totals['amount_tax']

            line.tax_amt = amount_tax
            discounted_price = line.unit_price - (line.unit_price * (line.disc_per or 0) / 100)
            line.unitprice_wt = (line.tax_amt / line.qty) + discounted_price if line.qty else 0.00
            line.tot_amt = line.qty * line.unit_price
            line.line_tot_amt = (line.tot_amt + line.tax_amt) - line.disc_amt
    
    
    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        return self.env[ACCOUNT_TAX]._convert_to_tax_base_line_dict(
            self,
            partner=self.header_id.user_id,
            currency=self.header_id.currency_id,
            product=self.product_id,
            taxes=self.tax_ids,
            price_unit=self.unit_price,
            quantity=self.qty,
            discount=self.disc_per,
            price_subtotal=self.tot_amt,
        )
    
    
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

    @api.onchange('disc_per')
    def onchange_discount_percentage(self):
        if self.disc_per < 0:
            raise UserError(_("Discount should be greater than or equal to zero"))
        if self.disc_per > 100:
            raise UserError(_("Discount should not be greater than hundred percent"))

    @api.onchange('qty')
    def onchange_qty(self):
        self.pending_qty = self.qty

    @api.depends('qty', 'pending_qty')
    def _compute_received_qty(self):
        for rec in self:
            rec.received_qty = rec.qty - rec.pending_qty
    
    @api.depends('pending_qty')
    def _compute_status(self):
        for record in self:
            if record.status in ('approved','part_in'):
                if record.pending_qty == 0:
                    record.status = 'closed'
                elif record.pending_qty < record.qty:
                    record.status = 'part_in'

