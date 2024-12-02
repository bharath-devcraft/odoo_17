# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmDriverMasterLangDetailsLine(models.Model):
    _name = 'cm.driver.master.lang.details.line'
    _description = "Language Details"
    _order = 'id asc'

    header_id = fields.Many2one('cm.driver.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Language Name", index=True, copy=False)
    lang_read = fields.Boolean(string="Read", default=False)
    lang_write = fields.Boolean(string="Write", default=False)
    lang_speak = fields.Boolean(string="Speak", default=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

