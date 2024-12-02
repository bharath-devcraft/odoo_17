# -*- coding: utf-8 -*-
from odoo import models, fields, api

RES_COMPANY = 'res.company'

BOUND_OPTIONS = [('east', 'East'),
            ('west', 'West')]

CUSTOM_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

SERVICE__AVAILABILITY_OPTION = [('all_days','All Days'),
                                ('specific_days','Specific Days'),
                                ('weekly','Weekly'),('monthly','Monthly'),
                                ('weekly_twice','Weekly Twice'),('ect', 'ect.')]

class CmVesselServiceRouteLine(models.Model):
    _name = 'cm.vessel.service.route.line'
    _description = 'Port Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.vessel.service.route', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    ports_id = fields.Many2one('cm.port', string="Port", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    entry_seq = fields.Integer(string="Sequence", copy=False)
    transshipment_days = fields.Integer(string="Transshipment Days", copy=False)
    bound = fields.Selection(selection=BOUND_OPTIONS, string="Bound", copy=False, tracking=True)
    berthing_days = fields.Integer(string="Berthing Days", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    hazardous_materials_allowed = fields.Selection(selection=YES_OR_NO, string="Hazardous Materials Allowed", copy=False)
    average_time_take = fields.Integer(string="Average Time Take", copy=False)
    service_availability = fields.Selection(selection=SERVICE__AVAILABILITY_OPTION, string="Service Availability", copy=False)
    specific_days = fields.Char(string="Specific Days", copy=False)
