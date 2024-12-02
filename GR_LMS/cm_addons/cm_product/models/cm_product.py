# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_PRODUCT = 'cm.product'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('restricted', 'Restricted'),
        ('spl_req', 'Special Requirement'),
        ('inactive', 'Inactive'),]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

ACCEPTABILITY = [('acceptable','Acceptable'),('not_acceptable', 'Not Acceptable')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

TANK_T_CODE = [('t1','T1'),('t2','T2'),('t3','T3'),('t4','T4'),('t5','T5'),('t6','T6'),('t7','T7'),('t8','T8'),('t9','T9'),('t10','T10'),
               ('t11', 'T11'),('t12', 'T12'),('t13', 'T13'),('t14', 'T14'),('t15', 'T16'),('t17', 'T17'),('t18', 'T18'),('t19', 'T19'),('t20', 'T20'),
               ('t21', 'T21'),('t22', 'T22'),('t23', 'T23'),('t50', 'T50'),('t75', 'T75')]

class CmProduct(models.Model):
    _name = 'cm.product'
    _description = 'Product'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    che_name = fields.Char(string="Chemical Name", index=True, copy=False)
    ship_name = fields.Char(string="Proper Shipping Name", index=True, copy=False)
    hs_id = fields.Many2one('cm.hsn.code', string="HSN/SAC Code", copy=False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bus_vert_id = fields.Many2one('cm.business.vertical', string="Business Vertical", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bus_vert_sub_type_id = fields.Many2one('cm.business.vertical.sub.type', string="Business Vertical Sub type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    gra_den = fields.Char(string="Specific Gravity/Density", copy=False)
    acceptability = status = fields.Selection(selection=ACCEPTABILITY, string="Acceptability")
    spl_req = fields.Char(string="Special Requirements", copy=False)
    dg_product = fields.Selection(selection=YES_OR_NO, string="Dangerous Goods")
    un_no = fields.Char( string="UN Number", copy=False)
    imo_class = fields.Char(string="IMO Class (Range 1 - 9)", size=10)
    sub_class1 = fields.Char(string="Sub Class I", size=10)
    sub_class2 = fields.Char(string="Sub Class II", size=10)
    psa_class = fields.Char(string="PSA Class")
    lpk_class = fields.Char(string="LPK Class")
    ems_class = fields.Char(string="EMS Code")
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")
    mar_poll = fields.Selection(selection=YES_OR_NO, string="Marine Pollutant")
    # tank_id = fields.Many2one('cm.tank.master', string="Suitable Tank Type", copy=False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tank_t_code = fields.Selection(selection=TANK_T_CODE, string="Tank T Code")
    fosfa = fields.Selection(selection=YES_OR_NO, string="FOSFA Approved")
    kosher = fields.Selection(selection=YES_OR_NO, string="Kosher Certified")
    clean_cate_id = fields.Many2one('cm.cleaning.category', string="Cleaning Category", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)


    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", tracking=True, readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    inactive_date = fields.Datetime(string="Inactivated Date", copy=False, readonly=True)
    inactive_user_id = fields.Many2one(RES_USERS, string="Inactivated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)

    line_ids = fields.One2many('cm.product.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_product where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Product / Trade  name must be unique"))

    @api.onchange('dg_product', 'che_name')
    def onchange_dg_product(self):
        if self.dg_product == 'yes' and self.che_name:
            self.ship_name = self.che_name + ' - DG'
        elif self.dg_product != 'yes':
            self.ship_name = self.che_name
            self.un_no = False
            self.imo_class = False
            self.psa_class = False
            self.lpk_class = False
            self.ems_class = False
            self.pack_grp = False
            self.sub_class1 = False
            self.sub_class2 = False
            self.mar_poll = False

    def validations(self):
        warning_msg = []
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(_(formatted_messages))
        
        return True

    @validation
    def entry_approve(self):
        if self.status in ('draft', 'editable'):
            self.validations()
            self.write({'status': 'active',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True

    def entry_draft(self):
        if self.status == 'active':
            if not(self.env[RES_USERS].has_group('custom_properties.group_set_to_draft')):
                raise UserError(_("You can't draft this entry. Draft Admin have the rights"))
            self.write({'status': 'editable'})
        return True

    def entry_inactive(self):
        if self.status != 'active':
            raise UserError(_("Unable to inactive other than active entry"))

        remark = self.inactive_remark.strip() if self.inactive_remark else None

        if not remark:
            raise UserError(_("Inactive remarks is required. Please enter the remarks in the Inactive Remarks field"))
        min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
        if len(remark) < int(min_char):
            raise UserError(_(f"Minimum {min_char} characters are required for Inactive Remarks"))

        self.write({
            'status': 'inactive',
            'inactive_user_id': self.env.user.id,
            'inactive_date': time.strftime(TIME_FORMAT)})
        return True

    def unlink(self):
        for rec in self:
            if rec.status != 'draft' or rec.entry_mode == 'auto':
                raise UserError(_("You can't delete other than manually created draft entries"))
            if rec.status == 'draft':
                is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
                if not is_mgmt:
                    res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.del_self_draft_entry')
                    if not res_config_rule and self.user_id != self.env.user:
                        raise UserError(_("You can't delete other users draft entries"))
                models.Model.unlink(rec)
        return True


    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CmProduct, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
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
        
        cm_product = self.env[CM_PRODUCT]
        result['all_draft'] = cm_product.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_product.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_product.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_product.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_product.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_product.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_product.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_product.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_product.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_product.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_product.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_product.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
