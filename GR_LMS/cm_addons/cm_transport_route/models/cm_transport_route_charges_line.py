# -*- coding: utf-8 -*-
from odoo import models, fields

RES_COMPANY = 'res.company'

MANDATORY_OPTIONS = [('yes', 'Yes'), ('no', 'No')]


class CmTransportRouteChargesLine(models.Model):
    _name = 'cm.transport.route.charges.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.route', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    charges_id = fields.Many2one('cm.charges.heads', string="Charge Head",copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mandatory = fields.Selection(selection=MANDATORY_OPTIONS, string="Mandatory", copy=False)
    value = fields.Float(string="Value", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', tracking=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

