# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CmExchangeRateLine(models.Model):
    _name = 'cm.exchange.rate.line'
    _description = 'Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.exchange.rate', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True)
    exchange_rate = fields.Float(string="Exchange Rate", digits=(2, 3))
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.constrains('exchange_rate','currency_id')
    def exchange_rate_validation(self):
        if self.exchange_rate <= 0:
            raise UserError(_("Exchange Rate should not be zero or negative."))