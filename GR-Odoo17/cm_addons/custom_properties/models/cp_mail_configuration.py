
import time
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import Counter
from dateutil.relativedelta import relativedelta
from odoo.addons.custom_properties.decorators import is_special_char,valid_email

_logger = logging.getLogger(__name__)

CP_MAIL_CONFIGURATION = 'cp.mail.configuration'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
    ('draft', "Draft"),
    ('editable', 'Editable'),
    ('active', "Active"),
    ('inactive', "Inactive")]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

MAIL_TYPE =  [('transaction','Transaction Mail'),
              ('scheduler','Scheduler Mail')]

class CpMailConfiguration(models.Model):
    _name = 'cp.mail.configuration'
    _description = 'Custom Mail Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    mail_type = fields.Selection(selection=MAIL_TYPE, string='Mail Type',)
    model_name = fields.Many2one('ir.model','Model Name')
    name = fields.Char('Mail Name', index=True, copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True, copy=False, default='draft')
    subject = fields.Char('Subject')
    from_mail_id = fields.Char('From Email-ID')
    interval = fields.Char('Interval')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
    note = fields.Html(string="Note", copy=False)

    ### Entry Info ###
    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean('Visible in Report', default=True)
    active_trans = fields.Boolean('Visible in Transactions', default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", readonly=True, copy=False,
                                  tracking=True, default='manual')
    company_id = fields.Many2one('res.company', required=True, copy=False,
                      readonly=True, default=lambda self: self.env.company, ondelete='restrict')
    user_id = fields.Many2one(RES_USERS, string="Created By", readonly=True, copy=False,
                                    ondelete='restrict', default=lambda self: self.env.user.id)
    crt_date = fields.Datetime(string="Creation Date", readonly=True, copy=False, default=fields.Datetime.now)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved By", readonly=True, 
                                     copy=False, ondelete='restrict')
    ap_rej_date = fields.Datetime(string="Approved Date", readonly=True, copy=False)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", readonly=True,
                                 copy=False, ondelete='restrict')
    inactive_date = fields.Datetime(string='Inactivated Date', readonly=True, copy=False)
    update_user_id = fields.Many2one(RES_USERS, string="Last Update By", readonly=True, copy=False,
                                    ondelete='restrict')
    update_date = fields.Datetime(string="Last Update Date", readonly=True, copy=False)
        
    # Child table declaration
    line_ids = fields.One2many('cp.mail.configuration.line', 'header_id', string='Mail Configuration Lines', copy=True)

    ## Validation ##
    def validations(self, **kw):
        """ Validations """
        warning_msg = []
        if not self.line_ids:
            warning_msg.append('System not allow to approve with empty line details')
        
        # ~ to_add = self.line_ids.filtered(lambda m: m.to_address is True).mapped('to_address')
        # ~ if not to_add:
            # ~ raise UserError('Minimum one to mail id is must')

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
    
    @api.constrains('line_ids')
    def _user_email_validation(self):

        if self.status == 'active' and not self.line_ids:
            raise UserError("You cannot delete all the entries; instead, you can inactivate the record")

        to_addresses = []
        cc_addresses = []
        bcc_addresses = []
        for line in self.line_ids:
            if not any([line.to_address, line.cc_address, line.bcc_address]):
                raise UserError('Either you have to select To, Cc, or Bcc for: {}'.format(line.email))
            if line.email and not valid_email(line.email):
                raise UserError(_('Email is not valid, check the given email for: {}'.format(line.email)))
            if line.to_address:
                to_addresses.append(line.email)
            if line.cc_address:
                cc_addresses.append(line.email)
            if line.bcc_address:
                bcc_addresses.append(line.email)

        # Consolidate all email addresses
        all_addresses = to_addresses + cc_addresses + bcc_addresses

        # Check for duplicates
        duplicates = [email for email, count in Counter(all_addresses).items() if count > 1]

        if duplicates:
            raise UserError('Duplicate mail ids are not allowed. Remove duplicates: {}'.format(', '.join(duplicates)))

        return True

    @api.constrains('name', 'mail_type')
    def _check_name_constrains(self):
        if self.name:
            self._special_char_check(self.name, 'mail name')
            
            name = self.name.upper().replace(" ", "")
            query = """ 
                SELECT UPPER(name),id
                FROM cp_mail_configuration 
                WHERE mail_type = %s
                AND UPPER(REPLACE(name, ' ', '')) = %s
                AND id != %s
            """

            params = [self.mail_type, name, self.id]

            if self.mail_type == 'transaction':
                query += "AND model_name = %s"
                params.append(self.model_name.id)

            self.env.cr.execute(query, params)
            if self.env.cr.fetchone():
                raise UserError(_('Mail config name must be unique'))
        return True

    @api.constrains('from_mail_id')
    def _check_email_constrains(self):
        if self.from_mail_id:
            self._special_char_check(self.from_mail_id, 'from email id')
            self._check_email(self.from_mail_id)
        return True

    @api.constrains('interval')
    def _check_interval_constrains(self):
        if self.interval:
            self._special_char_check(str(self.interval), 'interval')
        return True

    def _special_char_check(self, value, label):
        if is_special_char(self.env,value):
            raise UserError(_('Special character is not allowed in %s field' % (label)))
        return True

    def _check_email(self, value):
        if not valid_email(value):
            raise UserError(_('From email id is not valid, check the given email'))
        return True

    @api.onchange('mail_type')
    def mail_type_onchange(self):
        self.model_name = ''
        self.name = ''

    @api.onchange('model_name')
    def model_name_onchange(self):
        self.name = ''

    def entry_approve(self):
        """ entry_approve """ 
        if self.status in ('draft', 'editable'):
            self.validations()
            self.write({
                    'status' : 'active',
                    'ap_rej_user_id': self.env.user.id,
                    'ap_rej_date': time.strftime(TIME_FORMAT)
                })

        return True
    
    def entry_draft(self):
        """ entry_draft """
        if self.status == 'active':
            if not(self.env[RES_USERS].has_group('custom_properties.group_set_to_draft')):
                raise UserError(_("You can't draft this entry. Draft Admin have the rights"))
            self.write({'status': 'editable'})
        return True

    def entry_inactive(self):
        """ entry_inactive """
        if self.status != 'active':
            raise UserError(_('Unable to inactivate entry other than active.'))

        if not self.inactive_remark or not self.inactive_remark.strip():
            raise UserError(_('Inactive remark is required. Please enter remarks in the Inactive Remark field.'))

        if len(self.inactive_remark.strip()) < 10:
            raise UserError(_('Minimum 10 characters are required for the Inactive Remark.'))

        self.write({
            'status': 'inactive',
            'inactive_user_id': self.env.user.id,
            'inactive_date': time.strftime(TIME_FORMAT)
        })

        return True

    def process_mail_forms(self, mail_form_ids, val):
        """Processes mail forms to segregate email addresses."""

        for mail_form in mail_form_ids:
            val['email_from'].append(mail_form.from_mail_id)
            for line in mail_form.line_ids:
                if line.to_address:
                    val['email_to'].append(line.email)
                if line.cc_address:
                    val['email_cc'].append(line.email)
                if line.bcc_address:
                    val['email_bcc'].append(line.email)
        
        return val
    
    def mail_config_mailids_data(self, **kw):
        """Getting Mail Id's from mail configuration: mail_type, model_name, mail_name key value is a must"""

        mail_type = kw.get('mail_type', '')
        model_name = kw.get('model_name', False)
        mail_name = kw.get('mail_name', '')

        val = {
            'email_from': [],
            'email_to': [],
            'email_cc': [],
            'email_bcc': [],
        }

        if mail_type and mail_name:
            domain = [('active', '=', True), ('status', '=', 'active'), ('name', '=', mail_name)]
            if mail_type == 'transaction' and model_name:
                domain.append(('model_name', '=', model_name))
            
            mail_form_ids = self.env[CP_MAIL_CONFIGURATION].search(domain)
            
            val = self.process_mail_forms(mail_form_ids, val)

        return val

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

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CpMailConfiguration, self).write(vals)

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
        cm_master = self.env[CP_MAIL_CONFIGURATION]
        result['all_draft'] = cm_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_master.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result