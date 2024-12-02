# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

class CmProfileMasterLine(models.Model):
    _name = 'cm.profile.master.line'
    _description = 'Additional Contact Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.profile.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    contact_person = fields.Char(string="Contact Person", size=50)
    title_id = fields.Many2one('res.partner.title', string="Title", copy=False, ondelete='restrict')
    job_position = fields.Char(string="Job Position", copy=False, size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    phone_no = fields.Char(string="Phone No", size=12, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    attachment_ids = fields.Many2many('ir.attachment', string="File", ondelete='restrict', check_company=True)
    note = fields.Html(string="Notes", copy=False, sanitize=False)
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
    
    @api.constrains('phone_no')
    def phone_validation(self):
        for line in self:
            if line.phone_no and not valid_phone_no(line.phone_no):
                raise UserError(_(f"Phone number is invalid. Please enter the correct phone number with SDD code in additional contact details tab, Ref : {line.phone_no}"))
