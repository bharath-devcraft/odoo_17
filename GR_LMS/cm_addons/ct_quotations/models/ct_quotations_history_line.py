# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

APPLICABLE_OPTION = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

CARRIER_TYPE_OPTIONS = [('mlo', 'MLO'), ('feeder', 'Feeder'), ('agent', 'Agent')]

ACCOUNT_TAX = 'account.tax'

CT_QUOTATIONS = 'ct.quotations'

class CtQuotationsHistoryLine(models.Model):
    _name = 'ct.quotations.history.line'
    _description = 'Quotations History'
    _order = 'id asc'

    header_id = fields.Many2one(CT_QUOTATIONS, string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    quotation = fields.Char(staring="Quotation No", related="quotation_id.name")
    quotation_date = fields.Date(string="Quotation Date", related="quotation_id.entry_date")
    service_id = fields.Many2one('cm.service', string="Service Name", related="quotation_id.service_id")    
    bkg_party_id = fields.Many2one('cm.customer', string="Booking Party Name", ondelete='restrict', related="quotation_id.bkg_party_id")    
    booking_party_name = fields.Char(staring="Booking Party Name")    
    tot_amt = fields.Float(string="Total Value", related="quotation_id.tot_amt")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, related="quotation_id.currency_id")    
    quotation_status = fields.Selection(related='quotation_id.status', store=True, c_rule=True)
    quotation_id =  fields.Many2one(CT_QUOTATIONS, string="quotations", ondelete='restrict')
    line_tot_amt = fields.Float(string="Line Total")
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    def quotation_reference(self):
        return {
                'name': "Quotation",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ct.quotations',
                'res_id': self.quotation_id.id,
                'target': 'new',
                'view_id': self.env.ref("ct_quotations.ct_quotations_form").id}
