# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

class CtEnquiryAttachmentLine(models.Model):
    _name = 'ct.enquiry.attachment.line'
    _description = 'Attachments'
    _order = 'id asc'

    header_id = fields.Many2one('ct.enquiry', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    attach_desc = fields.Char(string="Description", size=252)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    attach_user_id = fields.Many2one('res.users', string="Attached By", copy=False, ondelete='restrict', readonly=True)
    attach_date = fields.Datetime(string="Attached Date", copy=False, readonly=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)

    @api.onchange('attachment_ids')
    def onchange_attachment(self):
        if self.attachment_ids:
            self.attach_user_id = self.env.user.id
            self.attach_date = time.strftime('%Y-%m-%d %H:%M:%S')
