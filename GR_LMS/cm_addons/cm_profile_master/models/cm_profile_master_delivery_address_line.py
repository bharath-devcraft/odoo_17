# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_special_char, valid_phone_no, valid_email, valid_pin_code, valid_gst_no, valid_cin_no, valid_website
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'
CM_COUNTRY_CODE = 'cm.country.code'

class CmProfileMasterDeliveryAddressLine(models.Model):
    _name = 'cm.profile.master.delivery.address.line'
    _description = 'Delivery Address'
    _order = 'id asc'

    header_id = fields.Many2one('cm.profile.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False, c_rule=True)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    ph_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Phone Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    cin_no = fields.Char(string="CIN No", copy=False, size=21)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    eff_from_date = fields.Date(string="Effective From Date")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    
    def validate_special_char(self, field_name, field_value):
        if field_value and is_special_char(self.env, field_value):
            raise UserError(_(f"Special character is not allowed in {field_name} field in delivery address tab, Ref: {field_value}"))
    
    @api.constrains('name', 'short_name', 'street', 'street1')
    def validate_fields(self):
        for line in self:
            line.validate_special_char('name', line.name)
            line.validate_special_char('short name', line.short_name)
            line.validate_special_char('Address Line 1', line.street)
            line.validate_special_char('Address Line 2', line.street1)

    @api.constrains('phone_no')
    def phone_no_validation(self):
        for line in self:
            if line.phone_no and not valid_phone_no(line.phone_no):
                raise UserError(_(f"Landline No / Ext is invalid. Please enter the correct Landline No / Ext with SDD code in delivery address tab, Ref : {line.phone_no}") )

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
                    raise UserError(_(f"Invalid zip code(IN). Please enter the correct 6 digit pin code in delivery address tab, Ref : {line.pin_code}") )
                else:
                    if not valid_pin_code(line.pin_code):
                        raise UserError(_(f"Invalid zip code. Please enter the correct pin code in delivery address tab, Ref : {line.pin_code}") )
                    line.validate_special_char('zip code', line.pin_code)

    @api.constrains('eff_from_date')
    def eff_from_date_validation(self):
        for line in self:
            if line.eff_from_date:
                if line.eff_from_date <= fields.Date.today():
                    raise UserError(_("The effective from date cannot be in past or current date. Please select a future date in delivery address tab"))
                
                latest_record = line.search([('header_id', '=', line.header_id.id)],order="eff_from_date desc", limit=1)
                if line.eff_from_date < latest_record.eff_from_date:
                    raise UserError(_("The effective from date cannot be earlier than the existing effective from date in delivery address tab"))

                duplicate_count = line.search_count([('eff_from_date', '=', line.eff_from_date), ('header_id', '=', line.header_id.id)])
                if duplicate_count > 1:
                    raise UserError(_("Multiple delivery addresses cannot have the same effective from date. Please choose a different effective from date in billing address tab"))
            else:
                raise UserError(_("The Effective From Date is mandatory for the address added in the Delivery Address tab. Please add it to proceed further"))

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

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code
            self.city_id = False
            self.state_id = False
            record = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1)
            c_code = record.id if record else False
            self.ph_cc_id = c_code
        else:
            self.country_code = False
            self.city_id = False
            self.state_id = False
            self.ph_cc_id = False
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
            self.pin_code = False
        else:
            self.state_id = False
            self.pin_code = False

    @api.onchange('city_id','state_id','header_id.pan_no','header_id.gst_category')
    def onchange_gst_category(self):
        if self.state_id and self.header_id.pan_no and self.header_id.gst_category=='registered':
            self.gst_no = str(self.state_id.short_name) + str(self.header_id.pan_no)
        else:
            self.gst_no = False