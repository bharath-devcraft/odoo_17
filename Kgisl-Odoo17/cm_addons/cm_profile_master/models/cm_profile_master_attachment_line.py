import time
from odoo import models, fields, api
from odoo.exceptions import UserError

class CmProfileMasterAttachmentLine(models.Model):
    _name = 'cm.profile.master.attachment.line'
    _description = 'Custom Profile Master Attachment'

    header_id = fields.Many2one('cm.profile.master', string='Master Head Ref',
                                index=True, required=True, ondelete='cascade')
    attach_desc = fields.Char(string="Description", size=150)
    attachment = fields.Many2many('ir.attachment', string='File')
    attach_date = fields.Datetime(string='Attached Date', readonly=True, copy=False)
    attach_user_id = fields.Many2one('res.users', 'Attached By', readonly=True)

    #onchange
    @api.onchange('attachment')
    def _onchange_attachment(self):
        '''onchange_attachment'''
        if self.attachment:
            self.write({'attach_user_id': self.env.user.id,
                        'attach_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            self.write({'attach_user_id': False,
                        'attach_date': False})
