# -*- coding: utf-8 -*-
from odoo import models, fields

RES_COMPANY = 'res.company'

class CmDepotLocationAuditChecklistLine(models.Model):
    _name = 'cm.depot.location.audit.checklist.line'
    _description = 'Audit Checklist'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.location', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False, c_rule=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    

    
    


