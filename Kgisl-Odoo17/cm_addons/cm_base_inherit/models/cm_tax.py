# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CmTax(models.Model):
    """User"""
    _name = "account.tax"
    _inherit = ['account.tax','mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _description = "Account Tax"

    
    entry_mode = fields.Selection([('auto', 'Auto'), ('manual', 'Manual')],'Entry Mode',readonly=True,default='manual') 
    

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactvie'),
        ('editable', 'Editable'),], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    
    inactive_remark = fields.Text('Inactive Remark')
    note = fields.Text('Notes', tracking=True)

    #Entry info
    active = fields.Boolean('Visible', default=True)
    active_rpt = fields.Boolean('Visible in Report', default=True)
    active_trans = fields.Boolean('Visible in Transactions', default=True)
    entry_mode = fields.Selection(
        [('auto', 'Auto'), ('manual', 'Manual')],
        'Entry Mode',
        readonly=True,
        default='manual')
    crt_date = fields.Datetime(
        'Creation Date',
        readonly=True,
        default=lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'))
    user_id = fields.Many2one(
        'res.users',
        'Created By',
        readonly=True,
        default=lambda self: self.env.user.id)
    ap_rej_date = fields.Datetime('Approved Date', readonly=True)
    ap_rej_user_id = fields.Many2one(
        'res.users', 'Approved By', readonly=True)
    inactive_date = fields.Datetime('Inactivated Date', readonly=True)
    inactive_user_id = fields.Many2one(
        'res.users', 'Inactivated By', readonly=True)
    update_date = fields.Datetime('Last Updated Date', readonly=True)
    update_user_id = fields.Many2one(
        'res.users', 'Last Updated By', readonly=True)

    
    #constrains
    @api.constrains('name')
    def name_validation(self):
        """ name_validation """

        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_('Special character is not allowed in Display Name field'))            
        return True
    
    
    @validation    
    def entry_approve(self):
        """ entry_approve """
        if self.status in ('draft','editable'):
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
        return True

    def entry_draft(self):
        """ entry_draft """
        self.write({'status': 'editable'})
        return True

    def entry_inactive(self):
        """ entry_inactive """
        if self.status == 'active':
            if self.inactive_remark:
                if self.inactive_remark.strip():
                    if len(self.inactive_remark.strip())>= 10:
                        self.write({'status':'inactive',
                                    'active':False,
                                    'inactive_user_id': self.env.user.id,
                                    'inactive_date': time.strftime('%Y-%m-%d %H:%M:%S')})
                    else:
                        raise UserError(
                            _('Minimum 10 characters are required for Inactive Remarks.'))
            else:
                raise UserError(
                    _('Inactive remark is must !!, Enter the remarks in Inactive Remark field.'))
        else:
            raise UserError(
                    _('Unable to inactive other than active entry.'))

        
    def unlink(self):
        """ Unlink """
        for rec in self:
            if rec.status not in ('draft') or rec.entry_mode == 'auto':
                raise UserError("You can't delete other than manually created draft entries.")
            if rec.status in ('draft'):
                res_config_rule = self.env['ir.config_parameter'].sudo().get_param('custom_properties.del_draft_entry')
                is_mgmt = self.env['res.users'].has_group('cm_user_mgmt.group_mgmt_admin')
                if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                    raise UserError("You can't delete other users draft entries")
                models.Model.unlink(rec)
        return True
    
    def write(self, vals):
        """ write """       
        vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'update_user_id': self.env.user.id})
        return super(CmTax, self).write(vals)
        
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
        cm_user = self.env['account.tax']
        result['all_draft'] = cm_user.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_user.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_user.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_user.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_user.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_user.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_user.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_user.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_user.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_user.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_user.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_user.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result   
        
    

