# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

COSTING_TYPE =  [('per_tank','Per Tank'),
                 ('per_document', 'Per Document'),
                 ('per_hour', 'Per Hour'),
                 ('per_day', 'Per Day')]

class CmDepotTariffLine(models.Model):
    _name = 'cm.depot.tariff.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.tariff', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    charges_id = fields.Many2one('cm.charges.heads', string="Charge Head", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mandatory = fields.Selection(selection=YES_OR_NO, string="Mandatory", default='yes')
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    costing_type = fields.Selection(selection=COSTING_TYPE, string="Costing Type")
    actual_cost = fields.Float(string="Actual Cost")
    gr_cost = fields.Float(string="Recovery Value")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


    @api.onchange('charges_id')
    def onchange_charges_id(self):
        if self.charges_id:
            self.costing_type = self.charges_id.costing_type
        else:
            self.costing_type = False