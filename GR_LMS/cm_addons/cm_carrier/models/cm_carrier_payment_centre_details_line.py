# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import is_alphabets,valid_account_no
from odoo.exceptions import UserError

RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

class CmCarrierPaymentCentreDetailsLine(models.Model):
    _name = 'cm.carrier.payment.centre.details.line'  
    _description = 'Payment Centre Details'
    _order = 'id asc'

    header_id = fields.Many2one('cm.carrier', string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)    
    contact_person = fields.Char(string="Contact Person", size=50)
    designation = fields.Char(string="Designation", size=252)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    whatsapp_no = fields.Char(string="WhatsApp No",copy=False, size=15)        
    email = fields.Char(string="Email", copy=False, size=252)
    street = fields.Char(string="Address Line 1", size=252)
    street1 = fields.Char(string="Address Line 2", size=252)
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    pin_code = fields.Char(string="Zip Code", copy=False, size=10)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict') 
    country_code = fields.Char(string="Country Code", copy=False, size=252)    
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    same_as_mobile = fields.Boolean(string="Same as Mobile Number", default=False, help="Click to apply same mobile number to whatsapp number")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    

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

    @api.onchange('same_as_mobile','mobile_no')
    def onchange_same_as_mobile(self):
        for rec in self:
            if rec.same_as_mobile:
                rec.whatsapp_no = rec.mobile_no
            else:
                rec.whatsapp_no = False
