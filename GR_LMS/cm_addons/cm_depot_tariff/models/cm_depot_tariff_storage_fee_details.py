# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmDepotTariffStorageFeeDetailsLine(models.Model):
    _name = 'cm.depot.tariff.storage.fee.details.line'
    _description = 'Storage Fee Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    minimum_days = fields.Integer(string="Minimum Days")
    maximum_days = fields.Integer(string="Maximum Days")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    actual_cost = fields.Float(string="Actual Cost")
    gr_cost = fields.Float(string="Recovery Value")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


