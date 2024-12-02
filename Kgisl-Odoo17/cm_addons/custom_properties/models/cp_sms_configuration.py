
import time
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import Counter
from dateutil.relativedelta import relativedelta
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf,is_mobile_num,is_valid_mail


_logger = logging.getLogger(__name__)

CP_SMS_CONFIGURATION = 'cp.sms.configuration'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
    ('draft', "Draft"),
    ('editable', 'Editable'),
    ('active', "Active"),
    ('inactive', "Inactive")]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

MESSAGE_TYPE =  [('sms','SMS'),
                 ('whatsapp','WhatsApp')]

class CpSmsConfiguration(models.Model):
    _name = 'cp.sms.configuration'
    _description = 'Custom Sms Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    message_type = fields.Selection(selection=MESSAGE_TYPE, string='Type',)
    name = fields.Char('Purpose', index=True, copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True, copy=False, default='draft')
    interval = fields.Char('Interval')
    inactive_remark = fields.Text('Inactive Remark')
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
    line_ids = fields.One2many('cp.sms.configuration.line', 'header_id', string='Sms Configuration Lines', copy=True)

    ## Validation ##
    def validations(self, **kw):
        """ Validations """
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

    @api.constrains('name')
    def _check_name_constrains(self):
        if self.name:
            self._special_char_check(self.name, 'purpose')

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cp_sms_configuration where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and message_type = '%s' """ %(name, self.id, self.message_type))
            if self.env.cr.fetchone():
                raise UserError(_('Sms config purpose must be unique'))
        return True

    @api.constrains('interval')
    def _check_interval_constrains(self):
        if self.interval:
            self._special_char_check(str(self.interval), 'interval')

    def _special_char_check(self, value, label):
        if is_special_char(self.env,value):
            raise UserError(_('Special character is not allowed in %s field' % (label)))

    @api.constrains('line_ids')
    def _user_mobile_validation(self):
         
        if self.status == 'active' and not self.line_ids:
            raise UserError(_("You cannot delete all the entries; instead, you can inactivate the record."))

        invalid_mobile_numbers = [line.mobile_no for line in self.line_ids if line.mobile_no and is_mobile_num(line.mobile_no)]
        if invalid_mobile_numbers:
            raise UserError(_('Mobile number is not valid, check the given numbers for: {}' .format(', '.join(invalid_mobile_numbers))))

        mobile_nos = [line.mobile_no for line in self.line_ids if line.mobile_no]

        duplicates = [mobile for mobile, count in Counter(mobile_nos).items() if count > 1]

        if duplicates:
            raise UserError(_('Duplicate mobile no is not allowed. Remove duplicates: {}'.format(', '.join(duplicates))))

    @api.onchange('message_type')
    def message_type_onchange(self):
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

    def sms_config_data(self, **kw):
        """Get mobile number(s) from SMS configuration: 
           message_type, action_name are required keys."""

        message_type = kw.get('message_type', '')
        action_name = kw.get('action_name', '')

        val = {'mobile_no': []}

        if message_type in ['sms', 'whatsapp'] and action_name:
            sms_form_ids = self.env[CP_SMS_CONFIGURATION].search(
                [('active', '=', True), ('status', '=', 'active'),
                 ('name', '=', action_name), ('message_type', '=', message_type)]
            )
            val['mobile_no'] = [line.mobile_no for ids in sms_form_ids for line in ids.line_ids]

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
        return super(CpSmsConfiguration, self).write(vals)

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
        cm_master = self.env[CP_SMS_CONFIGURATION]
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