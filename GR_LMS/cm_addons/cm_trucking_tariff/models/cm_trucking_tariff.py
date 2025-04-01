# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation,is_special_char, valid_pin_code
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

CM_TRUCKING_TARIFF = 'cm.trucking.tariff'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
RES_COMPANY = 'res.company'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
        ('draft', 'Draft'),
        ('editable', 'Editable'),
        ('active', 'Active'),
        ('inactive', 'Inactive')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

CONTAINER_CATEGORY = [('laden','Laden'), ('empty', 'Empty')]

YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

DG_NON_DG = [('yes', 'DG'), ('no', 'Non DG')]

APPLICABLE_OPTION = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]

class CmTruckingTariff(models.Model):
    _name = 'cm.trucking.tariff'
    _description = 'Trucking Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'


    name = fields.Char(string="Name", index=True)
    short_name = fields.Char(string="Reference No", index=True, copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    
    eff_from_date = fields.Date(string="Effective From Date")
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    port_id = fields.Many2one('cm.port', string="Entry / Exit Port", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('country_id', '=', country_id)]")
    address = fields.Char(string="Address", size=252)
    pin_code = fields.Char(string="Zip Code", size=10)
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    actual_cost = fields.Float(string="Actual Cost")
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Container Category")
    dg_product = fields.Selection(selection=DG_NON_DG, string="Product Type" )
    un_no = fields.Char( string="UN Number")
    port_pro_grp_id = fields.Many2one('cm.port.product.group', string="Port Product Group", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    
    valid_from_date = fields.Date(string="Validity From Date")
    valid_to_date = fields.Date(string="Validity To Date")
    validity_period = fields.Integer(string="Validity Period(Months)",default=3)
    del_address = fields.Char(string="Delivery Address", size=252)
    halt_address = fields.Char(string="Halt Address", size=252)
    to_pin_code = fields.Char(string="Zip Code", size=10)
    interim_halt = fields.Selection(selection=APPLICABLE_OPTION, string="Interim Halt")

    active = fields.Boolean(string="Visible in View", default=True)
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

    line_ids = fields.One2many('cm.trucking.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    
    # @api.constrains('name')
    def name_validation(self):
        if self.name:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in name field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from cm_trucking_tariff where upper(REPLACE(name, ' ', ''))  = '%s'
            and id != %s and company_id = %s""" %(name, self.id, self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Trucking Tariff service provider name must be unique"))
            
    @api.constrains('pin_code')
    def pin_code_validation(self):
        if self.pin_code:
            if self.country_id.code == 'IN':
                if not(len(str(self.pin_code)) == 6 and self.pin_code.isdigit() == True):
                    raise UserError(_("Invalid zip code(IN). Please enter the correct 6 digit zip code"))
            else:
                if not valid_pin_code(self.pin_code):
                    raise UserError(_("Invalid zip code. Please enter the correct zip code"))
                if is_special_char(self.env,self.pin_code):
                    raise UserError(_("Special character is not allowed in zip code field"))

    @api.onchange('valid_from_date','validity_period')
    def onchange_valid_from_date(self):
        if self.valid_from_date and self.validity_period:
            self.valid_to_date = self.valid_from_date + relativedelta(months=+self.validity_period)

    def validations(self):
        warning_msg = []
        self.name_validation()
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            raise UserError(_(formatted_messages))
        
        return True
    
    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False
    
    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': CM_TRUCKING_TARIFF
        }

        action = kw.get('action')
        if action in action_code_map:
            sequence_code = action_code_map[action]
            sequence_id = self.env[IR_SEQUENCE].search([('code', '=', sequence_code)], limit=1)
            if not sequence_id:
                warning_msg.append("The ir sequence has not been created.")
        if kw.get('date'):
            self.env.cr.execute(
                """select value from ir_config_parameter 
                where key = 'custom_properties.seq_num_reset' 
                order by id desc limit 1;
            """)
            seq_reset = self.env.cr.fetchone()
            if not seq_reset or not seq_reset[0]:
                warning_msg.append("The sequence number reset option has not been configured in the custom settings.")
            elif seq_reset[0] == 'fiscal_year':
                fiscal_year = self.env['cm.fiscal.year'].search([
                                ('from_date', '<=', kw.get('date')),('to_date', '>=', kw.get('date')),
                                ('status', '=', 'active'),('active', '=', True)])
                if not fiscal_year:
                    warning_msg.append("The fiscal year has not been created.")

        return self.display_warnings(warning_msg, kw)

    @validation
    def entry_approve(self):
        if self.status in ('draft', 'editable'):
            self.validations()

            if not self.short_name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CM_TRUCKING_TARIFF)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
                        (sequence_id.id,
                         sequence_id.code,
                         datetime.now().date(),
                         None,
                         None,
                         ''))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=datetime.now().date(), action='confirm')

                self.short_name = sequence

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
        return super(CmTruckingTariff, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_trucking_tariff = self.env[CM_TRUCKING_TARIFF]
        result['all_draft'] = cm_trucking_tariff.search_count([('status', '=', 'draft')])
        result['all_active'] = cm_trucking_tariff.search_count([('status', '=', 'active')])
        result['all_inactive'] = cm_trucking_tariff.search_count([('status', '=', 'inactive')])
        result['all_editable'] = cm_trucking_tariff.search_count([('status', '=', 'editable')])
        result['my_draft'] = cm_trucking_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_active'] = cm_trucking_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid)])
        result['my_inactive'] = cm_trucking_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid)])
        result['my_editable'] = cm_trucking_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid)])
              
        result['all_today_count'] = cm_trucking_tariff.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = cm_trucking_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = cm_trucking_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = cm_trucking_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
