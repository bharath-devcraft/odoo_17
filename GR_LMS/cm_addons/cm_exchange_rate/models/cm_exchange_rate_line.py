# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmExchangeRateLine(models.Model):
    _name = 'cm.exchange.rate.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.exchange.rate', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True)
    exchange_rate = fields.Float(string="Exchange Rate")
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

