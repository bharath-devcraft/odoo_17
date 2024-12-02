# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

CM_SDS_PRODUCT = 'cm.sds.product'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

class CmSdsProduct(models.Model):
    _name = 'cm.sds.product'
    _description = 'SDS Product'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True, copy=False)
    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    product_id = fields.Many2one('cm.product', string="Product Name", copy=False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Manufacturer Name", copy=False, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    issue_date = fields.Date(string="Issue Date", copy=False)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    valid_to_date = fields.Date(string="Validity End Date", copy=False)
    
    che_name = fields.Char(string="Chemical Name", index=True, copy=False)
    ship_name = fields.Char(string="Proper Shipping Name", index=True, copy=False)
    dg_product = fields.Selection(selection=YES_OR_NO, string="Dangerous Goods")
    un_no = fields.Char( string="UN Number")
    imo_class = fields.Char(string="IMO Class (Range 1 - 9)")
    sub_class1 = fields.Char(string="Sub Class I", size =5)
    sub_class2 = fields.Char(string="Sub Class II", size =5)
    psa_class = fields.Char(string="PSA Class")
    lpk_class = fields.Char(string="LPK Class")
    ems_class = fields.Char(string="EMS Code")
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")
    mar_poll = fields.Selection(selection=YES_OR_NO, string="Marine Pollutant")

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

    line_ids = fields.One2many('cm.sds.product.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_sds_product where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Sds Product name must be unique"))

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.che_name = self.product_id.che_name
            self.ship_name = self.product_id.ship_name
            self.dg_product = self.product_id.dg_product
            self.un_no = self.product_id.un_no
            self.imo_class = self.product_id.imo_class
            self.sub_class1 = self.product_id.sub_class1
            self.sub_class2 = self.product_id.sub_class2
            self.psa_class = self.product_id.psa_class
            self.lpk_class = self.product_id.lpk_class
            self.ems_class = self.product_id.ems_class
            self.pack_grp = self.product_id.pack_grp
            self.mar_poll = self.product_id.mar_poll
        else:
            self.name = False
            self.che_name = False
            self.ship_name = False
            self.dg_product =False
            self.un_no = False
            self.imo_class = False
            self.sub_class1 = False
            self.sub_class2 = False
            self.psa_class = False
            self.lpk_class = False
            self.ems_class = False
            self.pack_grp = False
            self.mar_poll = False

    @api.onchange('issue_date','validity_period')
    def onchange_issue_date(self):
        if self.issue_date and self.validity_period:
            self.valid_to_date = self.issue_date + relativedelta(months=+self.validity_period)
            
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
        return super(CmSdsProduct, self).write(vals)
     
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
        
        cm_sds_product = self.env[CM_SDS_PRODUCT]
        result['all_draft'] = cm_sds_product.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_sds_product.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_sds_product.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_sds_product.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_sds_product.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_sds_product.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_sds_product.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_sds_product.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_sds_product.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_sds_product.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_sds_product.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_sds_product.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
