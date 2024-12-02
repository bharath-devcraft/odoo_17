# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

CM_MASTER = 'cm_division_master'

RES_USERS = 'res.users'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class cm_division_master(models.Model):
    _name = 'cm_division_master'
    _description = 'cm_division_master'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, 
                 help="Maximum 4 char is allowed and will accept upper case only", size = 4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True,
                              tracking=True, copy=False, default='draft')
    inactive_remark = fields.Text(string="Inactive Remark", copy=False)
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
    update_date = fields.Datetime(string="Last Updated Date", readonly=True, copy=False)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", readonly=True, copy=False,
                                    ondelete='restrict')

    #Line Ref
    line_ids = fields.One2many('cm.master.line', 'header_id', string='Master Line', copy=True)
    line_ids_a = fields.One2many('cm.master.attachment.line', 'header_id', string='Attachment', copy=True)
    
    # ~ ####### windows action count #########
    @api.model
    def _needaction_domain_get(self):
        """ Window action menu count"""
        return False

    @api.model
    def _needaction_count(self, domain=None):
        """ Window action menu count"""
        return self.search_count(domain)
    
    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_('Special character is not allowed in name field'))

            name = self.name.upper()
            name = name.replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_master where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s""" %(name, self.id))
            data = self.env.cr.dictfetchall()
            if len(data) > 0:
                raise UserError(_('Master name must be unique'))
        return True

    @api.constrains('short_name')
    def short_name_validation(self):
        """ short_name_validation """
        if self.short_name:
            if is_special_char(self.env, self.short_name):
                raise UserError(_('Special character is not allowed in short name field'))

            short_name = self.short_name.upper()
            short_name = short_name.replace(" ", "")
            self.env.cr.execute(""" select upper(short_name)
            from cm_master where upper(REPLACE(short_name, ' ', ''))  = '%s'
            and id != %s""" %(short_name, self.id))
            data = self.env.cr.dictfetchall()
            print(short_name,data)
            if len(data) > 0:
                raise UserError(_('Master short name must be unique'))
        return True


    #onchange
    @api.onchange('name')
    def onchange_city(self):
        """ name_validation """
        ...
    
    def action_view_master_transaction(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Transaction History',
            'view_mode': 'tree,form',
            'res_model': 'ct.transaction',
            'domain': [('division_id', '=', self.id)]

        }
        return action

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

        if not self.line_ids_a:
            warning_msgs.append("Kindly check & add attachments, If required")

        if warning_msgs:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view.id if view else False
            context = {
                'message': "\n\n".join(warning_msgs),
                'transaction_id': self.id,
                'transaction_model': CM_MASTER,
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

    @validation
    def entry_approve(self):
        """ entry_approve """
        self.validations()
        if self.status in ('draft', 'editable'):
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')
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
                                    'inactive_date': time.strftime('%Y-%m-%d %H:%M:%S')})
                    else:
                        raise UserError(
                            _('Minimum 10 characters are required for Inactive Remark'))
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
        return super(CmMaster, self).create(vals)

    def write(self, vals):
        """ write """
        if 'short_name' in vals:
            short_name = vals['short_name'].upper()
        else:
            short_name = self.short_name.upper()
        vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'update_user_id': self.env.user.id, 'short_name': short_name})
        return super(CmMaster, self).write(vals)
     
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
        cm_master = self.env[CM_MASTER]
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

  
