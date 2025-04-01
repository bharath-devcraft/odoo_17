# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

VESSEL_SERVICE_PROVIDERS = [('feeder', 'Feeder'), ('mlo', 'MLO'),
                            ('costal', 'Costal'), ('all', 'All')]

ACCOUNT_TAX = 'account.tax'

class CtQuotationsPositionRouteLine(models.Model):
    _name = 'ct.quotations.position.route.line'
    _description = 'Position Route Suggestions'
    _order = 'carrier_rate desc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    ves_serv_route_id = fields.Many2one('cm.vessel.service.route', string="Route Name Id", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    select = fields.Boolean(string="Select", store=True)
    name = fields.Char(string="Route Name", size=252, related='ves_serv_route_id.name')
    transit_days = fields.Integer(string="Transit Days")
    carrier_rate = fields.Float(string="Carrier Rate")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True)      
    vessel_type = fields.Selection(selection=VESSEL_SERVICE_PROVIDERS, string="Vessel Type", related='ves_serv_route_id.vessel_service_providers')
    line_tot_amt = fields.Float(string="Line Total")
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
                   
    def vessel_service_route_action(self):
            return {
                'name': "Vessel Service Route",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cm.vessel.service.route',
                'res_id': self.ves_serv_route_id.id,
                'target': 'new',
                'view_id': self.env.ref("cm_vessel_service_route.cm_vessel_service_route_form").id}
