# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CtVendorInvoiceAdvanceLine(models.Model):
    _name = 'ct.vendor.invoice.advance.line'
    _description = 'Tax Breakup'
    _order = 'id desc'

    header_id = fields.Many2one('ct.vendor.invoice', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    adv_no = fields.Char(string="Advance No", copy=False)
    adv_date = fields.Date(string="Date", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    adv_amt = fields.Float(string="Advance Amount")    	
    adj_amt = fields.Float(string="Adjusted Amount")    	
    bal_amt = fields.Float(string="Balance Amount")    	
    cur_adj_amt = fields.Float(string="Current Adjustment")    	

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.onchange('adv_amt', 'adj_amt')
    def onchange_calculate_bal_amt(self):
        if self.adv_amt and self.adj_amt:
            bal_amt = self.adv_amt - self.adj_amt
            self.bal_amt = bal_amt
            self.cur_adj_amt = bal_amt
        else:
            self.bal_amt = False
            self.cur_adj_amt = False