# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

RES_COMPANY = 'res.company'

class CtDomsBusinessConfirmationLine(models.Model):
    _name = 'ct.doms.business.confirmation.line'
    _description = 'Emergency Contact Details'
    _order = 'contact_person asc'

    header_id = fields.Many2one('ct.doms.business.confirmation', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
