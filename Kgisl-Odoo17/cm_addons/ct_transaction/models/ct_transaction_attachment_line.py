from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError

class CtTransactionAttachmentLine(models.Model):
    _name = 'ct.transaction.attachment.line'
    _description = 'Custom Transaction Attachment Line'

    header_id = fields.Many2one('ct.transaction', string='Transaction Reference', index=True, required=True, ondelete='cascade')

    attach_desc = fields.Char(string="Attach Description", size=150)
    attachment = fields.Many2many(
        'ir.attachment',
        string='File',
        ondelete='restrict')
    attach_user_id = fields.Many2one('res.users', string="Attached By", readonly=True, copy=False,
                                    ondelete='restrict')
    attach_date = fields.Datetime(string='Attached Date', readonly=True, copy=False)

    status = fields.Selection(related='header_id.status', store=True)

    @api.onchange('attachment')
    def onchange_attachment(self):
        """ onchange_attachment """
        if self.attachment:
            self.attach_user_id = self.env.user.id
            self.attach_date = time.strftime('%Y-%m-%d %H:%M:%S')
