# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CmDepotLocationLine(models.Model):
    _name = 'cm.depot.location.line'
    _description = 'Additional Contacts'
    _order = 'id asc'

    header_id = fields.Many2one('cm.depot.location', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    contact_person = fields.Char(string="Contact Person", size=50)
    designation = fields.Char(string="Designation", copy=False, size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)
    phone_no = fields.Char(string="Landline No / Ext", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    work_location = fields.Char(string="Work Location", copy=False, size=50)
    dep_name = fields.Char(string="Department", copy=False, size=50)
    skype = fields.Char(string="Skype ID", copy=False, size=50)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        for line in self:
            if line.mobile_no and line.header_id.country_id:
                if line.header_id.country_id.code == 'IN':
                    if not(len(str(line.mobile_no)) == 10 and line.mobile_no.isdigit() == True):
                        raise UserError(_(f"Mobile number(IN) is  invalid. Please enter correct mobile number in additional contact details tab, Ref : {line.mobile_no}"))
                if not valid_mobile_no(line.mobile_no):
                    raise UserError(_(f"Mobile number is  invalid. Please enter correct mobile number in additional contact details tab, Ref : {line.mobile_no}"))
                
    @api.constrains('whatsapp_no')
    def whatsapp_no_validation(self):
        for line in self:
            if line.whatsapp_no and line.header_id.country_id:
                if line.header_id.country_id.code == 'IN':
                    if not(len(str(line.whatsapp_no)) == 10 and line.whatsapp_no.isdigit() == True):
                        raise UserError(_(f"Whatsapp number(IN) is  invalid. Please enter correct Whatsapp number in additional contact details tab, Ref : {line.whatsapp_no}"))
                if not valid_mobile_no(line.whatsapp_no):
                    raise UserError(_(f"Whatsapp number is  invalid. Please enter correct Whatsapp number in additional contact details tab, Ref : {line.whatsapp_no}"))

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
