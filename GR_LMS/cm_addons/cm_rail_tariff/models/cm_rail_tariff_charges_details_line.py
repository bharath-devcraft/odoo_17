# -*- coding: utf-8 -*-
from odoo import models, fields, api

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COSTING_TYPE =  [('per_tank','Per Tank'),
                 ('per_document', 'Per Document'),
                 ('per_hour', 'Per Hour'),
                 ('per_day', 'Per Day')]

class CmRailTariffChargesDetailsLine(models.Model):
    _name = 'cm.rail.tariff.charges.details.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.rail.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    charges_id = fields.Many2one('cm.charges.heads', string="Charge Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", default='yes', c_rule=True)
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)
    gr_cost = fields.Float(string="Actual Cost")
    recovery_value = fields.Float(string="Recovery Value")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
