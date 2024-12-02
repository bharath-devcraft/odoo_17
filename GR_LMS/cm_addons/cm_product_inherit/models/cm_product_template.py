# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

PRODUCT_TEMPLATE = 'product.template'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

APPLICABLE_OPTION = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]

FLEXI_TYPE = [('tltd', 'TLTD'), ('tlbd', 'TLBD'), ('blbd', 'BLBD')]


LAYER_TYPE = [('3_layer', '3+1 Layer'), ('4_layer', '4+1 Layer'), ('5_layer', '5+1 Layer')]

CUSTOM_TYPE = [('flexi_bag', 'Flexi Bag'), ('flexi_accessories', 'Flexi Accessories'), ('consumables', 'Consumables'), ('asset', 'Asset')]

CAPACITY = [('16kl', '16KL'), ('18kl', '18KL'), ('20kl', '20KL'), ('22kl', '22KL'), ('24kl', '24KL')]

VALVE_TYPE = [('3_butterfly', 'Butterfly'), ('3_ball_valve', 'Ball valve'), ('both', 'Both')]

BAG_COSTING_METHOD = [('with_accessories', 'With Accessories'), ('without_accessories', 'Without Accessories')]

PAD_TYPE = [('with_heating_pad', 'With Heating Pad'), ('without_heating_pad', 'Without Heating Pad')]

MOC = [('pp', 'PP(Polypropylene)'), ('pe', 'PE(Polyethylene)')]

S_NO = [('required', 'Required'), ('not_required', 'Not Required')]

class CmProductTemplate(models.Model):
    _name = 'product.template'
    _description = 'Record'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin','product.template']
    _order = 'name asc'


    short_name = fields.Char(string="Short Name", copy=False, help="Maximum 4 char is allowed and will accept upper case only", size=4)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    custom_type = fields.Selection(selection=CUSTOM_TYPE, string="Type")
    flexi_type = fields.Selection(selection=FLEXI_TYPE, string="Flexi Type", copy=False, help='TLTD (Top Loading Top Discharge),TLBD (Top Loading Bottom Discharge),BLBD (Bottom Load Bottom Discharge)')
    layer_type = fields.Selection(selection=LAYER_TYPE, string="Layer Type", copy=False, default='3_layer')
    capacity = fields.Selection(selection=CAPACITY, string="Capacity(L)", copy=False)
    valve_size = fields.Char(string="Valve Size(Inch)", copy=False, size=50)
    valve_type = fields.Selection(selection=VALVE_TYPE, string="Valve Type", copy=False)
    halal_certification = fields.Selection(selection=APPLICABLE_OPTION, string="Halal Certification", copy=False)
    warranty = fields.Selection(selection=APPLICABLE_OPTION, string="Warranty", copy=False, tracking=True)
    warranty_period = fields.Integer(string="Warranty Periods(Months)", copy=False, default = 18)
    mfg_lead_time = fields.Integer(string="Manufacturing Lead Time(Days)", copy=False)
    bag_costing_method = fields.Selection(selection=BAG_COSTING_METHOD, string="Bag Costing Method", copy=False)
    pad_type = fields.Selection(selection=PAD_TYPE, string="Pad Type", copy=False)
    serial_no_req = fields.Selection(selection=S_NO, string="Serial No", copy=False)
    
    moc_id = fields.Many2one('cm.moc', string="Material of Construction(MOC)", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    weight = fields.Float(string="Weight(Kg)", copy=False)
    uom_coff = fields.Float(string="UOM Coff", copy=False)
    thickness = fields.Char(string="Thickness", copy=False, size=252)
    hs_id = fields.Many2one('cm.hsn.code', string="HSN/SAC Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bus_vert_id = fields.Many2one('cm.business.vertical', string="Business Vertical", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    bus_vert_sub_type_id = fields.Many2one('cm.business.vertical.sub.type', string="Business Vertical Sub Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    dg_product = fields.Selection(selection=YES_OR_NO, string="Dangerous Goods" ,copy=False, default="no")
    dry_box_type = fields.Char(string="Dry Box Type", default="20 Feet Heavy Duty", copy=False, size=252)

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

    line_ids = fields.One2many('cm.product.template.line', 'header_id', string="Accessories Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.product.template.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    # @api.constrains('name')
    # def name_validation(self):
    #     if self.name:
    #         if is_special_char(self.env, self.name):
    #             raise UserError(_("Special character is not allowed in name field"))

    #         name = self.name.upper().replace(" ", "")
    #         self.env.cr.execute(""" select upper(name)
    #         from product_template where upper(REPLACE(name, ' ', ''))  = '%s'
    #         and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
    #         if self.env.cr.fetchone():
    #             raise UserError(_("Flexi bag name must be unique"))

    # @api.constrains('short_name')
    # def short_name_validation(self):
    #     if self.short_name:
    #         if is_special_char(self.env, self.short_name):
    #             raise UserError(_("Special character is not allowed in short name field"))

    #         short_name = self.short_name.upper().replace(" ", "")
    #         self.env.cr.execute(""" select upper(short_name)
    #         from product_template where upper(REPLACE(short_name, ' ', ''))  = '%s'
    #         and id != %s and company_id = %s""" %(short_name, self.id, self.company_id.id))
    #         if self.env.cr.fetchone():
    #             raise UserError(_("Flexi bag short name must be unique"))

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
        return super(CmProductTemplate, self).write(vals)
     
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
        
        product_template = self.env[PRODUCT_TEMPLATE]
        result['all_draft'] = product_template.search_count([('status', '=', 'draft'), ('custom_type', '=', 'flexi_bag')])
        result['all_active'] = product_template.search_count([('status', '=', 'active'), ('custom_type', '=', 'flexi_bag')])
        result['all_inactive'] = product_template.search_count([('status', '=', 'inactive'), ('custom_type', '=', 'flexi_bag')])
        result['all_editable'] = product_template.search_count([('status', '=', 'editable'), ('custom_type', '=', 'flexi_bag')])
        result['my_draft'] = product_template.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('custom_type', '=', 'flexi_bag')])
        result['my_active'] = product_template.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('custom_type', '=', 'flexi_bag')])
        result['my_inactive'] = product_template.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('custom_type', '=', 'flexi_bag')])
        result['my_editable'] = product_template.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('custom_type', '=', 'flexi_bag')])
              
        result['all_today_count'] = product_template.search_count([('crt_date', '>=', fields.Date.today()), ('custom_type', '=', 'flexi_bag')])
        result['all_month_count'] = product_template.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('custom_type', '=', 'flexi_bag')])
        result['my_today_count'] = product_template.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('custom_type', '=', 'flexi_bag')])
        result['my_month_count'] = product_template.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('custom_type', '=', 'flexi_bag')])

        return result
    
    @api.model
    def retrieve_acc_dashboard(self):
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
        
        product_template = self.env[PRODUCT_TEMPLATE]
        result['all_draft'] = product_template.search_count([('status', '=', 'draft'),('custom_type', '=', 'flexi_accessories')])
        result['all_active'] = product_template.search_count([('status', '=', 'active'),('custom_type', '=', 'flexi_accessories')])
        result['all_inactive'] = product_template.search_count([('status', '=', 'inactive'),('custom_type', '=', 'flexi_accessories')])
        result['all_editable'] = product_template.search_count([('status', '=', 'editable'),('custom_type', '=', 'flexi_accessories')])
        result['my_draft'] = product_template.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('custom_type', '=', 'flexi_accessories')])
        result['my_active'] = product_template.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('custom_type', '=', 'flexi_accessories')])
        result['my_inactive'] = product_template.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('custom_type', '=', 'flexi_accessories')])
        result['my_editable'] = product_template.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('custom_type', '=', 'flexi_accessories')])
              
        result['all_today_count'] = product_template.search_count([('crt_date', '>=', fields.Date.today()),('custom_type', '=', 'flexi_accessories')])
        result['all_month_count'] = product_template.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('custom_type', '=', 'flexi_accessories')])
        result['my_today_count'] = product_template.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('custom_type', '=', 'flexi_accessories')])
        result['my_month_count'] = product_template.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('custom_type', '=', 'flexi_accessories')])

        return result
    
    @api.model
    def retrieve_gen_dashboard(self):
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
        
        product_template = self.env[PRODUCT_TEMPLATE]
        result['all_draft'] = product_template.search_count([('status', '=', 'draft'),('custom_type', '=', 'consumables')])
        result['all_active'] = product_template.search_count([('status', '=', 'active'),('custom_type', '=', 'consumables')])
        result['all_inactive'] = product_template.search_count([('status', '=', 'inactive'),('custom_type', '=', 'consumables')])
        result['all_editable'] = product_template.search_count([('status', '=', 'editable'),('custom_type', '=', 'consumables')])
        result['my_draft'] = product_template.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid),('custom_type', '=', 'consumables')])
        result['my_active'] = product_template.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid),('custom_type', '=', 'consumables')])
        result['my_inactive'] = product_template.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid),('custom_type', '=', 'consumables')])
        result['my_editable'] = product_template.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid),('custom_type', '=', 'consumables')])
              
        result['all_today_count'] = product_template.search_count([('crt_date', '>=', fields.Date.today()),('custom_type', '=', 'consumables')])
        result['all_month_count'] = product_template.search_count([('crt_date', '>=', datetime.today().replace(day=1)),('custom_type', '=', 'consumables')])
        result['my_today_count'] = product_template.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()),('custom_type', '=', 'consumables')])
        result['my_month_count'] = product_template.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)),('custom_type', '=', 'consumables')])

        return result
