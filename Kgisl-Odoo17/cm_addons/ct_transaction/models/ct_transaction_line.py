from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'

class CtTransactionLine(models.Model):
    _name = 'ct.transaction.line'
    _description = 'Custom Transaction Line'
    _order = 'description'

    header_id = fields.Many2one('ct.transaction', string='Transaction Reference', index=True, required=True, ondelete='cascade')

    product_id = fields.Many2one('product.product', string="Product Name", 
                      ondelete='restrict', index=True)
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one('cm.master', string="Brand", tracking=True,
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(
        string="Quantity",
        digits=(2, 3))
    unit_price = fields.Float(
        string="Unit Price")
    disc_per = fields.Float(
        string="Discount %")
    disc_amt = fields.Float(
        string="DV",
        store=True, compute='_compute_total')
    taxes_id = fields.Many2many(ACCOUNT_TAX,string='Taxes', ondelete='restrict')
    unitprice_wt = fields.Float(
        string="Unit Price(WT)",
        store=True, help="Unit price with Taxes", compute='_compute_total')
    tax_amt = fields.Float(
        string="Tax amount")
    tot_amt = fields.Float(
        string="Line Total",
        store=True, compute='_compute_total')
    tax_amt = fields.Float(
        string="Tax amount",
        store=True, compute='_compute_total')
    line_tot_amt = fields.Float(
        string="Sub Total",
        store=True, compute='_compute_total')

    status = fields.Selection(related='header_id.status', store=True)
    
    # Child table declaration
    line_ids = fields.One2many('ct.transaction.serialno.line', 'header_id', string='Transaction Serialno Line', copy=True)


    ### Line total,Tax amount and Discount amount calculation ###
    @api.depends('qty', 'unit_price', 'taxes_id', 'disc_per')
    def _compute_total(self):
        """ _compute_total """

        for line in self:
            line.disc_amt = (line.qty * line.unit_price * line.disc_per) / 100
            amount_tax = 0
            if line.taxes_id and line.unit_price > 0:
                tax_results = self.env[ACCOUNT_TAX]._compute_taxes([line._convert_to_tax_base_line_dict()])
                totals = next(iter(tax_results['totals'].values()))
                amount_tax = totals['amount_tax']

            line.tax_amt = amount_tax
            line.unitprice_wt = (line.tax_amt / line.qty) + line.unit_price if line.qty else 0.00
            line.tot_amt = line.qty * line.unit_price
            line.line_tot_amt = (line.tot_amt + line.tax_amt) - line.disc_amt
    
    
    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env[ACCOUNT_TAX]._convert_to_tax_base_line_dict(
            self,
            partner=self.header_id.partner_id,
            currency=self.header_id.currency_id,
            product=self.product_id,
            taxes=self.taxes_id,
            price_unit=self.unit_price,
            quantity=self.qty,
            discount=self.disc_per,
            price_subtotal=self.tot_amt,
        )
    
    
    @api.onchange('product_id')
    def onchange_product(self):
        """ onchange_product """
        if self.product_id:
            self.description = self.product_id.name