# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACCOUNT_TAX = 'account.tax'
CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

class CtQuotationComparisonExpensesLine(models.Model):
    _name = 'ct.quotation.comparison.expenses.line'
    _description = 'Other Charges'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotation.comparison', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    vendor_1_expense_id = fields.Many2one('cm.master', string="Expense")
    vendor_1_description = fields.Char(string="Description", size=252)
    vendor_1_amt = fields.Float(string="Amount", c_rule=True)
    vendor_1_disc_per = fields.Float(string="Discount(%)")
    vendor_1_disc_amt = fields.Float(string="Discount Amount(-)")
    vendor_1_tax_ids = fields.Many2many(ACCOUNT_TAX, string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_1_line_tot_amt = fields.Float(string="Line Total")
    vendor_1_tax_amt = fields.Float(string="Tax Amount(+)")

    vendor_2_expense_id = fields.Many2one('cm.master', string="Expense")
    vendor_2_description = fields.Char(string="Description", size=252)
    vendor_2_amt = fields.Float(string="Amount", c_rule=True)
    vendor_2_disc_per = fields.Float(string="Discount(%)")
    vendor_2_disc_amt = fields.Float(string="Discount Amount(-)")
    vendor_2_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_expense_vendor_2_tax', 'expense_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_2_line_tot_amt = fields.Float(string="Line Total")
    vendor_2_tax_amt = fields.Float(string="Tax Amount(+)")
    
    vendor_3_expense_id = fields.Many2one('cm.master', string="Expense")
    vendor_3_description = fields.Char(string="Description", size=252)
    vendor_3_amt = fields.Float(string="Amount", c_rule=True)
    vendor_3_disc_per = fields.Float(string="Discount(%)")
    vendor_3_disc_amt = fields.Float(string="Discount Amount(-)")
    vendor_3_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_expense_vendor_3_tax', 'expense_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_3_line_tot_amt = fields.Float(string="Line Total")
    vendor_3_tax_amt = fields.Float(string="Tax Amount(+)")

    vendor_4_expense_id = fields.Many2one('cm.master', string="Expense")
    vendor_4_description = fields.Char(string="Description", size=252)
    vendor_4_amt = fields.Float(string="Amount", c_rule=True)
    vendor_4_disc_per = fields.Float(string="Discount(%)")
    vendor_4_disc_amt = fields.Float(string="Discount Amount(-)")
    vendor_4_tax_ids = fields.Many2many(ACCOUNT_TAX, 'm2m_quotation_expense_vendor_4_tax', 'expense_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    vendor_4_line_tot_amt = fields.Float(string="Line Total")
    vendor_4_tax_amt = fields.Float(string="Tax Amount(+)")

    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)