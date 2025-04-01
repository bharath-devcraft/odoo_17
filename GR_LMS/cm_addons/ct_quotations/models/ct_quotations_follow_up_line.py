# -*- coding: utf-8 -*-

from odoo import models, fields

RES_USERS = 'res.users'

class CtQuotationsFollowUpLine(models.Model):
    _name = 'ct.quotations.follow.up.line'
    _description = 'Follow Up Log'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    user_id = fields.Many2one(RES_USERS, string="Added By", default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Added Date", default=fields.Datetime.now, readonly=True)
    next_followup_date = fields.Date(string="Next Follow Up Date", store=True)    
    notes = fields.Text(string="Notes")
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)