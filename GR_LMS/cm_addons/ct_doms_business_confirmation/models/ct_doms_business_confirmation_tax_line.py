# -*- coding: utf-8 -*-

from odoo import models, fields

class CtDomsBusinessConfirmationTaxLine(models.Model):
    _name = 'ct.doms.business.confirmation.tax.line'
    _description = 'Tax Breakup'
    _order = 'tax_name asc'

    header_id = fields.Many2one('ct.doms.business.confirmation', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    tax_name = fields.Char(string="Tax Name", copy=False, size=252)
    tax_amt = fields.Float(string="Tax Value", c_rule=True)	
    
    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
