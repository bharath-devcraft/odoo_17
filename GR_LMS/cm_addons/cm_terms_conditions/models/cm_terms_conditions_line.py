# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmTermsConditionsLine(models.Model):
    _name = 'cm.terms.conditions.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.terms.conditions', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    term_cond = fields.Text(string="T & C", index=True, copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
