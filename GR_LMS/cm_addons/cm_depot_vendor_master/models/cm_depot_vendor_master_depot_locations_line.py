# -*- coding: utf-8 -*-
from odoo import models, fields

RES_COMPANY = 'res.company'

CUSTOM_STATUS = [('active', 'Active'),
        ('inactive', 'Inactive')]

class CmDepotVendorMasterDepotLocationsLine(models.Model):
    _name = 'cm.depot.vendor.master.depot.locations.line'
    _description = 'Delivery Address'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.vendor.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    depot_id = fields.Many2one('cm.depot.location', string="Depot Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
