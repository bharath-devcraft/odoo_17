# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

MANDATORY_OPTIONS = [('yes', 'Yes'), ('no', 'No')]


class CmServiceChecklistLine(models.Model):
    _name = 'cm.service.checklist.line'
    _description = 'Checklist'
    _order = 'id asc'

    header_id = fields.Many2one('cm.service', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    mandatory = fields.Selection(selection=MANDATORY_OPTIONS, string="Mandatory", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

