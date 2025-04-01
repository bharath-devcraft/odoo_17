# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CmPortTariffDemurrageLine(models.Model):
    _name = 'cm.port.tariff.demurrage.line'
    _description = 'Demurrage(Port Storage / Ground Rent) Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.port.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    minimum_days = fields.Integer(string="Minimum Days")
    maximum_days = fields.Integer(string="Maximum Days")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    actual_cost = fields.Float(string="Actual Cost")
    gr_cost = fields.Float(string="Recovery Value")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
