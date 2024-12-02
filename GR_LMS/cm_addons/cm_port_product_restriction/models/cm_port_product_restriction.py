# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

CM_PORT_PRODUCT_RESTRICTION = 'cm.port.product.restriction'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

RESTRICTED_CATEGORY =  [('tank_operator','Tank Operator'),
                        ('carrier', 'Carrier'),
                        ('port', 'Port'),
                        ('others', 'Others')]

SHIPMENT_TYPE = [('import', 'Import'),
                ('export', 'Export'),
                ('t_s', 'T/S'),
                ('all', 'All')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

class CmPortProductRestriction(models.Model):
    _name = 'cm.port.product.restriction'
    _description = 'Product Restriction'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", readonly=True, index=True, copy=False)
    product_id = fields.Many2one('cm.product', string="Product Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    restricted_category = fields.Selection(selection=RESTRICTED_CATEGORY, string="Restricted Category", copy=False)
    shipment_type = fields.Selection(selection=SHIPMENT_TYPE, string="Shipment Type", copy=False)
    tank_operator_id = fields.Many2one('cm.tank.operator', string="Tank Operator Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)]) 
    carrier_id = fields.Many2one('cm.carrier', string="Carrier Name",copy=False, ondelete='restrict',domain=[('status', '=', 'active'),('active_trans', '=', True)])
    port_id = fields.Many2one('cm.port', string="Port Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    reason = fields.Text(string="Reason", copy=False)
    un_no = fields.Char( string="UN Number", copy=False)
    sub_class1 = fields.Char(string="Sub Class I", size =10)
    sub_class2 = fields.Char(string="Sub Class II", size =10)
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")

    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])

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

    line_ids = fields.One2many('cm.port.product.restriction.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    @api.constrains('restricted_category','product_id','tank_operator_id','carrier_id','port_id')
    def duplicate_validation(self):
        if self.restricted_category and self.product_id:
            self.env.cr.execute(""" select id
            from cm_port_product_restriction where restricted_category = %s
            and product_id  = %s 
            and (tank_operator_id = %s or tank_operator_id is null)
            and (carrier_id = %s or carrier_id is null)
            and (port_id = %s or port_id is null)
            and id != %s and company_id = %s""",(self.restricted_category,self.product_id.id,
                                                self.tank_operator_id.id if self.tank_operator_id else None,
                                                self.carrier_id.id if self.carrier_id else None,
                                                self.port_id.id if self.port_id else None,
                                                self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Duplicate entry are not allowed"))

    @api.onchange('restricted_category')
    def onchange_restricted_category(self):
        self.tank_operator_id = False
        self.carrier_id = False
        self.port_id = False
        self.name = 'Others' if self.restricted_category == 'others' else False

    @api.onchange('tank_operator_id','carrier_id','port_id')
    def onchange_ref_name(self):
        self.name = False
        if self.restricted_category:
            if self.restricted_category == 'tank_operator' and self.tank_operator_id:
                self.name = self.tank_operator_id.name
            elif self.restricted_category == 'carrier' and self.carrier_id:
                self.name = self.carrier_id.name
            elif self.restricted_category == 'port' and self.port_id:
                self.name = self.port_id.name
            elif self.restricted_category == 'others':
                self.name = 'Others'

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.un_no = self.product_id.un_no
            self.sub_class1 = self.product_id.sub_class1
            self.sub_class2 = self.product_id.sub_class2
            self.pack_grp = self.product_id.pack_grp
        else:
            self.un_no = False
            self.sub_class1 = False
            self.sub_class2 = False
            self.pack_grp = False


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
        return super(CmPortProductRestriction, self).write(vals)
     
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
        
        cm_port_pro_rst = self.env[CM_PORT_PRODUCT_RESTRICTION]
        result['all_draft'] = cm_port_pro_rst.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_port_pro_rst.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_port_pro_rst.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_port_pro_rst.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_port_pro_rst.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_port_pro_rst.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_port_pro_rst.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_port_pro_rst.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_port_pro_rst.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_port_pro_rst.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_port_pro_rst.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_port_pro_rst.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
