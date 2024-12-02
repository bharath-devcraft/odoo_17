# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import valid_mobile_no,valid_email,valid_phone_no

from odoo.exceptions import UserError

RES_COMPANY = 'res.company'

CM_CITY = 'cm.city'

RELATIONSHIP_TYPE = [('mother', 'Mother'), ('father', 'Father'),
                     ('brother', 'Brother'), ('sister', 'Sister'), 
                     ('wife', 'Wife'), ('son', 'Son'), ('guardian', 'Guardian')]

class CmDriverMasterLine(models.Model):
    _name = 'cm.driver.master.line'
    _description = 'Emergency Contact Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.driver.master', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    name = fields.Char(string="Name", index=True, copy=False)
    relationship = fields.Selection(selection=RELATIONSHIP_TYPE, string="Relationship", copy=False)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="Whats App No",copy=False, size=15)    
    email = fields.Char(string="Email", copy=False, size=252)
    address_line_1 = fields.Char(string="Address Line 1", size=252)
    address_line_2 = fields.Char(string="Address Line 2", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.country_id
        else:
            self.state_id = False
            self.country_id = False
        
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

