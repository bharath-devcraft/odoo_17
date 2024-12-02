# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmTransportVendorBillingAddressLine(models.Model):
    _name = 'cm.transport.vendor.billing.address.line'
    _description = 'Billing Address'
    _order = 'id asc'


    header_id = fields.Many2one('cm.transport.vendor', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    eff_from_date = fields.Date(string="Effect From Date")
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    def validate_special_char(self, field_name, field_value):
        if field_value and is_special_char(self.env, field_value):
            raise UserError(_(f"Special character is not allowed in {field_name} field in billing address tab, Ref: {field_value}"))


    @api.constrains('email')
    def email_validation(self):
        for line in self:
            if line.email and  not valid_email(line.email):
                raise UserError(_(f"Email is invalid. Please enter the correct email in billing address tab, Ref : {line.email}"))

    @api.constrains('pin_code')
    def pin_code_validation(self):
        for line in self:
            if line.pin_code:
                if line.country_id.code == 'IN' and  not(len(str(line.pin_code)) == 6 and line.pin_code.isdigit() == True):
                    raise UserError(_(f"Invalid Pin Code(IN). Please enter the correct 6 digit pin code in billing address tab, Ref : {line.pin_code}") )
                else:
                    if not valid_pin_code(line.pin_code):
                        raise UserError(_(f"Invalid Pin Code. Please enter the correct pin code in billing address tab, Ref : {line.pin_code}") )
                    line.validate_special_char('Pin Code', line.pin_code)

    @api.constrains('eff_from_date')
    def eff_from_date_validation(self):
        for line in self:
            if line.eff_from_date:
                duplicate_count = line.search_count([('eff_from_date', '=', line.eff_from_date), ('header_id', '=', line.header_id.id)])
                if duplicate_count > 1:
                    raise UserError(_("Multiple billing addresses with the same effective from date are not allowed"))

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.country_id
        else:
            self.state_id = False
            self.country_id = False
