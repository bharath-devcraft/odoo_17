import time
from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_mobile_num,is_valid_mail,is_alphanum

from odoo.exceptions import UserError

class CmSupplierCustomerLine(models.Model):
    _name = 'cm.supplier.customer.line'
    _description = 'Supplier/Customer Master Line'

    header_id = fields.Many2one('cm.supplier.customer', string='Master Head Reference',
                                index=True, required=True, ondelete='cascade')
    name = fields.Char(string="Name", index=True, copy=False)
    title = fields.Many2one('res.partner.title', string='Title')
    job_position = fields.Char(string='Job Position')
    mobile_no = fields.Char(string="Mobile No", size=15)
    phone_no = fields.Char(string="Phone No", size=12)
    email = fields.Char(string="Email", copy=False, size=252)
    attachment = fields.Many2many('ir.attachment', string='Attachment')
    note = fields.Html(string="Note", copy=False)

    @api.constrains('mobile_no')
    def _check_mobile_no(self):
        if self.mobile_no and self.header_id.country_id:
            if self.header_id.country_id.code == 'IN':
                if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
                    raise UserError(
                    _('Mobile number is  invalid. Please enter correct mobile number in additional contact details tab, Ref : %s')% self.mobile_no)
            if is_mobile_num(self.mobile_no):
                raise UserError(
                    _('Mobile number is  invalid. Please enter correct mobile number in additional contact details tab, Ref : %s')% self.mobile_no)
        return True

    @api.constrains('email')
    def _check_email(self):
        if self.email:
            if is_valid_mail(self.email):
                raise UserError(_('Email is invalid. Please enter the correct email in  additional contact details tab, Ref : %s')% self.email)
        return True
    
    @api.constrains('phone_no')
    def phone_validation(self):
        if len(str(self.phone_no)) in (9, 10, 11, 12) and self.phone_no.isdigit() == True:
            pass
        else:
           raise UserError(_('Phone number is invalid. Please enter the correct phone number with SDD code in additional contact details tab, Ref : %s')% self.phone_no)
        return True
