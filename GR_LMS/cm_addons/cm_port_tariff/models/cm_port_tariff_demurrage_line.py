# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CmPortTariffDemurrageLine(models.Model):
    _name = 'cm.port.tariff.demurrage.line'
    _description = 'Demurrage Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.port.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    minimum_days = fields.Integer(string="Minimum Days", copy=False)
    maximum_days = fields.Integer(string="Maximum Days", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True)
    actual_cost = fields.Float(string="Actual Cost", copy=False)
    gr_cost = fields.Float(string="GR Cost", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
