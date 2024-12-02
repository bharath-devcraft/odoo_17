# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmVendorMasterDeliveryAddressLine(models.Model):
    _name = 'cm.vendor.master.delivery.address.line'
    _description = 'Delivery Address'
    _order = 'id asc'

    header_id = fields.Many2one('cm.vendor.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    pin_code = fields.Char(string="Zip code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    eff_from_date = fields.Date(string="Effective From Date")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    
    def validate_special_char(self, field_name, field_value):
        if field_value and is_special_char(self.env, field_value):
            raise UserError(_(f"Special character is not allowed in {field_name} field in delivery address tab, Ref: {field_value}"))
    
    @api.constrains('street', 'street1')
    def validate_fields(self):
        for line in self:
            line.validate_special_char('street', line.street)
            line.validate_special_char('street1', line.street1)

    @api.constrains('pin_code')
    def pin_code_validation(self):
        for line in self:
            if line.pin_code:
                if line.country_id.code == 'IN' and not(len(str(line.pin_code)) == 6 and line.pin_code.isdigit() == True):
                    raise UserError(_(f"Invalid zip code(IN). Please enter the correct 6 digit zip code in delivery address tab, Ref : {line.pin_code}") )
                else:
                    if not valid_pin_code(line.pin_code):
                        raise UserError(_(f"Invalid zip code. Please enter the correct zip code in delivery address tab, Ref : {line.pin_code}") )
                    line.validate_special_char('zip code', line.pin_code)

    @api.constrains('eff_from_date')
    def eff_from_date_validation(self):
        for line in self:
            if line.eff_from_date:
                duplicate_count = line.search_count([('eff_from_date', '=', line.eff_from_date), ('header_id', '=', line.header_id.id)])
                if duplicate_count > 1:
                    raise UserError(_("Multiple billing addresses with the same effective from date are not allowed"))

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code
            self.city_id = False
            self.state_id = False
        else:
            self.country_code = False
            self.city_id = False
            self.state_id = False
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
        else:
            self.state_id = False
