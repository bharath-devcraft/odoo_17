# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

CM_FISCAL_YEAR = 'cm.fiscal.year'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CmFiscalYear(models.Model):
    _name = 'cm.fiscal.year'
    _description = 'Fiscal Year'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    name = fields.Char(string="Name", index=True, copy=False, 
                help="Maximum 9 char is allowed and will accept upper case only", size = 9)
    short_name = fields.Char(string="Short Name", copy=False, 
                help="Maximum 5 char is allowed and will accept upper case only", size = 5)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                            copy=False, default='draft')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    note = fields.Html(string="Note", copy=False)

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
    
    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env,self.name):
                raise UserError(_('Special character is not allowed in name field'))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_fiscal_year where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s""" %(name, self.id))
            if self.env.cr.fetchone():
                raise UserError(_('Fiscal year name must be unique'))
        return True

    @api.constrains('short_name')
    def short_name_validation(self):
        """ short_name_validation """
        if self.short_name:
            if is_special_char(self.env,self.short_name):
                raise UserError(_('Special character is not allowed in short name field'))

            short_name = self.short_name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_fiscal_year where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s""" %(short_name, self.id))
            if self.env.cr.fetchone():
                raise UserError(_('Fiscal year short name must be unique'))
        return True

    def validations(self):
        """ validations """

        warning_msg = []

        if self.status in ('draft', 'editable'):
            res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.rule_checker_master')
            is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
            if res_config_rule and self.user_id == self.env.user and not(is_mgmt):
                warning_msg.append("Created user is not allow to approve the entry")

            if self.from_date > self.to_date:
                warning_msg.append("From date should not be greater than to date.")

            if self.from_date == self.to_date:
                warning_msg.append("Same date should not allowed.")

            dup_entry = self.search_count([('status', '=', 'active'),
                        '|','|',
                        '&', ('from_date', '<=', self.from_date), ('to_date', '>=', self.from_date),
                        '&', ('from_date', '<=', self.to_date), ('to_date', '>=', self.to_date),
                        '&', ('from_date', '>=', self.from_date), ('to_date', '<=', self.to_date)])

            if dup_entry and dup_entry > 0:
                warning_msg.append("The date range conflicts with an already active record")

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
                'transaction_model': CM_FISCAL_YEAR,
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
        if 'short_name' in vals:
            vals['short_name'] = vals.get('short_name').upper()
        return super(CmFiscalYear, self).create(vals)

    def write(self, vals):
        """ write """
        if 'short_name' in vals:
            short_name = vals['short_name'].upper()
        else:
            short_name = self.short_name.upper()
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id, 'short_name': short_name})
        return super(CmFiscalYear, self).write(vals)
     
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
        cm_fy = self.env[CM_FISCAL_YEAR]
        result['all_draft'] = cm_fy.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_fy.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_fy.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_fy.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_fy.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_fy.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_fy.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_fy.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_fy.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_fy.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_fy.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_fy.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result

  
