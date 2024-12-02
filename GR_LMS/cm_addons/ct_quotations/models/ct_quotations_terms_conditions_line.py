# -*- coding: utf-8 -*-

from odoo import models, fields

class CtQuotationsTermsConditionsLine(models.Model):
    _name = 'ct.quotations.terms.conditions.line'
    _description = 'Terms & Conditions'
    _order = 'id asc'

    header_id = fields.Many2one('ct.quotations', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    term_name = fields.Char(string="Term Name", index=True, side=252)
    description = fields.Char(string="Description", size=252)
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
