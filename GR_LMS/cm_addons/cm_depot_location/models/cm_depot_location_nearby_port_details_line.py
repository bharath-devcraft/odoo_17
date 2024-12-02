# -*- coding: utf-8 -*-
from odoo import models, fields,api

RES_COMPANY = 'res.company'

PORT_TYPE = [('seaport', 'Seaport'), ('airport', 'Airport'), ('dry_port', 'Dry(ICD) Port')]


class CmDepotLocationNearbyPortDetailsLine(models.Model):
    _name = 'cm.depot.location.nearby.port.details.line'
    _description = 'Near By Ports'
    _order = 'id asc'


    header_id = fields.Many2one('cm.depot.location', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    port_id = fields.Many2one('cm.port', string="Port Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    distance = fields.Integer(string='Distance(KM)' )
    port_type = fields.Selection(selection=PORT_TYPE, string="Port Type", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    @api.onchange('port_id')
    def onchange_port_id(self):
        if self.port_id:
            self.port_type = self.port_id.port_category
        else:
            self.port_type = False