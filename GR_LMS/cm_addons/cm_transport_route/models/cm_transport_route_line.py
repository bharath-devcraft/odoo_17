# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

TRAVEL_TYPE_OPTION = [('empty', 'Empty'),
                      ('laden', 'Laden')]

class CmTransportRouteLine(models.Model):
    _name = 'cm.transport.route.line'
    _description = 'Route Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.route', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    from_location_id = fields.Many2one('cm.transport.location', string="From Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    to_location_id = fields.Many2one('cm.transport.location', string="To Location", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)]) 
    travel_type = fields.Selection(selection=TRAVEL_TYPE_OPTION, string="Travel Type", copy=False)
    transit_days = fields.Float(string="Transit Days", copy=False)    
    distance = fields.Integer(string="Distance KM", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

            
