# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'
CM_COUNTRY_CODE = 'cm.country.code'

class CmCustomerCreditFormLine(models.Model):
    _name = 'cm.customer.credit.form.line'
    _description = 'Director Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.customer.credit.form', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No", size=15, copy=False)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    fax = fields.Char(string="Fax", copy=False, size=12)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    landmark = fields.Char(string="Landmark", size=252)
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    country_code = fields.Char(string="Country Code", copy=False, size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    designation = fields.Char(string="Designation", copy=False, size=50)
    skype = fields.Char(string="Skype ID")
    mb_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Mobile Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    wh_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Whatsapp Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    ph_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Phone Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])    
    same_as_mobile = fields.Boolean(string="Same as Mobile No", default=False, help="Click to apply same mobile number to whatsapp number")
    
    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        for line in self:
            if line.mobile_no and line.header_id.country_id:
                if line.header_id.country_id.code == 'IN':
                    if not(len(str(line.mobile_no)) == 10 and line.mobile_no.isdigit() == True):
                        raise UserError(_(f"Mobile number(IN) is  invalid. Please enter correct mobile number in additional contact details tab, Ref : {line.mobile_no}"))
                if not valid_mobile_no(line.mobile_no):
                    raise UserError(_(f"Mobile number is  invalid. Please enter correct mobile number in additional contact details tab, Ref : {line.mobile_no}"))

    @api.constrains('email')
    def email_validation(self):
        for line in self:
            if line.email and not valid_email(line.email):
                raise UserError(_(f"Email is invalid. Please enter the correct email in  additional contact details tab, Ref : {line.email}"))
    
    @api.constrains('phone_no')
    def phone_validation(self):
        for line in self:
            if line.phone_no and not valid_phone_no(line.phone_no):
                raise UserError(_(f"Landline No / Ext is invalid. Please enter the correct Landline No / Ext with SDD code in additional contact details tab, Ref : {line.phone_no}"))

    @api.constrains('pin_code')
    def pin_code_validation(self):
        for line in self:
            if line.pin_code:
                if line.country_id.code == 'IN' and  not(len(str(line.pin_code)) == 6 and line.pin_code.isdigit() == True):
                    raise UserError(_(f"Invalid Pin Code(IN). Please enter the correct 6 digit pin code in director details tab, Ref : {line.pin_code}") )
                else:
                    if not valid_pin_code(line.pin_code):
                        raise UserError(_(f"Invalid Pin Code. Please enter the correct pin code in director details tab, Ref : {line.pin_code}") )
                    line.validate_special_char('Pin Code', line.pin_code)

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            self.country_code = self.country_id.code
            self.city_id = False
            self.state_id = False
            record = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1)
            c_code = record.id if record else False
            self.mb_cc_id = c_code
            self.wh_cc_id = c_code
            self.ph_cc_id = c_code
        else:
            self.country_code = False
            self.city_id = False
            self.state_id = False
            self.mb_cc_id = False
            self.wh_cc_id = False
            self.ph_cc_id = False

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
        else:
            self.state_id = False
            
    @api.onchange('same_as_mobile')
    def onchange_same_as_mobile(self):
        for rec in self:
            if rec.same_as_mobile:
                rec.whatsapp_no = rec.mobile_no
                rec.wh_cc_id = rec.mb_cc_id
            else:
                rec.whatsapp_no = False
                rec.wh_cc_id = False
