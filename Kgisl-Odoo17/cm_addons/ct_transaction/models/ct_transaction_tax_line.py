from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError

class CtTransactionTaxLine(models.Model):
    _name = 'ct.transaction.tax.line'
    _description = 'Custom Transaction Tax Line'

    header_id = fields.Many2one('ct.transaction', string='Transaction Reference', index=True, required=True, ondelete='cascade')

    tax_name = fields.Char('Tax Name')
    tax_amt = fields.Float(
        string="Tax Value")	
    
    status = fields.Selection(related='header_id.status', store=True)
