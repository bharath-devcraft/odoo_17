# -*- coding: utf-8 -*-

from odoo import models, fields

PAY_MODE_OPTIONS = [('cash', 'Cash'),
                    ('credit', 'Credit')]

class CtCustomerInvoiceReceiptDetailsLine(models.Model):
    _name = 'ct.customer.invoice.receipt.details.line'
    _description = 'Receipt Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.customer.invoice', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    received_date = fields.Date(string="Received Date", copy=False)
    payment_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False)
    ref_no = fields.Char(string="Ref No")
    received_amt = fields.Float(string="Received Amount")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)