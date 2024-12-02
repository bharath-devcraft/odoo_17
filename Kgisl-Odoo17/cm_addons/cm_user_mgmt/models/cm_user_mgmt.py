# -*- coding: utf-8 -*-
import time
import logging
from odoo.addons.custom_properties.decorators import validation,is_special_char,is_special_char_pre_or_suf
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class CmUserMgmt(models.Model):
    """User"""
    _name = "res.users"
    _inherit = ['res.users','mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _description = "User Managment"

    
    entry_mode = fields.Selection([('auto', 'Auto'), ('manual', 'Manual')],'Entry Mode',readonly=True,default='manual') 
    copy_user_id = fields.Many2one('res.users', 'User', domain=[('status', '=', 'active')])
    user_menu_access = fields.Many2many(
        'ir.ui.menu',
        'ir_ui_menu_user_rel',
        'user_id',
        'menu_id',
        'Access Menu',domain=[('name','!=','')])
    groups_id = fields.Many2many(
        'res.groups',
        'res_groups_users_rel',
        'uid',
        'gid',
        'Groups')       
        
    
    company_user_ids = fields.Many2many(
        'res.company',
        'user_company_mapping',
        'user_id',
        'company_id',
        store=True,
        string='Company')
    division_ids = fields.Many2many(
        'res.company',
        'user_division_mapping',
        'user_id',
        'division_id',
        store=True,
        string='Division')
        
    department_ids = fields.Many2many(
        'res.company',
        'user_department_mapping',
        'user_id',
        'department_id',
        store=True,
        string='Department')
 
    mobile_no = fields.Char('Mobile No', size=21)
    ext_no = fields.Char('Ext No', size=15)    
    digi_sign = fields.Image(string="Digital Signature", max_width=128, max_height=128)    
    division_id = fields.Many2one('res.company', 'User Division')
    department_id = fields.Many2one('res.company', 'User Department')
    fiscal_year_id = fields.Many2one('cm.fiscal.year', 'Fiscal Year')
    
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
    @api.constrains('name','login')
    def name_validation(self):
        """ name_validation """
        if self.login:
            if is_special_char(self.env, self.login):
                raise UserError(_('Special character is not allowed in login field'))
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
    
    
    

    def copy_menus_user_id(self):
        """Copy User"""
        self.env.cr.execute(
            """delete from ir_ui_menu_user_rel where user_id=%d""" %
            self.id)
        self.env.cr.execute(
            """delete from res_groups_users_rel where uid=%d""" %
            self.id)
        self.env.cr.execute(
            """select * from ir_ui_menu_user_rel where user_id=%d""" %
            self.copy_user_id.id)
        data = self.env.cr.dictfetchall()
        for i in data:
            self.env.cr.execute(
                """insert into ir_ui_menu_user_rel values(%s,%s)""" %
                (self.id, i['menu_id']))
        self.env.cr.execute(
            """select * from res_groups_users_rel where uid=%d""" %
            self.copy_user_id.id)
        data1 = self.env.cr.dictfetchall()
        for j in data1:
            self.env.cr.execute(
                """insert into res_groups_users_rel values(%s,%s)""" %
                (j['gid'], self.id))
        return True
        
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
        return super(CmUserMgmt, self).write(vals)
        
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
        cm_user = self.env['res.users']
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
        
    

