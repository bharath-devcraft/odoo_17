# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmCountryLine(models.Model):
    _name = 'cm.country.line'
    _description = 'Festival Details'
    _order = 'id asc'

    header_id = fields.Many2one('res.country', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    date = fields.Date(string="Date", copy=False)
    name = fields.Char(string="Name")
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


