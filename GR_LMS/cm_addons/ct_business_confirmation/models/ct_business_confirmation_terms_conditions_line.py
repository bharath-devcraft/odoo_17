# -*- coding: utf-8 -*-

from odoo import models, fields

class CtBusinessConfirmationTermsConditionsLine(models.Model):
    _name = 'ct.business.confirmation.terms.conditions.line'
    _description = 'Terms & Conditions'
    _order = 'id asc'

    header_id = fields.Many2one('ct.business.confirmation', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    description = fields.Text(string="Description", size=252)
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
