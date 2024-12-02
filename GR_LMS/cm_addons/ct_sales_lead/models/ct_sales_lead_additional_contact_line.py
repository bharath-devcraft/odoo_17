# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no
from odoo.exceptions import UserError

class CtSalesLeadAdditionalContactLine(models.Model):
    _name = 'ct.sales.lead.additional.contact.line'
    _description = 'Additional Contact Details'
    _order = 'contact_person asc'

    header_id = fields.Many2one('ct.sales.lead', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    contact_person = fields.Char(string="Contact Person", size=50)
    designation = fields.Char(string="Designation", copy=False, size=50)
    dep_name = fields.Char(string="Department", copy=False, size=50)
    work_location = fields.Char(string="Work Location", copy=False, size=50)
    mobile_no = fields.Char(string="Mobile No", copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)
    email = fields.Char(string="Email", copy=False, size=252)
    skype = fields.Char(string="Skype ID", copy=False, size=50)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        for line in self:
            if line.mobile_no and not valid_mobile_no(line.mobile_no):
                raise UserError(_(f"Mobile number is  invalid. Please enter correct mobile number in additional contacts tab, Ref : {line.mobile_no}"))

    @api.constrains('whatsapp_no')
    def whatsapp_no_validation(self):
        for line in self:
            if line.whatsapp_no and not valid_mobile_no(line.whatsapp_no):
                raise UserError(_(f"WhatsApp number is  invalid. Please enter correct whatsApp number in additional contacts tab, Ref : {line.mobile_no}"))

    @api.constrains('email')
    def email_validation(self):
        for line in self:
            if line.email and not valid_email(line.email):
                raise UserError(_(f"Email is invalid. Please enter the correct email in  additional contacts tab, Ref : {line.email}"))
    
    @api.constrains('phone_no')
    def phone_validation(self):
        for line in self:
            if line.phone_no and not valid_phone_no(line.phone_no):
                raise UserError(_(f"Landline No / Ext is invalid. Please enter the correct Landline No / Ext with SDD code in additional contacts tab, Ref : {line.phone_no}"))