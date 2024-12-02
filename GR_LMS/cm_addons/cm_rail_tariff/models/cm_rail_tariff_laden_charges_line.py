# -*- coding: utf-8 -*-
import time
from odoo import models, fields

RES_USERS = 'res.users'

class CmRailTariffLadenChargesLine(models.Model):
    _name = 'cm.rail.tariff.laden.charges.line'
    _description = 'Laden Charges'
    _order = 'id asc'

    header_id = fields.Many2one('cm.rail.tariff', string="Header Ref",index=True, required=True, ondelete='cascade', c_rule=True)
    min_gross_weight = fields.Float(string="Minimum Gross Wt(MT)", copy=False)
    max_gross_weight = fields.Float(string="Maximum Gross Wt(MT)", copy=False)
    actual_cost = fields.Float(string="Actual Cost", copy=False)
    busy_season_cost = fields.Float(string="Busy Season Cost", copy=False)
    gr_cost = fields.Float(string="GR Cost", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])