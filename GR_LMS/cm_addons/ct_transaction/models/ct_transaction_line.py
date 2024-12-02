# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

class CtTransactionLine(models.Model):
    _name = 'ct.transaction.line'
    _description = 'Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.transaction', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.product', string="Product Name", index=True, ondelete='restrict')
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
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    line_ids = fields.One2many('ct.transaction.serialno.line', 'header_id', string='S/N Details', copy=True, c_rule=True)

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
            line.unitprice_wt = (line.tax_amt / line.qty) + line.unit_price if line.qty else 0.00
            line.tot_amt = line.qty * line.unit_price
            line.line_tot_amt = (line.tot_amt + line.tax_amt) - line.disc_amt
    
    
    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        return self.env[ACCOUNT_TAX]._convert_to_tax_base_line_dict(
            self,
            partner=self.header_id.partner_id,
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
