# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmDriverMasterHealthHistoryLine(models.Model):
    _name = 'cm.driver.master.health.history.line'
    _description = "Driver's Health History"
    _order = 'id asc'


    header_id = fields.Many2one('cm.driver.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    mhc_date = fields.Date(string="Last Health Checkup Date")
    next_mhc_date = fields.Date(string="Next Health Checkup Date")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

