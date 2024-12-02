# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_DEPOT_TARIFF = 'cm.depot.tariff'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
CM_CITY = 'cm.city'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('revised', 'Revised'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

TANK_T_CODE = [('t1','T1'),('t2','T2'),('t3','T3'),('t4','T4'),('t5','T5'),('t6','T6'),('t7','T7'),('t8','T8'),('t9','T9'),('t10','T10'),
               ('t11', 'T11'),('t12', 'T12'),('t13', 'T13'),('t14', 'T14'),('t15', 'T16'),('t17', 'T17'),('t18', 'T18'),('t19', 'T19'),('t20', 'T20'),
               ('t21', 'T21'),('t22', 'T22'),('t23', 'T23'),('t50', 'T50'),('t75', 'T75')]

SUB_TYPE2 = [('swap_body','Swap Body'),
            ('baffle', 'Baffle'),
            ('foodgrade', 'Foodgrade'),
            ('industrial', 'Industrial')]

PACKAGE_DEAL = [('applicable', 'Applicable'),
                   ('not_applicable', 'Not Applicable')]

class CmDepotTariff(models.Model):
    _name = 'cm.depot.tariff'
    _description = 'Depot Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Html(string="Remarks", copy=False, sanitize=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    eff_from_date = fields.Date(string="Effective From Date")

    depot_id = fields.Many2one('cm.depot.location', string="Depot Location Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    depot_vendor_id = fields.Many2one('cm.depot.vendor.master', string="Deport Vendor Name", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    city_id = fields.Many2one(CM_CITY, string="City", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict')
    tank_t_code = fields.Selection(selection=TANK_T_CODE, string="Tank T Code")
    sub_type2 = fields.Selection(selection=SUB_TYPE2, string="Sub Type2")
    clean_cate_id = fields.Many2one('cm.cleaning.category', string="Cleaning Category", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # package_deal_ref_id = fields.Many2one('cm.master', string="Package Deal Ref", domain=[('status', '=', 'active'),('active_trans', '=', True)])
    package_deal = fields.Selection(selection=PACKAGE_DEAL, string="Package Deal")
    rental_per_day = fields.Float(string="Rental Per Day")

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

    line_ids = fields.One2many('cm.depot.tariff.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.depot.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.depot.tariff.storage.fee.details.line', 'header_id', string="Storage Fee Details", copy=True, c_rule=True) 

    
    @api.constrains('depot_id','depot_vendor_id','tank_t_code','sub_type2','clean_cate_id','package_deal')
    def depot_id_validation(self):
        if self.depot_id:
            self.env.cr.execute(""" select id
            from cm_depot_tariff where depot_id  = %s and depot_vendor_id  = %s
            and tank_t_code  = '%s' and sub_type2  = '%s' and clean_cate_id  = %s and package_deal  = '%s'
            and id != %s and company_id = %s and status != 'inactive' """ %(self.depot_id.id,
            self.depot_vendor_id.id, self.tank_t_code, self.sub_type2,self.clean_cate_id.id,self.package_deal, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Depot location name must be unique"))

    @api.onchange('depot_vendor_id')
    def onchange_depot_vendor_id(self):
        if self.depot_vendor_id:
            self.city_id = self.depot_vendor_id.city_id
            self.state_id = self.depot_vendor_id.state_id
            self.country_id = self.depot_vendor_id.country_id
        else:
            self.city_id = False
            self.state_id = False
            self.country_id = False
    
    @api.onchange('depot_id')
    def onchange_depot_id(self):
        if self.depot_id:
            self.name = self.depot_id.name
            self.package_deal = self.depot_id.package_deal
        else:
            self.name = False
            self.package_deal = False

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
        return super(CmDepotTariff, self).write(vals)
     
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
        
        cm_depot_tariff = self.env[CM_DEPOT_TARIFF]
        result['all_draft'] = cm_depot_tariff.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_depot_tariff.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_depot_tariff.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_depot_tariff.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_depot_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_depot_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_depot_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_depot_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_depot_tariff.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_depot_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_depot_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_depot_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
