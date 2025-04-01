# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'
RES_COMPANY = 'res.company'

VALIDITY_SELECTION = [('limit', 'Limited'), ('no_limit', 'No Limit')]

IS_WARRANTY = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]
WARRANTY_CATEGORY = [('limited', 'Limited'), ('perpetual', 'Perpetual/Life Time')]
RFQ_MODE = [('pi','PI'),('si','SI')]
WARRANTY_FROM = [('from_grn','From GRN Date'),
                     ('from_invoice','From Sup Invoice Date'),
                     ('custom','Custom/Commissioning Date')]

class CtQuotationSubmitLine(models.Model):
    _name = 'ct.quotation.submit.line'
    _description = 'Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.quotation.submit', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('custom_type', '=', 'consumables'),('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    brand_id = fields.Many2one('cm.master', string="Brand", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    brand_desc = fields.Char(string="Brand Desc", size=252)
    qty = fields.Float(string="Quantity", digits=(2, 3))
    unit_price = fields.Float(string="Unit Price")
    disc_per = fields.Float(string="Discount(%)")
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    unitprice_wt = fields.Float(string="Unit Price(WT)", help="Unit price with Taxes", store=True, compute='_compute_all_line') 
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')
    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')
    line_tot_amt = fields.Float(string="Line Total", store=True, compute='_compute_all_line')
    
    discount_notes = fields.Text(string="Discount Remarks")
    tax_remarks = fields.Text(string="No Tax / Deviation Remarks")
    is_compared = fields.Boolean(string="Compared", default=False)
    specification = fields.Text(string="Specification")
    
    is_warranty = fields.Selection(related='header_id.is_warranty', selection=IS_WARRANTY, store=True, string="Warranty", copy=False)
    warranty_category = fields.Selection(related='header_id.warranty_category', selection=WARRANTY_CATEGORY, string="Warranty Category", store=True, copy=False)
    warranty_from = fields.Selection(related='header_id.warranty_from', selection=WARRANTY_FROM, string="Warranty From", store=True, copy=False)     
    warranty_period = fields.Float(related='header_id.warranty_period', string="Warranty Period(Months)", store=True, digits=(12,2), copy=False)
    warranty_date = fields.Date(related='header_id.warranty_date', string="Warranty From Date", store=True, copy=False)
    warranty_to_date = fields.Date(related='header_id.warranty_to_date', string="Warranty To Date", store=True, readonly=True, copy=False)
    days = fields.Integer(related='header_id.days', string="Days", store=True, copy=False)
    
    is_validity = fields.Selection(related='header_id.is_validity', selection=VALIDITY_SELECTION, string="Price Validity Range", store=True, copy=False)
    validity_period = fields.Integer(related='header_id.validity_period', string="Validity Period(Months)", store=True, copy=False)
    validity_period_days = fields.Integer(related='header_id.validity_period_days', string="Validity Period(Days)", store=True, copy=False)
    validity_date = fields.Date(related='header_id.validity_date', string="Validity Date", store=True, copy=False)
    
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
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
            partner=False,
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
    
    @api.onchange('brand_id')
    def onchange_brand(self):
        if self.brand_id:
            self.brand_desc = self.brand_id.name


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
