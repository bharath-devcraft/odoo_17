# -*- coding: utf-8 -*-
import time
import re
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf,is_mobile_num,is_valid_mail,is_alphanum
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

RES_USERS='res.users'
CM_PROFILE_MASTER='cm.profile.master'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmProfileMaster(models.Model):
    _name = 'cm.profile.master'
    _description = 'Base Custom Profile Master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, 
                 help="Maximum 4 char is allowed and will accept upper case only", size = 4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                              tracking=True, copy=False, default='draft')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
    note = fields.Html(string="Note", copy=False)
    
    #GENERAL INFORMATION
    contact_person = fields.Char(string="Contact Person", size=20)
    mobile_no = fields.Char(string="Mobile No", size=15)
    phone_no = fields.Char(string="Phone No", size=12)
    email = fields.Char(string="Email", copy=False, size=252)
    fax = fields.Char(string="Fax", copy=False, size=12)
    website = fields.Char(string="Website", copy=False, size=100)
    street = fields.Char(string="Street", size=252)
    street1 = fields.Char(string="Street1", size=252)
    landmark = fields.Char(string="Landmark", size=252)
    pincode = fields.Char(string="Zip", copy=False, size=10)
    city_id = fields.Many2one('cm.master', string="City",
               ondelete='restrict', domain=[('status', 'in', ['active']),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True,
                                 copy=False, tracking=True, ondelete='restrict')
    
    #OFFICIAL INFORMATION
    tds = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'TDS Applicable')
    tan_no = fields.Char(string="TAN", size=10)
    cst_no = fields.Char(string="CST No", copy=False, size=20)
    tin_no = fields.Char(string="TIN No", copy=False, size=18)
    cheque_favor = fields.Char(string="Cheque In Favor Of", copy=False, tracking=True, size=252)
    company_type = fields.Selection(string='Company Type',
            selection=[('person', 'Individual'), ('company', 'Company')])
    grade = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], 'Grade')
    pan_no = fields.Char(string="PAN No", copy=False, size=10)
    aadhar_no = fields.Char(string="Aadhar No", copy=False, tracking=True, size=12)
    gst_category = fields.Selection([('registered', 'Registered'), ('un_registered', 'Un Registered')], 'GST Category')
    gst_no = fields.Char(string="GST No", copy=False, size=15)

    #Entry info
    company_id = fields.Many2one('res.company', required=True, copy=False,
                      readonly=True, default=lambda self: self.env.company, ondelete='restrict')
    active = fields.Boolean('Visible', default=True)
    active_rpt = fields.Boolean('Visible in Report', default=True)
    active_trans = fields.Boolean('Visible in Transactions', default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", readonly=True, copy=False,
                                  tracking=True, default='manual')
    crt_date = fields.Datetime(string="Creation Date", readonly=True, copy=False,
                               default=fields.Datetime.now)
    user_id = fields.Many2one(RES_USERS, string="Created By", readonly=True, copy=False,
                                    ondelete='restrict', default=lambda self: self.env.user.id)
    ap_rej_date = fields.Datetime(string="Approved Date", readonly=True, copy=False)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved By", readonly=True, 
                                     copy=False, ondelete='restrict')
    inactive_date = fields.Datetime(string='Inactivated Date', readonly=True, copy=False)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", readonly=True,
                                 copy=False, ondelete='restrict')
    update_date = fields.Datetime(string="Last Updated Date", readonly=True, copy=False)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", readonly=True, copy=False,
                                    ondelete='restrict')

    #Line Ref
    line_ids = fields.One2many('cm.profile.master.line', 'header_id', string='Additional Contact Details', copy=True)
    line_ids_a = fields.One2many('cm.profile.master.attachment.line', 'header_id', string='Attachment', copy=True)
    line_ids_b = fields.One2many('cm.profile.master.billing.address.line', 'header_id', string='Billing Address', copy=True)
    line_ids_c = fields.One2many('cm.profile.master.bank.details.line', 'header_id', string='Bank Details', copy=True)
    line_ids_d = fields.One2many('cm.profile.master.delivery.address.line', 'header_id', string='Delivery Address', copy=True)
    
    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_('Special character is not allowed in name field'))

            name = self.name.upper()
            name = name.replace("'", "").replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_profile_master where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s""" %(name, self.id))
            data = self.env.cr.dictfetchall()
            if len(data) > 0:
                raise UserError(_('Profile master name must be unique'))
        return True

    @api.constrains('short_name')
    def short_name_validation(self):
        """ short_name_validation """
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_('Special character is not allowed in short name field'))

            short_name = self.short_name.upper()
            short_name = short_name.replace("'", "").replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_profile_master where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s""" %(short_name, self.id))
            data = self.env.cr.dictfetchall()
            if len(data) > 0:
                raise UserError(_('Profile master short name must be unique'))
        return True
        
    @api.constrains('phone_no')
    def phone_validation(self):
        if not(len(str(self.phone_no)) in (9, 10, 11, 12) and self.phone_no.isdigit() == True):
           raise UserError('Phone number is invalid. Please enter the correct phone number with SDD code')
        return True

    @api.constrains('mobile_no')
    def _check_mobile_no(self):
        if self.mobile_no and self.country_id:
            if self.country_id.code == 'IN':
                if not(len(str(self.mobile_no)) == 10 and self.mobile_no.isdigit() == True):
                    raise UserError(
                    _('Mobile number is  invalid. Please enter correct mobile number'))
            if is_mobile_num(self.mobile_no):
                raise UserError(
                    _('Mobile number is  invalid. Please enter correct mobile number'))
        return True

    @api.constrains('email')
    def _check_email(self):
        if self.email  and is_valid_mail(self.email):
                raise UserError(_('Email is invalid. Please enter the correct email'))
        return True
    

    @api.constrains('street')
    def _street_check(self):
        if self.street and is_special_char(self.env,self.street):
            raise UserError(_('Special character is not allowed in street field'))
        return True                

    @api.constrains('street1')
    def _street1_check(self):
        if self.street1 and is_special_char(self.env,self.street1):
                raise UserError(_('Special character is not allowed in street1 field'))
        return True

    @api.constrains('pincode')
    def _check_zip(self):
        if self.pincode:
            if self.country_id.code == 'IN':
                if len(str(self.pincode)) == 6 and self.pincode.isdigit() == True:
                    return True
                else:
                    raise UserError(_('Invalid zip code. Please enter the correct 6 digit zip code'))
            else:
                if len(str(self.pincode)) not in (6, 7, 8, 9, 10):
                    raise UserError(_('Invalid zip code. Please enter the correct zip code'))
                if is_special_char(self.env,self.pincode):
                    raise UserError(_('Special character is not allowed in zip code field'))

    @api.constrains('tin_no')
    def _check_tin(self):
        if self.tin_no:
            rec_ids = self.env[CM_PROFILE_MASTER].with_context(active_test=False).search([('tin_no', '=', self.tin_no), ('id', '!=', self.id)])
            if not rec_ids:
                if len(self.tin_no) < 11 or len(self.tin_no) > 18:
                    raise UserError(_('Invalid TIN number. Please enter the correct TIN number'))
                else:
                    return True
            else:
                raise UserError(_('TIN number must be Unique'))

    @api.constrains('pan_no')
    def _check_pan_no(self):
        if self.pan_no:
            rec_ids = self.env[CM_PROFILE_MASTER].with_context(active_test=False).search([('pan_no', '=', self.pan_no), ('id', '!=', self.id)])
            if not rec_ids:
                pattern = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
                if (len(self.pan_no) < 10 or len(self.pan_no) > 10) or not(re.match(pattern, self.pan_no)):
                    raise UserError(_('Invalid PAN number. Please enter the correct PAN number'))
                else:
                    return True
            else:
                raise UserError(_('PAN number must be Unique'))

    @api.constrains('tan_no')
    def _check_tan_no(self):
        if self.tan_no:
            rec_ids = self.env[CM_PROFILE_MASTER].with_context(active_test=False).search([('tan_no', '=', self.tan_no), ('id', '!=', self.id)])
            if not rec_ids:
                if len(self.tan_no) < 10 or len(self.tan_no) > 10:
                    raise UserError(_('Invalid TAN number. Please enter the correct TAN number'))
                else:
                    return True
            else:
                raise UserError(_('TAN number must be Unique'))

    @api.constrains('cst_no')
    def _check_cst(self):
        if self.cst_no:
            if len(str(self.cst_no)) == 11 and self.cst_no.isdigit() == True:
                return True
            else:
                raise UserError(_('Invalid CST number. Please enter the correct CST number'))

    @api.constrains('aadhar_no')
    def _check_aadhar_no(self):
        if self.aadhar_no:
            if len(str(self.aadhar_no)) == 12 and self.aadhar_no.isdigit() == True:
                return True
            else:
                raise UserError(_('Invalid aadhar number. Please enter the correct aadhar number'))

    @api.constrains('gst_no')
    def _check_gst_no(self):
        if self.gst_no:
            if len(str(self.gst_no)) == 15:
                return True
            else:
                raise UserError(_('Invalid GST number. Please enter the correct GST number'))

        if self.gst_category == 'yes' and self.gst_no:
            gst_no = self.gst_no.upper()
            gst_no = gst_no.replace(" ", "")
            self.env.cr.execute("""select upper(gst_no) from cm_profile_master where upper(REPLACE(gst_no, ' ', ''))  = '%s' """ %(gst_no))
            data = self.env.cr.dictfetchall()
            if len(data) > 1:
                raise UserError(_('GST number must be Unique'))


    @api.constrains('line_ids','email','mobile_no')
    def contact_details_validations(self):
        """Contact details validations"""
        mobile_nos = []
        emails = []
        mobile_nos.append(self.mobile_no)
        emails.append(self.email.replace(" ", "").upper())
        for item in self.line_ids:
            if item.email:
                emails.append((item.email.replace(" ", "")).upper())
            if item.mobile_no:
                mobile_nos.append(item.mobile_no)
        if list(dict.fromkeys(mobile_nos)) != mobile_nos:
            raise UserError(
                    _('Duplicate mobile numbers are not allowed within the provided contact details.'))

        if list(dict.fromkeys(emails)) != emails:
            raise UserError(
                    _('Duplicate emails  are not allowed within the provided contact details.'))


    @api.onchange('gst_category')
    def check_gst_category(self):
        self.gst_no = ''

    
    def validations(self):
        """ validations """
        warning_msg = []
        if not self.line_ids:
            warning_msg.append('System not allow to approve with empty line details')
        if self.status in ('draft', 'editable'):
            res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.rule_checker_master')
            is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
            if res_config_rule and self.user_id == self.env.user and not(is_mgmt): 
                warning_msg.append("Created user is not allow to approve the entry")
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(formatted_messages)
        else:
            return True
        

    def approve_warning_rule(self):
        """Warning Messages"""
        
        warning_msgs = []
        if not self.note:
            warning_msgs.append("Would you like to continue without notes")

        if warning_msgs:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view.id if view else False
            context = {
                'message': "\n\n".join(warning_msgs),
                'transaction_id': self.id,
                'transaction_model': CM_PROFILE_MASTER,
                'transaction_stage': self.status
            }
            return {
                'name': 'Warning',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view_id, 'form')],
                'view_id': view_id,
                'target': 'new',
                'context': context,
            }

        if self.status == 'draft':
            self.entry_approve()
        
        return True


    def entry_approve(self):
        """ entry_approve """
        self.validations()
        if self.status in ('draft', 'editable'):
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True

    def entry_draft(self):
        """ entry_draft """
        if self.status == 'active':
            self.write({'status': 'editable'})
            return True

    def entry_inactive(self):
        """ entry_inactive """
        if self.status == 'active':
            if self.inactive_remark:
                if self.inactive_remark.strip():
                    if len(self.inactive_remark.strip())>= 10:
                        self.write({'status':'inactive',
                                    'inactive_user_id': self.env.user.id,
                                    'inactive_date': time.strftime(TIME_FORMAT)})
                    else:
                        raise UserError(_('Minimum 10 characters are required for Inactive Remark'))
            else:
                raise UserError(
                    _('Inactive remark is must, Enter the remarks in Inactive Remark field'))
        else:
            raise UserError(
                    _('Unable to inactive other than active entry'))

    def unlink(self):
        """ Unlink """
        for rec in self:
            if rec.status not in ('draft') or rec.entry_mode == 'auto':
                raise UserError("You can't delete other than manually created draft entries")
            if rec.status in ('draft'):
                res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.del_draft_entry')
                is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
                if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                    raise UserError("You can't delete other users draft entries")
                models.Model.unlink(rec)
        return True

    def create(self, vals):
        """ create """
        if 'short_name' in vals:
            vals['short_name'] = vals.get('short_name').upper()
        return super(CmProfileMaster, self).create(vals)

    def write(self, vals):
        """ write """
        if 'short_name' in vals:
            short_name = vals['short_name'].upper()
        else:
            short_name = self.short_name.upper()
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id, 'short_name': short_name})
        return super(CmProfileMaster, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the transaction views.
        """

        result = {
            'all_draft': 0,
            'all_active': 0,
            'all_inactive': 0,
            'all_editable': 0,
            'my_draft': 0,
            'my_active': 0,
            'my_inactive': 0,
            'my_editable': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0,
        }
        
        
        #counts
        cm_profile_master = self.env[CM_PROFILE_MASTER]
        result['all_draft'] = cm_profile_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_profile_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_profile_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_profile_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_profile_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_profile_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_profile_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_profile_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_profile_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_profile_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_profile_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_profile_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
