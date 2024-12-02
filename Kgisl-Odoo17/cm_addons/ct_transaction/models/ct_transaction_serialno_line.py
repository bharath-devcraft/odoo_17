from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError

class CtTransactionSerialnoLine(models.Model):
    _name = 'ct.transaction.serialno.line'
    _description = 'Custom Transaction Serialno Line'

    header_id = fields.Many2one('ct.transaction.line', string='Transaction Reference', index=True, required=True, ondelete='cascade')

    serial_no = fields.Char(string='Serial No')
    qty = fields.Float(
        string="Quantity",
        digits=(2, 3))
    expiry_date = fields.Date("Expiry Date")
    
    status = fields.Selection(related='header_id.status', store=True)
