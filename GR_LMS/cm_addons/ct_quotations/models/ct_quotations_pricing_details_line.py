# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

ACCOUNT_TAX = 'account.tax'

class CtQuotationsPricingDetailsLine(models.Model):
    _name = 'ct.quotations.pricing.details.line'
    _description = 'Pricing Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    entry_seq = fields.Integer(string="Sequence")
    chrg_head_id = fields.Many2one('cm.charges.heads', string="Charges Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)]) #TODO
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Quantity", digits=(2, 3))	
    unit_price = fields.Float(string="Unit Price")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    disc_per = fields.Float(string="Discount(%)")
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    unitprice_wt = fields.Float(string="Unit Price(WT)", help="Unit price with Taxes", store=True, compute='_compute_all_line')
    markup_value = fields.Float(string="Markup Value")	
    tot_amt = fields.Float(string="Total Value", store=True, compute='_compute_all_line')
    tax_amt = fields.Float(string="Tax Value", store=True, compute='_compute_all_line')
    line_tot_amt = fields.Float(string="Line Total", store=True, compute='_compute_all_line')    
    line_applicable = fields.Selection(selection=APPLICABLE_OPTION, string="#", copy=False, tracking=True)
    entry_mode = fields.Selection(related='header_id.entry_mode', string="Entry Mode", default="manual", readonly=True, tracking=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    
    
    @api.depends('qty', 'unit_price', 'tax_ids', 'disc_per')
    def _compute_all_line(self):
        for line in self:
            line.disc_amt = (line.qty * (line.unit_price + line.markup_value) * line.disc_per) / 100
            amount_tax = 0
            if line.tax_ids and line.unit_price > 0:
                tax_results = self.env[ACCOUNT_TAX]._compute_taxes([line._convert_to_tax_base_line_dict()])
                totals = next(iter(tax_results['totals'].values()))
                amount_tax = totals['amount_tax']

            line.tax_amt = amount_tax
            line.unitprice_wt = (line.tax_amt / line.qty) + (line.unit_price + line.markup_value) if line.qty else 0.00
            line.tot_amt = line.qty * (line.unit_price + line.markup_value) 
            line.line_tot_amt = (line.tot_amt + line.tax_amt) - line.disc_amt
    
    
    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        return self.env[ACCOUNT_TAX]._convert_to_tax_base_line_dict(
            self,
            partner= False,#self.header_id.partner_id,
            currency= self.currency_id,
            product= False,#self.product_id,
            taxes=self.tax_ids,
            price_unit=self.unit_price + self.markup_value,
            quantity=self.qty,
            discount=self.disc_per,
            price_subtotal=self.tot_amt,
        )
    