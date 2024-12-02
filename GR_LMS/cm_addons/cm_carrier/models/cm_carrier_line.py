# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CmCarrierLine(models.Model):
    _name = 'cm.carrier.line'
    _description = 'Additional Contact'
    _order = 'id asc'

    header_id = fields.Many2one('cm.carrier', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    designation = fields.Char(string="Designation", size=252)    
    department = fields.Char(string="Department", size=252)
    work_location = fields.Char(string="Work Location", size=252)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)    
    landline_no = fields.Integer(string="Landline No / Ext", copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    skype = fields.Char(string="Skype ID", size=252)

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

    @api.constrains('email')
    def email_validation(self):
        for line in self:
            if line.email and not valid_email(line.email):
                raise UserError(_(f"Email is invalid. Please enter the correct email in  additional contact details tab, Ref : {line.email}"))

