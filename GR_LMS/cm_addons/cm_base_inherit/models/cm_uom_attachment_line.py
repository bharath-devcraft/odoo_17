# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

class CmUomAttachmentLine(models.Model):
    _name = 'cm.uom.attachment.line'
    _description = 'Attachments'
    _order = 'id asc'

    header_id = fields.Many2one('uom.uom', string="Header Ref",index=True, required=True, ondelete='cascade', c_rule=True)
    attach_desc = fields.Char(string="Description", size=252)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
    attach_user_id = fields.Many2one('res.users', string="Attached By", copy=False, ondelete='restrict', readonly=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    

    @api.onchange('attachment_ids')
    def onchange_attachment_ids(self):
        if self.attachment_ids:
            self.write({'attach_user_id': self.env.user.id,
                        'attach_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            self.write({'attach_user_id': False,
                        'attach_date': False})
