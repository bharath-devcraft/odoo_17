# -*- coding: utf-8 -*-

from odoo import models, fields

class CtTransactionSerialnoLine(models.Model):
    _name = 'ct.transaction.serialno.line'
    _description = 'Serial Number'
    _order = 'id asc'

    header_id = fields.Many2one('ct.transaction.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    serial_no = fields.Char(string="Serial No", copy=False, size=252)
    qty = fields.Float(string="Quantity", digits=(2, 3))
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
