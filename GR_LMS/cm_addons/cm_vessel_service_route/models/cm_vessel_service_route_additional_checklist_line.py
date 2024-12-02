# -*- coding: utf-8 -*-
from odoo import models, fields

class CmVesselServiceRouteAdditionalChecklistLine(models.Model):
    _name = 'cm.vessel.service.route.additional.checklist.line'
    _description = 'Additional Checklist'
    _order = 'id asc'

    header_id = fields.Many2one('cm.vessel.service.route', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    stage = fields.Char(string="Stage", index=True, copy=False, size=252)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

