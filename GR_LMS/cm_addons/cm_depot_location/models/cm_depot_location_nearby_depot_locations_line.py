# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

CONTRACT_TYPE = [('own', 'Own'), ('lease', 'Lease'), ('rent', 'Rent')]

class CmDepotLocationNearbyDepotLocationsLine(models.Model):
    _name = 'cm.depot.location.nearby.depot.locations.line'
    _description = 'Near By Depots'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.location', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    port_location_id = fields.Many2one('cm.depot.location', string="Depot Location Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    distance = fields.Integer(string="Distance KM", copy=False)
    contract_type = fields.Selection(selection=CONTRACT_TYPE, string="Contract Type", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    @api.onchange('port_location_id')
    def onchange_port_location_id(self):
        if self.port_location_id:
            self.contract_type = self.port_location_id.contract_type
        else:
            self.contract_type = False