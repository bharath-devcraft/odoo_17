# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

class CmDepotJobSequenceLine(models.Model):
    _name = 'cm.depot.job.sequence.line'
    _description = 'Job Sequence Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.job.sequence', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    nature_of_job = fields.Many2one('cm.nature.of.job', string="Nature Of Job", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    note = fields.Text(string="Notes", copy=False, sanitize=False)
    sequence = fields.Integer(string="Sequence", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

