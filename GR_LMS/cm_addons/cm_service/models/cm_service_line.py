# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

MANDATORY_OPTIONS = [('yes', 'Yes'), ('no', 'No'), ('term', 'Term')]

OFFICIAL_DOC_OPTIONS = [('visible', 'Visible'),
                        ('not_visible', 'Not Visible')]

class CmServiceLine(models.Model):
    _name = 'cm.service.line'
    _description = 'Charges Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.service', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Many2one('cm.charges.heads', string="Name", index=True, copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mandatory = fields.Selection(selection=MANDATORY_OPTIONS, string="Mandatory", copy=False)
    visible_doc = fields.Selection(selection=OFFICIAL_DOC_OPTIONS, string="Visible In Official Document", copy=False, default="not_visible")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

