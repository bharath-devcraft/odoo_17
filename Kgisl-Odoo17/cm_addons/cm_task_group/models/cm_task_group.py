# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

CM_TASK_GROUP = 'cm.task.group'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revised', 'Revised')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmTaskGroup(models.Model):
    _name = 'cm.task.group'
    _description = 'Task Group'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    name = fields.Char(string="Name", readonly=True, index=True, copy=False, size=128)
    short_name = fields.Char(string="Short Name", copy=False, size=4,
                 help="Maximum 4 char is allowed and will accept upper case only")
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                              tracking=True, copy=False, default='draft')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
    note = fields.Html(string="Note", copy=False)
    nature_of_work = fields.Text('Nature of work')
    department_ids = fields.Many2many(
        'res.company',
        string='Responsible Department',
        ondelete='restrict') # temporary
    revise_remark = fields.Text('Revise Remarks', copy=False)
    watcher_mail_id = fields.Char('Watcher Mail ID', size=128)

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
    revised_date = fields.Datetime(string='Revised Date', readonly=True, copy=False)
    revised_user_id = fields.Many2one(RES_USERS, string="Revised By", readonly=True,
                                 copy=False, ondelete='restrict')
    parent_ref = fields.Many2one('cm.task.group', 'Parent Ref', readonly=True)
    revise_version = fields.Integer('Revise Version', readonly=True)

    #Line Ref
    line_ids = fields.One2many('cm.task.group.line', 'header_id', string='Master Line', copy=True)

    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_('Special character is not allowed in name field'))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_task_group where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s""" %(name, self.id))
            if self.env.cr.fetchone():
                raise UserError(_('Task group name must be unique'))
        return True

    @api.constrains('short_name')
    def short_name_validation(self):
        """ short_name_validation """
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_('Special character is not allowed in short name field'))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_task_group where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s""" %(short_name, self.id))
            if self.env.cr.fetchone():
                raise UserError(_('Task group short name must be unique'))
        return True

    def validations(self):
        """ validations """

        warning_msg = []

        if self.status in ('draft'):
            res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.rule_checker_master')
            is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
            if res_config_rule and self.user_id == self.env.user and not(is_mgmt):
                warning_msg.append("Created user is not allow to approve the entry")

        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(formatted_messages)
        else:
            return True

    @validation
    def entry_approve(self):
        """ entry_approve """
        self.validations()
        if self.status in ('draft'):
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True

    def entry_inactive(self):
        """ entry_inactive """
        if self.status != 'active':
            raise UserError(_('Unable to inactive other than active entry'))

        remark = self.inactive_remark.strip() if self.inactive_remark else None

        if not remark:
            raise UserError(_('Inactive remark is required. Please enter the remarks in the Inactive Remark field'))

        if len(remark) < 10:
            raise UserError(_('Minimum 10 characters are required for Inactive Remark'))

        self.write({
            'status': 'inactive',
            'inactive_user_id': self.env.user.id,
            'inactive_date': time.strftime(TIME_FORMAT)
        })

        return True

    def entry_revise(self):
        """ entry_revise """
        if self.status == 'active':
            remark = self.revise_remark.strip() if self.revise_remark else None

            if not remark:
                raise UserError(_('Revise remark is required. Please enter the remarks in the Revise Remark field'))

            if len(remark) < 10:
                raise UserError(_('Minimum 10 characters are required for Revise Remark'))
            
            task_group_id = self.copy({
                'status': 'revised',
                'revise_version': '',
                'line_ids':self.line_ids,
                'user_id': self.env.user.id,
                'crt_date': time.strftime(TIME_FORMAT),
                'revised_date': time.strftime(TIME_FORMAT),
                'parent_ref': self.id,
                'revise_remark': self.revise_remark,
                'revised_user_id': self.env.user.id,
                'entry_mode':'auto'})
            self.write({'status': 'draft',
                        'revise_version': self.revise_version + 1,
                        'revise_remark': '',})
            for line_item in self.line_ids:
                line_item.copy({'header_id':task_group_id.id})

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

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CmTaskGroup, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the task group master views.
        """

        result = {
            'all_draft': 0,
            'all_active': 0,
            'all_inactive': 0,
            'all_revised': 0,
            'my_draft': 0,
            'my_active': 0,
            'my_inactive': 0,
            'my_revised': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0,
        }
        
        
        #counts
        cm_tg = self.env[CM_TASK_GROUP]
        result['all_draft'] = cm_tg.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_tg.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_tg.search_count([('status', '=', 'inactive')])
        result['all_revised'] = cm_tg.search_count([('status', '=', 'revised')])
        result['my_draft'] = cm_tg.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_tg.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_tg.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_revised'] = cm_tg.search_count([('status', '=', 'revised'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_tg.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_tg.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_tg.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_tg.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result