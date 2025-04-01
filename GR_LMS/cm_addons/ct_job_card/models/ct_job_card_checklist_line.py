# -*- coding: utf-8 -*-

from odoo import models, fields, api

IS_APPLICABLE = [('yes', 'Yes'), ('no', 'No')]


class CtJobCardChecklistLine(models.Model):
    _name = 'ct.job.card.checklist.line'
    _description = 'Checklist'
    _order = 'id asc'

    header_id = fields.Many2one('ct.job.card', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)

    description = fields.Char(string="Description", copy=False)
    is_applicable = fields.Selection(selection=IS_APPLICABLE, string="Applicable", copy=False)

    status = fields.Selection(related='header_id.status', store=True, c_rule=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
