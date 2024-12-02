from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'

class CtTransactionExpensesLine(models.Model):
    _name = 'ct.transaction.expenses.line'
    _description = 'Custom Transaction Expenses Line'

    header_id = fields.Many2one('ct.transaction', string='Transaction Reference', index=True, required=True, ondelete='cascade')

    expense_id = fields.Many2one('cm.master', string="Expense",
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    amt = fields.Float(
        string="Amount",
        store=True)
    disc_per = fields.Float(
        string="Discount %",
        store=True)
    disc_amt = fields.Float(
        string="DV",
        store=True, compute='_compute_total')
    taxes_id = fields.Many2many(ACCOUNT_TAX, string='Taxes', ondelete='restrict')
    line_tot_amt = fields.Float(
        string="Sub Total",
        store=True, compute='_compute_total')
    tax_amt = fields.Float(
        string="Tax amount",
        store=True, compute='_compute_total')

    status = fields.Selection(related='header_id.status', store=True)


    ### Line total,Tax amount and Discount amount calculation ###
    @api.depends('amt', 'disc_per', 'taxes_id')
    def _compute_total(self):
        """ _compute_total """

        for line in self:
            line.disc_amt = (line.amt * (line.disc_per / 100))

            amount_tax = 0
            sub_total = 0
            if line.taxes_id:
                if line.amt > 0 :
                    tax_results = self.env[ACCOUNT_TAX]._compute_taxes([line._convert_to_tax_base_line_dict()])
                    totals = next(iter(tax_results['totals'].values()))
                    amount_untaxed = totals['amount_untaxed']
                    amount_tax = totals['amount_tax']
                    sub_total = amount_untaxed + totals['amount_tax']
                else:
                    sub_total = 0
                    amount_tax = 0
            else:
                sub_total = line.amt - line.disc_amt

            line.tax_amt = amount_tax
            line.line_tot_amt = sub_total
    
    
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
            product= False,
            taxes=self.taxes_id,
            price_unit=self.amt,
            quantity=1,
            discount=self.disc_per,
            price_subtotal=self.line_tot_amt,
        )
