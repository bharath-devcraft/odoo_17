# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

MANDATORY_OPTIONS = [('yes', 'Yes'), ('no', 'No')]

OFFICIAL_DOC_OPTIONS = [('visible', 'Visible'),
                        ('not_visible', 'Not Visible')]

class CmServiceTermsConditionLine(models.Model):
    _name = 'cm.service.terms.condition.line'
    _description = 'Terms & Condition Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.service', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    term_name = fields.Char(string="Term Name", index=True, copy=False, side=252)
    description = fields.Char(string="Description", size=252)   
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

