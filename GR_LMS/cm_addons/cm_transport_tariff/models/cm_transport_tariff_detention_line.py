# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmTransportTariffLine(models.Model):
    _name = 'cm.transport.tariff.detention.line'
    _description = 'Detention Charges'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    minimum = fields.Integer(string="Minimum Hrs.", copy=False)
    maximum = fields.Integer(string="Maximum Hrs.", copy=False)
    value = fields.Integer(string="Per Hrs Value(INR)", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

