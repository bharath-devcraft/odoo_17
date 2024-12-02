# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

CM_MASTER = 'cm.master'
RES_COMPANY = 'res.company'

class CmProfileMasterDeliveryAddressLine(models.Model):
    _name = 'cm.profile.master.delivery.address.line'
    _description = 'Delivery Address'
    _order = 'id asc'

    header_id = fields.Many2one('cm.profile.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False, c_rule=True)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    street = fields.Char(string="Street", size=252)
    street1 = fields.Char(string="Street1", size=252)
    pin_code = fields.Char(string="Pin Code", copy=False, size=10)
    city_id = fields.Many2one(CM_MASTER, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    phone_no = fields.Char(string="Phone No", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    cin_no = fields.Char(string="CIN No", copy=False, size=21)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    eff_from_date = fields.Date(string="Effect From Date", default=fields.Date.today)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    
    def validate_special_char(self, field_name, field_value):
        if field_value and is_special_char(self.env, field_value):
            raise UserError(_(f"Special character is not allowed in {field_name} field in delivery address tab, Ref: {field_value}"))
    
    @api.constrains('name', 'short_name', 'street', 'street1')
    def validate_fields(self):
        for line in self:
            line.validate_special_char('name', line.name)
            line.validate_special_char('short name', line.short_name)
            line.validate_special_char('street', line.street)
            line.validate_special_char('street1', line.street1)

    @api.constrains('phone_no')
    def phone_no_validation(self):
        for line in self:
            if line.phone_no and not valid_phone_no(line.phone_no):
                raise UserError(_(f"Phone number is invalid. Please enter the correct phone number with SDD code in delivery address tab, Ref : {line.phone_no}") )

    @api.constrains('email')
    def email_validation(self):
        for line in self:
            if line.email and not valid_email(line.email):
                raise UserError(_(f"Email is invalid. Please enter the correct email in delivery address tab, Ref : {line.email}"))
        
    @api.constrains('gst_no')
    def gst_no_validation(self):
        for line in self:
            if line.gst_no and not valid_gst_no(line.gst_no):
                raise UserError(_(f"Invalid GST number. Please enter the correct GST number in delivery address tab, Ref : {line.gst_no}") )


    @api.constrains('pin_code')
    def pin_code_validation(self):
        for line in self:
            if line.pin_code:
                if line.country_id.code == 'IN' and not(len(str(line.pin_code)) == 6 and line.pin_code.isdigit() == True):
                    raise UserError(_(f"Invalid Pin Code(IN). Please enter the correct 6 digit pin code in delivery address tab, Ref : {line.pin_code}") )
                else:
                    if not valid_pin_code(line.pin_code):
                        raise UserError(_(f"Invalid Pin Code. Please enter the correct pin code in delivery address tab, Ref : {line.pin_code}") )
                    line.validate_special_char('Pin Code', line.pin_code)

    @api.constrains('eff_from_date')
    def eff_from_date_validation(self):
        for line in self:
            if line.eff_from_date:
                duplicate_count = line.search_count([('eff_from_date', '=', line.eff_from_date), ('header_id', '=', line.header_id.id)])
                if duplicate_count > 1:
                    raise UserError(_("Multiple billing addresses with the same effective from date are not allowed"))

    @api.constrains('cin_no')
    def cin_no_validation(self):
        for line in self:
            if line.cin_no:
                if not valid_cin_no(line.cin_no):
                    raise UserError(_(f"Invalid CIN number. Please enter the correct CIN number in delivery address tab, Ref: {line.cin_no}"))
                line.validate_special_char('CIN number', line.cin_no)
                if ' ' in line.cin_no:
                    raise UserError(_(f"Space is not allowed in CIN number field in delivery address tab, Ref: {line.cin_no}"))

    @api.constrains('website')
    def website_validation(self):
        for line in self:
            if line.website and not valid_website(line.website):
                raise UserError(_(f"Website is invalid. Please enter the correct website in delivery address tab, Ref : {line.website}"))


