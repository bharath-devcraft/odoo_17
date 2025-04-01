# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CtRfqPartner(models.Model):
    _name = 'ct.rfq.partner'
    _description = 'RFQ Partner Details'
    _order = 'description asc'

    header_id = fields.Many2one('ct.rfq.line', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    partner_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict')
    description = fields.Char(string="Description", size=252)
    email = fields.Char(string="Email", size=252)
    part_address = fields.Char(string="Vendor Address")
    flag_mail = fields.Boolean(string="Mail Notification", default=True)    
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    
