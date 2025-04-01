# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _
from odoo.exceptions import UserError

RES_USERS = 'res.users'

class CmRailTariffLadenChargesLine(models.Model):
    _name = 'cm.rail.tariff.laden.charges.line'
    _description = 'Laden Charges'
    _order = 'id asc'

    header_id = fields.Many2one('cm.rail.tariff', string="Header Ref",index=True, required=True, ondelete='cascade', c_rule=True)
    min_gross_weight = fields.Float(string="Minimum Gross Wt(MT)")
    max_gross_weight = fields.Float(string="Maximum Gross Wt(MT)")
    actual_cost = fields.Float(string="Actual Cost")
    busy_season_cost = fields.Float(string="Busy Season Cost")
    gr_cost = fields.Float(string="Total Actual Cost")
    dg_cost = fields.Float(string="DG Value", store=True, compute = '_compute_dg_cost_value')
    total_recover_value = fields.Float(string="Total Recover Value")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    @api.onchange('gr_cost')
    def onchange_gr_cost(self):
        if self.gr_cost and self.gr_cost < 0:
            raise UserError(_("Recovery value should not be lesser than zero"))
        
    @api.depends('header_id.laden_dg_extra', 'actual_cost','busy_season_cost','gr_cost')
    def _compute_dg_cost_value(self):
        if self.header_id.laden_dg_extra and 0 < self.header_id.laden_dg_extra <= 100:
            for line in self:
                line.dg_cost = ((line.gr_cost/ 100) * self.header_id.laden_dg_extra ) + line.gr_cost
                line.total_recover_value = line.dg_cost