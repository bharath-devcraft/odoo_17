# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

ACCOUNT_TAX = 'account.tax'

class CtQuotationsRePositionCarrierLine(models.Model):
    _name = 'ct.quotations.reposition.carrier.line'
    _description = 'Re-Position Carrier Suggestions'
    _order = 'pol,pod,tot_amt asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    service_name = fields.Char(string="Service Name", copy=False, related="carrier_sea_tariff_id.service_name")            
    carrier_id = fields.Many2one('cm.carrier', string="Carrier", ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)], related="carrier_sea_tariff_id.carrier_id")
    carrier_type = fields.Selection(selection=CARRIER_TYPE_OPTIONS, string="Type", related="carrier_sea_tariff_id.carrier_type")
    pol = fields.Char(string="POL", size=252, related="carrier_sea_tariff_id.pol_port_id.name")    
    carrier_term = fields.Char(string="Carrier Term", size=252, related="carrier_sea_tariff_id.carrier_term_id.name")
    pod = fields.Char(string="POD", size=252, related="carrier_sea_tariff_id.pod_port_id.name")        
    select = fields.Boolean(string="Select")
    imo_class = fields.Char(string="IMO Class", size=10)
    tot_amt = fields.Float(string="Rate")
    transit_days = fields.Integer(string="Transit Days", related="carrier_sea_tariff_id.transit_time")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, related="carrier_sea_tariff_id.currency_id")
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
