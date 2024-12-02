# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

FEEDBACK_TYPE_OPTION = [('legals', 'Legals'),('transportation_cost', 'Transportation Cost'),
                        ('service_performance', 'Service Performance'), ('reliability', 'Reliability'),
                        ('accessibility', 'Accessibility'), ('capability', 'Capability'),
                        ('security', 'security'), ('past_incident', 'Past Incident')]

RATING_OPTIONS = [('0','0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class CmTransportVendorServiceFeedbackLine(models.Model):
    _name = 'cm.transport.vendor.service.feedback.line'
    _description = 'Service Feedback'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.vendor', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    feedback_type = fields.Selection(selection=FEEDBACK_TYPE_OPTION, string="Feedback Type", copy=False)
    rating = fields.Selection(selection=RATING_OPTIONS, string="Rating", copy=False)
    feedback = fields.Text(string="Feedback Notes", copy=False)        
    user_id = fields.Many2one('res.users', string="Added By", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    crt_date = fields.Date(string="Added Date", default=fields.Date.today)    
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

