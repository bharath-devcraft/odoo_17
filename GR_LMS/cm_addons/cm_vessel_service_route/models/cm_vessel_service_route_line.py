# -*- coding: utf-8 -*-
from odoo import api, models, fields

BOUND_OPTIONS = [('east', 'East'),
            ('west', 'West')]

CUSTOM_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

SERVICE_AVAILABILITY_OPTION = [('all_days','All Days'),
                                ('specific_days','Specific Days'),
                                ('weekly','Weekly'),('monthly','Monthly'),
                                ('weekly_twice','Weekly Twice'),('daily', 'Daily'),
                                ('weekdays_only','Weekdays Only(Monday-Friday)'),
                                ('weekends_only','Weekends Only')]

VESSEL_SERVICE_PROVIDERS = [('feeder', 'Feeder'), ('mlo', 'MLO'),
                            ('costal', 'Costal'), ('all', 'All')]

class CmVesselServiceRouteLine(models.Model):
    _name = 'cm.vessel.service.route.line'
    _description = 'Route Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.vessel.service.route', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    port_id = fields.Many2one('cm.port', string="Port Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    port_bound = fields.Selection(selection=BOUND_OPTIONS, string="Bound", copy=False, tracking=True)
    entry_seq = fields.Integer(string="Sequence", copy=False)
    service_availability = fields.Selection(selection=SERVICE_AVAILABILITY_OPTION, string="Service Availability", copy=False, default='all_days')
    specific_days = fields.Char(string="Specific Days", copy=False, size=252)
    berthing_days = fields.Integer(string="Berthing Days", copy=False)
    trans_days = fields.Integer(string="Transshipment Days", copy=False)
    avg_time = fields.Integer(string="Travel Time Days", copy=False)
    dg_product = fields.Selection(selection=YES_OR_NO, string="DG Materials Allowed" ,copy=False, c_rule=True)
    vessel_service_providers = fields.Selection(selection=VESSEL_SERVICE_PROVIDERS, string="Vessel Service Providers", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    @api.onchange('service_availability')
    def onchange_service_availability(self):
        self.specific_days = False