# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api,_
from odoo.exceptions import UserError

RES_USERS = 'res.users'
RES_COMPANY = 'res.company'

class CmBlClauseAttachmentLine(models.Model):
    _name = 'cm.bl.clause.attachment.line'
    _description = 'Attachments'
    _order = 'attach_date desc'

    header_id = fields.Many2one('cm.bl.clause', string="Header Ref",index=True, required=True, ondelete='cascade', c_rule=True)
    attach_desc = fields.Char(string="Description", size=252)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
    attach_user_id = fields.Many2one(RES_USERS, string="Attached By", copy=False, ondelete='restrict', readonly=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    @api.constrains('attach_desc')
    def attach_desc_validation(self):
        for line in self:
            desc = line.attach_desc.strip() if line.attach_desc else None
            if len(desc) < 3:
                raise UserError(_(f"Description field must contain at least 3 characters in the attachments tab. Ref: {line.attach_desc}"))    
    

    @api.onchange('attachment_ids')
    def onchange_attachment_ids(self):
        if self.attachment_ids:
            self.write({'attach_user_id': self.env.user.id,
                        'attach_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            self.write({'attach_user_id': False,
                        'attach_date': False})
