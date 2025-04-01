# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

class CmTransportTariffChargesLine(models.Model):
    _name = 'cm.transport.tariff.charges.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    charges_id = fields.Many2one('cm.charges.heads', string="Charges Heads", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", default='yes')
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    value = fields.Float(string="Value")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
