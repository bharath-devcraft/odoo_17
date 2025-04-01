# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import timedelta

ACCOUNT_TAX = 'account.tax'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

WARRANTY_FROM = [('from_grn',
                                       'From GRN Date'),
                                      ('from_invoice',
                                       'From Sup Invoice Date'),
                                      ('custom',
                                       'Custom / Mfg Date')]
WARRANTY_CATEGORY=[('limited', 'Limited'), ('life_time', 'Perpetual/Life Time')]

ENTRY_TYPE = [('direct','Direct'),
                ('from_po','From PO')]

WARRANTY=[('applicable','Applicable'),
          ('not_applicable','Not Applicable')]

ENTRY_TYPE =  [('direct','Direct'),
               ('from_po','From PO'),
               ('from_pi','From PR')]


class CtGRNLine(models.Model):
    _name = 'ct.grn.line'
    _description = 'Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.grn', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    product_id = fields.Many2one('product.template', string="Product Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one(CM_MASTER, string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    qty = fields.Float(string="Quantity", digits=(2, 3))
    pending_qty = fields.Float(string="Pending Quantity", digits=(2, 3))
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
    po_qty = fields.Float(string="PO Qty", digits=(12, 3))
    pr_qty = fields.Float(string="PR Qty", digits=(12, 3))
    po_pending_qty = fields.Float(string="PO Pending Qty", digits=(12, 3))
    pr_pending_qty = fields.Float(string="PR Pending Qty", digits=(12, 3))
    entry_type = fields.Selection(selection=ENTRY_TYPE,related='header_id.entry_type', string="Mode of GRN", store=True)
    pr_line_id = fields.Many2one('ct.purchase.request.line', 'PR Line')
    po_line_id = fields.Many2one('ct.purchase.order.line', 'PO Line')

    warranty_flag = fields.Selection(selection=WARRANTY, string="Warranty")
    warranty_from = fields.Selection(selection=WARRANTY_FROM, string="Warranty From")
    warranty_date = fields.Date(string="Warranty From Date")
    warranty_to_date = fields.Date(string="Warranty To Date")
    warranty_period = fields.Integer(string="Warranty Period(Months)") 
    warranty_category = fields.Selection(selection=WARRANTY_CATEGORY, string="Warranty Category")
    attachment_ids = fields.Many2many('ir.attachment', string="Warranty File Attachment", ondelete='restrict', check_company=True)
    days = fields.Integer('Days')
    remarks = fields.Text('Remarks')
    entry_type = fields.Selection(selection=ENTRY_TYPE, related='header_id.entry_type', string="Mode of GRN")

    
    line_ids = fields.One2many('ct.grn.serialno.line', 'header_id', string='Serial Number', copy=True, c_rule=True)
    
    @api.onchange('warranty_flag','warranty_from','warranty_date','warranty_period','days')
    def onchange_warranty(self):
        if self.warranty_flag == 'applicable':
            if self.warranty_category == 'limited':
                if self.warranty_from == 'custom' and self.warranty_date:
                    new_date=self.warranty_date +relativedelta(months=self.warranty_period, days=self.days)
                    self.warranty_to_date = new_date
                elif self.warranty_from == 'from_grn' and self.header_id.entry_date:
                    new_date=self.header_id.entry_date +relativedelta(months=self.warranty_period, days=self.days)
                    self.warranty_to_date = new_date
                elif self.warranty_from == 'from_invoice' and self.header_id.partner_invoice_date:
                    new_date=self.header_id.partner_invoice_date +relativedelta(months=self.warranty_period, days=self.days)
                    self.warranty_to_date = new_date

        else:
            self.warranty_from=False
            self.warranty_date=False
            self.warranty_to_date=False
            self.warranty_period=False
            self.warranty_category=False
            self.attachment_ids=False
            self.days=False
    
    
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
            self.uom_id = self.product_id.uom_id if self.product_id.uom_id else ''
            if self.product_id.serial_no_req == 'required':
                self.warranty_flag = 'applicable'
    
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
    
    
    def unlink(self):
        for rec in self:
            if rec.po_line_id and rec.po_line_id.flag_used==True:
                rec.po_line_id.flag_used=False
            if rec.pr_line_id and rec.pr_line_id.flag_used==True:
                rec.pr_line_id.flag_used=False
            models.Model.unlink(rec)
        return True
