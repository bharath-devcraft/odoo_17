# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

class CtTransactionExpensesLine(models.Model):
    _name = 'ct.transaction.expenses.line'
    _description = 'Other Charges'
    _order = 'id asc'

    header_id = fields.Many2one('ct.transaction', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    expense_id = fields.Many2one(CM_MASTER, string="Expense", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    description = fields.Char(string="Description", size=252)
    amt = fields.Float(string="Amount", c_rule=True)
    disc_per = fields.Float(string="Discount(%)")
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    line_tot_amt = fields.Float(string="Line Total", store=True, compute='_compute_all_line')
    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)

    @api.depends('amt', 'disc_per', 'tax_ids')
    def _compute_all_line(self):
        for line in self:
            line.disc_amt = (line.amt * (line.disc_per / 100))

            amount_tax = 0
            sub_total = 0
            if line.tax_ids:
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
        self.ensure_one()
        return self.env[ACCOUNT_TAX]._convert_to_tax_base_line_dict(
            self,
            partner=self.header_id.partner_id,
            currency=self.header_id.currency_id,
            product= False,
            taxes=self.tax_ids,
            price_unit=self.amt,
            quantity=1,
            discount=self.disc_per,
            price_subtotal=self.line_tot_amt,
        )

    @api.onchange('disc_per')
    def onchange_discount_percentage(self):
        if self.disc_per < 0:
            raise UserError(_("Discount should be greater than or equal to zero"))
        if self.disc_per > 100:
            raise UserError(_("Discount should not be greater than hundred percent"))
