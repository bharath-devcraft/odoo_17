# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf,is_mobile_num,is_valid_mail
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import uuid
import werkzeug

_logger = logging.getLogger(__name__)

CM_SURVEY = 'cm.survey'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmSurvey(models.Model):
    _name = 'cm.survey'
    _description = 'Base custom survey'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'crt_date desc'

    def _get_default_access_token(self):
        return str(uuid.uuid4())

    name = fields.Char(string="Name", index=True, copy=False)
    purpose = fields.Char(string="Purpose", copy=False, side=252)
    from_date = fields.Date(string="From Date", default=fields.Date.today)
    to_date = fields.Date(string="To Date")
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                              copy=False, default='draft')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
    note = fields.Html(string="Note", copy=False)
    access_token = fields.Char('Access Token', default=lambda self: self._get_default_access_token(), copy=False)
    survey_start_url = fields.Char('Survey URL', compute='_compute_survey_start_url', store=True)

    #Entry info
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
    update_date = fields.Datetime(string="Last Update Date", readonly=True, copy=False)
    update_user_id = fields.Many2one(RES_USERS, string="Last Update By", readonly=True, copy=False,
                                    ondelete='restrict')
    close_date = fields.Datetime(string='Close Date', readonly=True, copy=False)

    #Line Ref
    line_ids = fields.One2many('cm.survey.line', 'header_id', string='Survey Line', copy=True)
   
    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_('Special character is not allowed in name field'))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_survey where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s""" %(name, self.id))
            if self.env.cr.fetchone():
                raise UserError(_('Survey name must be unique'))
        return True

    def validations(self):
        """ validations """
        warning_msg = []

        if self.status in ('draft', 'editable'):
            res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.rule_checker_master')
            is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
            if res_config_rule and self.user_id == self.env.user and not(is_mgmt):
                warning_msg.append("Created user is not allow to approve the entry")
        if self.from_date and self.from_date < fields.Date.today():
                warning_msg.append("From date should not be lesser than current date")
        if self.from_date and self.to_date and self.to_date < self.from_date:
                warning_msg.append("To date should not be lesser than from date")
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(formatted_messages)
        else:
            return True

    def entry_approve(self):
        """ entry_approve """
        self.validations()
        if self.status in ('draft', 'editable'):
            self.survey_mail_data_design()
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
        return super(CmSurvey, self).create(vals)

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CmSurvey, self).write(vals)
     
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
            'all_closed': 0,
            'my_draft': 0,
            'my_active': 0,
            'my_inactive': 0,
            'my_editable': 0,
            'my_closed': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0,
        }
        
        
        #counts
        cm_master = self.env[CM_SURVEY]
        result['all_draft'] = cm_master.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_master.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_master.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_master.search_count([('status', '=', 'editable')])
        result['all_closed'] = cm_master.search_count([('status', '=', 'closed')])
        result['my_draft'] = cm_master.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_master.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_master.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_master.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_master.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_master.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_master.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_master.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result

    def get_start_url(self):
        return '/custom/survey/start/%s' % self.access_token
    
    @api.depends('access_token')
    def _compute_survey_start_url(self):
        for invite in self:
            if invite.access_token:
                url = werkzeug.urls.url_join(invite.get_base_url(), invite.get_start_url())
                invite.survey_start_url = url
    
    def create_survey(self, **kw):
        """Survey Creation"""

        name = kw.get('name', '')
        purpose = kw.get('purpose', '')
        from_date = kw.get('from_date', '')
        to_date = kw.get('to_date', '')
        if name and purpose and from_date and to_date:

            survey_id = self.create(
                {
                    'name': name,
                    'crt_date': time.strftime(TIME_FORMAT),
                    'purpose': purpose,
                    'from_date': from_date,
                    'to_date': to_date,
                    'status': 'draft'})
            #self.survey_mail_data_design(trans_rec = survey_id)

            return survey_id if survey_id else False
        return False

    def survey_mail_data_design(self, **kw):
        """ survey_mail_data_design """

        data = [[f"""
                <p>Hello,</p>
                <p>Please click the following link to view the details:</p>
                <p><a href="{self.survey_start_url}">Click here</a></p>
                <p>Thank you!</p>
                """]]

        trans_rec = kw.get('trans_rec', self)
        mail_name = kw.get('mail_name', 'Survey')
        mail_config_name = kw.get('mail_config_name', 'Feedback Survey')
        mail_type = kw.get('mail_type', 'transaction')

        #### Subject ###
        subject = kw.get('subject', '#Survey details')
        if trans_rec and data[0][0] and mail_name and subject and mail_config_name:
            default_to = []
            
            ### Mail Configuration ###
            vals = self.env['cp.mail.configuration'].mail_config_mailids_data(mail_type=mail_type,model_name=CM_SURVEY,mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0])
            # ~ if queue_id:
                # ~ queue_id.send_mail(queue_id = queue_id.id)

        return True

    def survey_close(self, **kw):
        """ Once current date crossed to date status change """
        self.search([('to_date', '<', fields.Date.today()),('status', '=', 'active')]).write({'status': 'closed','close_date': fields.Datetime.now()})

        return True
