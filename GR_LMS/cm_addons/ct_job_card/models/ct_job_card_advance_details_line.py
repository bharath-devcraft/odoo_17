# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CtJobCardAdvanceDetailsLine(models.Model):
    _name = 'ct.job.card.advance.details.line'
    _description = 'Advance Details'
    _order = 'id asc'

    header_id = fields.Many2one('ct.job.card', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    chrg_head_id = fields.Many2one('cm.charges.heads', string="Charges Head", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    emp_id = fields.Many2one('cm.employee', string="Service Engineer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    value = fields.Float(string="Value")
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    notes = fields.Text(string="Notes", copy=False)

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
