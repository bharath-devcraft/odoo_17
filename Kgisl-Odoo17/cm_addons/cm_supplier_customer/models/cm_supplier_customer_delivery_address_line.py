import time
import re
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_mobile_num,is_valid_mail,is_alphanum
from odoo.exceptions import UserError

class CmSupplierCustomerDeliveryAddress(models.Model):
    _name = 'cm.supplier.customer.delivery.address.line'
    _description = 'Delivery Address'

    header_id = fields.Many2one('cm.supplier.customer', string='Master Head Reference',
                                index=True, required=True, ondelete='cascade')
    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, 
                 help="Maximum 4 char is allowed and will accept upper case only", size=4)
    tag_line = fields.Char('Tag Line', size=512)
    street = fields.Char(string="Street", size=252)
    street1 = fields.Char(string="Street1", size=252)
    pincode = fields.Char(string="Zip", copy=False, size=10)
    city_id = fields.Many2one('cm.master', string="City",
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    phone_no = fields.Char(string="Phone No", size=12)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    cin_no = fields.Char(string='CIN NO', size=21)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    effective_date = fields.Date(string='Effective From Date')
    
    
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_('Special character is not allowed in name field in delivery address tab , Ref : %s')% self.name)
                
    @api.constrains('short_name')
    def short_name_validation(self):
        """ short_name_validation """
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_('Special character is not allowed in short name field in delivery address tab , Ref : %s')% self.short_name)
    
    @api.constrains('street')
    def _street_check(self):
        if self.street:
            if is_special_char(self.env,self.street):
                raise UserError(_('Special character is not allowed in street field in delivery address tab, Ref : %s')% self.street)
        return True                

    @api.constrains('street1')
    def _street1_check(self):
        if self.street1:
            if is_special_char(self.env,self.street1):
                raise UserError(_('Special character is not allowed in street1 field in delivery address tab, Ref : %s')% self.street1)
        return True
    
    @api.constrains('phone_no')
    def phone_validation(self):
        if len(str(self.phone_no)) in (9, 10, 11, 12) and self.phone_no.isdigit() == True:
            pass
        else:
           raise UserError(_('Phone number is invalid. Please enter the correct phone number with SDD code in delivery address tab, Ref : %s')% self.phone_no)
        return True

    @api.constrains('email')
    def _check_email(self):
        if self.email:
            if is_valid_mail(self.email):
                raise UserError(_('Email is invalid. Please enter the correct email in delivery address tab, Ref : %s')% self.email)
        return True
        
    @api.constrains('gst_no')
    def _check_gst_no(self):
        if self.gst_no:
            if len(str(self.gst_no)) == 15:
                return True
            else:
                raise UserError(_('Invalid GST number. Please enter the correct GST number in delivery address tab, Ref : %s')% self.gst_no)
    
    @api.constrains('pincode')
    def _check_zip(self):
        if self.pincode:
            if self.country_id.code == 'IN':
                if len(str(self.pincode)) == 6 and self.pincode.isdigit() == True:
                    return True
                else:
                    raise UserError(_('Invalid zip code. Please enter the correct 6 digit zip code in delivery address tab, Ref : %s')% self.pincode)
            else:
                if not(len(str(self.pincode)) in (6, 7, 8, 9, 10)):
                    raise UserError(_('Invalid zip code. Please enter the correct zip code in delivery address tab, Ref : %s')% self.pincode)
                if is_special_char(self.env,self.pincode):
                    raise UserError(_('Special character is not allowed in zip code field in delivery address tab, Ref : %s')% self.pincode)
        return True
        
    @api.constrains('effective_date')
    def _check_effective_date(self):
        if self.effective_date:
            self.env.cr.execute(""" select id
            from cm_supplier_customer_delivery_address_line where effective_date='%s' 
            and header_id=%s """ %(self.effective_date, self.header_id.id))
            billing_add_data = self.env.cr.dictfetchall()
            if len(billing_add_data) > 1:
                raise UserError(_('Multiple delivery address with same effective from date is not allowed'))

    @api.constrains('cin_no')
    def _check_cin_no(self):
        if self.cin_no:
            if len(str(self.cin_no)) == 21:
                if is_special_char(self.env,self.cin_no):
                    raise UserError(_('Special character is not allowed in CIN number field in delivery address tab, Ref : %s')% self.cin_no)
                cin_no_space = ''.join(c for c in self.cin_no if  c in ' ')
                if cin_no_space:
                    raise UserError(_('Space is not allowed in CIN number field in delivery address tab, Ref : %s')% self.cin_no)
            else:
                raise UserError(_('Invalid CIN number. Please enter the correct CIN number in delivery address tab, Ref : %s')% self.cin_no)
        return True
        
    @api.constrains('website')
    def _check_website(self):
        if self.website and re.match(
                'www.(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?', self.website) is None:
            raise UserError(_('Website is invalid. Please enter the correct website in delivery address tab, Ref : %s')% self.website)
        else:
            pass
        return True


