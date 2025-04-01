# -*- coding: utf-8 -*-
import time
from odoo.addons.custom_properties.decorators import validation
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import Counter

CM_PORT_TARIFF = 'cm.port.tariff'
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

IMPORT_EXPORT =  [('import','Import'),
                  ('export', 'Export'),
                  ('both', 'Both'),
                  ('t_s', 'T/S')]

CARGO_CATEGORY =  [('dg','DG'),
                  ('non_dg', 'Non DG')]

CONTAINER_SIZE =  [('20_feet_tk','20 Feet TK'),
                   ('40_feet_tk','40 Feet TK')]

CONTAINER_CATEGORY =  [('laden','Laden'),
                       ('empty', 'Empty')]

PACK_GRP = [('1', 'I'), ('2', 'II'), ('3', 'III')]

T_S_TYPE =  [('in_bound','In Bound'),
             ('out_bound', 'Out Bound')]

PRICE_OWNER =  [('agent','Agent'),
                ('operator', 'Operator')]

CARRIER_TYPE =  [('feeder','Feeder'),
                 ('agent', 'Agent')]

PORT_CATEGORY = [('sea', 'Sea'), ('icd', 'ICD')]

class CmPortTariff(models.Model):
    _name = 'cm.port.tariff'
    _description = 'Port Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'name asc'

    name = fields.Char(string="Name", index=True)
    eff_from_date = fields.Date(string="Effective From Date")
    port_id = fields.Many2one('cm.port', string="Port Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    terminal_id = fields.Many2one('cm.port.terminal', string="Terminal Name", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', port_id)]")
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    port_category = fields.Selection(selection=PORT_CATEGORY, string="Sea / ICD")
    import_export = fields.Selection(selection=IMPORT_EXPORT, string="Import / Export")
    t_s_type = fields.Selection(selection=T_S_TYPE, string="T/S Type")
    container_category = fields.Selection(selection=CONTAINER_CATEGORY, string="Empty / Laden")
    cargo_category = fields.Selection(selection=CARGO_CATEGORY, string="Product Type")
    port_pro_grp_id = fields.Many2one('cm.port.product.group', string="Port Product Group", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True),('port_id', '=', port_id)]")
    pack_grp = fields.Selection(selection=PACK_GRP, string="Packing Group")
    container_size = fields.Selection(selection=CONTAINER_SIZE, string="Container Size", default='20_feet_tk', c_rule=True)
    carrier_terms_id = fields.Many2one('cm.carrier.terms', string="Carrier Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    carrier_type = fields.Selection(selection=CARRIER_TYPE, string="Carrier Type", default="feeder")
    price_owner = fields.Selection(selection=PRICE_OWNER, string="Price Owner")
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    inactive_remark = fields.Text(string="Inactive Remarks", copy=False)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])


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

    line_ids = fields.One2many('cm.port.tariff.line', 'header_id', string="Charges Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('cm.port.tariff.demurrage.line', 'header_id', string="Demurrage(Port Storage / Ground Rent) Details", copy=True, c_rule=True)
    line_ids_b = fields.One2many('cm.port.tariff.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    @api.depends('line_ids')
    def _compute_all_line(self):
        for rec in self:
            rec.tot_amt =  sum(rec.line_ids.mapped('gr_cost'))

    def duplicate_validation(self):
        if (self.port_id and self.terminal_id and self.port_category and self.import_export
            and self.container_category and self.cargo_category and self.container_size 
            and self.carrier_terms_id and self.carrier_type and self.price_owner):
            self.env.cr.execute(""" select id
            from cm_port_tariff where port_id  = %s and terminal_id = %s
            and port_category = '%s' and import_export = '%s' and container_category = '%s'
            and cargo_category = '%s' and container_size = '%s' and carrier_terms_id = '%s'
            and carrier_type = '%s' and price_owner = '%s'
            and id != %s and company_id = %s""" %(self.port_id.id,self.terminal_id.id,self.port_category,
                                                self.import_export,self.container_category,self.cargo_category,
                                                self.container_size,self.carrier_terms_id.id,self.carrier_type,
                                                self.price_owner,self.id,self.company_id.id))
            if self.env.cr.fetchone():
                raise UserError(_("Duplicate entry are not allowed"))

    @api.onchange('port_id')
    def onchange_port_id(self):
        if self.port_id:
            self.name = self.port_id.name
            self.country_id = self.port_id.country_id.id
            if self.port_id.port_category == 'seaport':
                self.port_category = 'sea'
            elif self.port_id.port_category == 'dry_port':
                self.port_category = 'icd'
            else:
                self.port_category = ''
        else:
            self.name = False
            self.country_id = False
            self.port_category = False

    @api.onchange('cargo_category')
    def onchange_cargo_category(self):
        self.pack_grp = False
        self.port_pro_grp_id = False

    @api.onchange('import_export')
    def onchange_import_export(self):
        self.t_s_type = False

    def validate_demurrage_details_lines(self, warning_msg):
        existing_ranges = []
        for dem_line in self.line_ids_a:
            self.validate_line_values(dem_line, warning_msg)
            if dem_line.minimum_days is not None and dem_line.maximum_days is not None:
                existing_ranges.append((dem_line.minimum_days, dem_line.maximum_days))
        
        self.validate_range_conflict(warning_msg, existing_ranges)

    def validate_line_values(self, line, warning_msg):
        if line.minimum_days and line.minimum_days < 0:
            warning_msg.append("Minimum days should be greater than zero in demurrage details tab")
        if line.maximum_days and line.maximum_days < 0:
            warning_msg.append("Maximum days should be greater than zero in demurrage details tab")
        if line.minimum_days and line.maximum_days and line.maximum_days < line.minimum_days:
            warning_msg.append("Maximum days should be greater than minimum days in demurrage details tab")
        if line.actual_cost and line.actual_cost < 0:
            warning_msg.append("Actual cost should be greater than zero in demurrage details tab")
        if line.gr_cost and line.gr_cost < 0:
            warning_msg.append("GR cost should be greater than zero in demurrage details tab")

    def validate_range_conflict(self, warning_msg, ranges):
        for i, (min_days, max_days) in enumerate(ranges):
            for j, (cmp_min_days, cmp_max_days) in enumerate(ranges):
                if i >= j:
                    continue
                if not (max_days < cmp_min_days or min_days > cmp_max_days):
                    warning_msg.append(
                        f"Range conflict: ({min_days}, {max_days}) overlaps with existing range ({cmp_min_days}, {cmp_max_days}) "
                        f"in demurrage details tab"
                    )

    def validate_terminal_handling_charge_lines(self, warning_msg):
        dub_terminal = []
        for ter_line in self.line_ids:
            if ter_line.actual_cost and ter_line.actual_cost < 0:
                warning_msg.append(f"Charges name({ter_line.charges_id.name}) actual cost should be greater than zero in THC details tab")
            if ter_line.gr_cost and ter_line.gr_cost < 0:
                warning_msg.append(f"Charges name({ter_line.charges_id.name}) gr cost should be greater than zero in THC details tab")
            dub_terminal.append(ter_line.charges_id.name)
        duplicates = [terminal for terminal, count in Counter(dub_terminal).items() if count > 1]
        if duplicates:
            warning_msg.append(f"Duplicate charges name are not allowed. Ref: {(', '.join(duplicates))}")

    def validations(self):
        warning_msg = []
        if not self.line_ids_a:
            warning_msg.append("System not allow to approve with empty demurrage details")
        self.duplicate_validation()
        is_mgmt = self.env[RES_USERS].has_group('custom_properties.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_master')
            if res_config_rule and self.user_id == self.env.user:
                warning_msg.append("Created user is not allow to approve the entry")
        self.validate_terminal_handling_charge_lines(warning_msg)
        self.validate_demurrage_details_lines(warning_msg)
        if warning_msg:
            formatted_messages = "\n".join(dict.fromkeys(warning_msg))
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
        return super(CmPortTariff, self).write(vals)
     
    @api.model
    def retrieve_dashboard(self):
        result = {}
        
        cm_port_tariff = self.env[CM_PORT_TARIFF]
        result['all_draft'] = cm_port_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'agent')])
        result['all_active'] = cm_port_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'agent')])
        result['all_inactive'] = cm_port_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'agent')])
        result['all_editable'] = cm_port_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'agent')])
        result['my_draft'] = cm_port_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_active'] = cm_port_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_inactive'] = cm_port_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
        result['my_editable'] = cm_port_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'agent')])
              
        result['all_today_count'] = cm_port_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
        result['all_month_count'] = cm_port_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])
        result['my_today_count'] = cm_port_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'agent')])
        result['my_month_count'] = cm_port_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'agent')])

        return result
    
    @api.model
    def retrieve_op_dashboard(self):
        result = {}
        
        cm_port_tariff = self.env[CM_PORT_TARIFF]
        result['all_draft'] = cm_port_tariff.search_count([('status', '=', 'draft'), ('price_owner', '=', 'operator')])
        result['all_active'] = cm_port_tariff.search_count([('status', '=', 'active'), ('price_owner', '=', 'operator')])
        result['all_inactive'] = cm_port_tariff.search_count([('status', '=', 'inactive'), ('price_owner', '=', 'operator')])
        result['all_editable'] = cm_port_tariff.search_count([('status', '=', 'editable'), ('price_owner', '=', 'operator')])
        result['my_draft'] = cm_port_tariff.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_active'] = cm_port_tariff.search_count([('status', '=', 'active'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_inactive'] = cm_port_tariff.search_count([('status', '=', 'inactive'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
        result['my_editable'] = cm_port_tariff.search_count([('status', '=', 'editable'), ('user_id', '=', self.env.uid), ('price_owner', '=', 'operator')])
              
        result['all_today_count'] = cm_port_tariff.search_count([('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
        result['all_month_count'] = cm_port_tariff.search_count([('crt_date', '>=', datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])
        result['my_today_count'] = cm_port_tariff.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today()), ('price_owner', '=', 'operator')])
        result['my_month_count'] = cm_port_tariff.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1)), ('price_owner', '=', 'operator')])

        return result
