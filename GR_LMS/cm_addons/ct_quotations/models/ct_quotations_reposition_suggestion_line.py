# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

ACCOUNT_TAX = 'account.tax'

class CtQuotationsRepositionSuggestionLine(models.Model):
    _name = 'ct.quotations.reposition.suggestion.line'
    _description = 'Reposition Route Suggestions'
    _order = 'tot_amt asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    service_name = fields.Char(string="Service Name", copy=False, related="carrier_sea_tariff_id.service_name")            
    carrier_id = fields.Many2one('cm.carrier', string="Carrier Name", ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)], related="carrier_sea_tariff_id.carrier_id")
    carrier_type = fields.Selection(selection=CARRIER_TYPE_OPTIONS, related="carrier_sea_tariff_id.carrier_type")
    tot_amt = fields.Float(string="Rate")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, related="carrier_sea_tariff_id.currency_id")
    tot_transit_days = fields.Integer(string="Total Transit Days", related="carrier_sea_tariff_id.transit_time")
    validity_date = fields.Date(string="Validity Date", related="carrier_sea_tariff_id.valid_to_date")
    carrier_sea_tariff_id =  fields.Many2one('cm.carrier.sea.freight.rate', string="Carrier Sea Freight Rate", ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)])
    line_tot_amt = fields.Float(string="Line Total")    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    def carrier_sea_freight_rate(self):
            return {
                'name': "Carrier Sea Freight Rate",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cm.carrier.sea.freight.rate',
                'res_id': self.carrier_sea_tariff_id.id,
                'target': 'new',
                'view_id': self.env.ref("cm_carrier_sea_freight_rate.cm_carrier_sea_freight_rate_form").id}
