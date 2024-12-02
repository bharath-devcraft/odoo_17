# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmTransportVendorClientDetailsLine(models.Model):
    _name = 'cm.transport.vendor.client.details.line'
    _description = 'Client Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.transport.vendor', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    gr_customer_id = fields.Many2one('res.partner', string="GR Customer", ondelete='restrict') #,domain=[('status', '=', 'active'),('active_trans', '=', True)])
    name = fields.Char(string="Name", index=True, copy=False, c_rule=True)
    user_id = fields.Many2one('res.users', string="Added By", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    crt_date = fields.Date(string="Added Date", default=fields.Date.today)    
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    
    def validate_special_char(self, field_name, field_value):
        if field_value and is_special_char(self.env, field_value):
            raise UserError(_(f"Special character is not allowed in {field_name} field in client details tab, Ref: {field_value}"))
    
    @api.constrains('name')
    def validate_fields(self):
        for line in self:
            line.validate_special_char('name', line.name)
