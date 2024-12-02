# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

STAGE_OPTIONS = [('enquiry', 'Enquiry'), ('quotation', 'Quotation')]

class CmCarrierChecklistLine(models.Model):
    _name = 'cm.carrier.checklist.line'
    _description = 'Checklist'
    _order = 'id asc'

    header_id = fields.Many2one('cm.carrier', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    process_name = fields.Selection(selection=STAGE_OPTIONS, string="Stage", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

