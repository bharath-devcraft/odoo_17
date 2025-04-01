# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_GATE_PASS = 'ct.gate.pass'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('ack', 'WFA Security'),
    ('approved', 'Open'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

GP_TYPE = [('direct', 'Direct')]
YES_OR_NO = [('yes', 'Yes'), ('no', 'No')]

class CtGatePass(models.Model):
    _name = 'ct.gate.pass'
    _description = 'Gate Pass'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="GP No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="GP Date", copy=False, default=fields.Date.today)
    address = fields.Char(string="Address", size=252)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    gp_type = fields.Selection(selection=GP_TYPE, string="GP Type", required=True, default='direct')
    transport = fields.Char(string="Transport", size=128)
    exp_return_date = fields.Date(string="Expected Return Date")
    task_manager = fields.Many2one('res.users', string="Task Manager", ondelete='restrict')
    taken_by = fields.Char(string="Taken By", size = 128)
    outward_type = fields.Char(string="Outward Type", size = 128)
    received_by = fields.Char(string="Received By/Store", size=128)
    security_remark = fields.Text(string="Security Remarks")
    dc_no = fields.Char(string="Invoice / DC No")
    dc_date = fields.Date(string="Invoice / DC Date")
    returnable = fields.Selection(selection=YES_OR_NO, sting="Returnable", required=True, default='yes')
    out_date = fields.Date(string="Out Date")
    security_name = fields.Char(string="Security Name", size=128)
    reference = fields.Char(string="Reference", size=128)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    ack_user_id = fields.Many2one(RES_USERS, string="Ack By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    ack_date = fields.Datetime(string="Ack Date", copy=False, readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids = fields.One2many('ct.gate.pass.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.gate.pass.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False


    def validate_approve_action(self, warning_msg):
        is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
        if not is_mgmt:
            res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.rule_checker_transaction')
            if res_config_rule and self.confirm_user_id == self.env.user:
                warning_msg.append("Confirmed user is not allow to approve the entry")

    def validate_serial_lines(self, detail_line, warning_msg, dub_serial):
        serial_qty = 0
        for serial_line in detail_line.line_ids:
            serial_qty += serial_line.qty
            if serial_line.qty <= 0:
                warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero in serial no tab {serial_line.serial_no_id.serial_no}")
            if serial_line.serial_no_id.serial_no in dub_serial:
                warning_msg.append(f"{serial_line.serial_no_id.serial_no} duplicate serial no not allowed for product({detail_line.description})")
            dub_serial.append(serial_line.serial_no_id.serial_no)
        if detail_line.line_ids and serial_qty != detail_line.qty:
            warning_msg.append(f"Product({detail_line.description}) sum of serial no quantity should be equal to product quantity")


    def validate_line_items(self, warning_msg):
        if not self.line_ids:
            warning_msg.append("System not allow to confirm/approve with empty line details")
        else:
            dub_product = set()
            dub_serial = []
            for detail_line in self.line_ids:
                if detail_line.qty <= 0:
                    warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero")
                combination = (
                    detail_line.product_id.id, 
                    detail_line.uom_id.id, 
                    detail_line.brand_id.id if detail_line.brand_id else None
                )
                if combination in dub_product:
                    warning_msg.append(f"Duplicate product are not allowed. Ref : {detail_line.description}")
                if  detail_line.product_id.serial_no_req =='required' and  not detail_line.line_ids:
                    warning_msg.append(f"Serial required for the mentioned product. Ref : {detail_line.description}")
                
                else:
                    dub_product.add(combination)
                self.validate_serial_lines(detail_line, warning_msg, dub_serial)


    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            self.validate_line_items(warning_msg)
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.gate.pass.draft',
            'approve': CT_GATE_PASS
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
    
    @api.depends('line_ids')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)

    @api.onchange('vendor_id')
    def vendor_id_onchange(self):
        self.address = ", ".join(filter(None, [
                self.vendor_id.street,
                self.vendor_id.street1,
                self.vendor_id.city_id.name,
                self.vendor_id.state_id.name,
                self.vendor_id.country_id.name
            ]))


    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()
            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_GATE_PASS)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """ ,
                        (sequence_id.id,
                         sequence_id.code,
                         self.entry_date,
                         None,
                         None,
                         ''))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.entry_date, action='approve')

                self.name = sequence
            
            self.write({'status': 'ack',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

        return True

    @validation
    def entry_ack(self):
        if self.status == 'ack':
            if self.out_date:
                if self.out_date < self.entry_date:
                    raise UserError('Out date should not be lesser than gate pass date')
            else:
                raise UserError(('Please give out date for security acknowledgement !!!'))
            
            if not self.reference:
                raise UserError(('Please give reference for security acknowledgement !!!'))
            
            if not self.security_name:
                raise UserError(('Please give security name for security acknowledgement !!!'))
                
            self.write(
                {'status':'approved',
                 'ack_user_id': self.env.user.id,
                 'ack_date': time.strftime('%Y-%m-%d %H:%M:%S')
                 })
    
    def entry_reject(self):
        if self.status == 'wfa':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.ap_rej_remark or not self.ap_rej_remark.strip():
                raise UserError(_("Reject remarks is must. Kindly enter the remarks in Approve / Reject Remarks field"))
            if self.ap_rej_remark and len(self.ap_rej_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for Approve / Reject Remarks"))
            self.write({'status': 'rejected',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def entry_cancel(self):
        if self.status == 'ack':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.cancel_remark or not self.cancel_remark.strip():
                raise UserError(_("Cancel remarks is must. Kindly enter the remarks in Cancel Remarks field"))
            if self.cancel_remark and len(self.cancel_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for cancel remarks"))
            self.write({'status': 'cancelled',
                        'cancel_user_id': self.env.user.id,
                        'cancel_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def unlink(self):
        for rec in self:
            if rec.status != 'draft' or rec.entry_mode == 'auto':
                raise UserError(_("You can't delete other than manually created draft entries"))
            if rec.status == 'draft':
                is_mgmt = self.env[RES_USERS].has_group('cm_user_mgmt.group_mgmt_admin')
                if not is_mgmt:
                    res_config_rule = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.del_self_draft_entry')
                    if not res_config_rule and self.user_id != self.env.user and not(is_mgmt):
                        raise UserError(_("You can't delete other users draft entries"))
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CtGatePass, self).write(vals)

    @api.model
    def retrieve_dashboard(self):
        result = {
            'all_draft': 0,
            'all_wfa': 0,
            'all_approved': 0,
            'all_rejected': 0,
            'all_cancelled': 0,
            'my_draft': 0,
            'my_wfa': 0,
            'my_approved': 0,
            'my_rejected': 0,
            'my_cancelled': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0
        }

        ct_gate_pass = self.env[CT_GATE_PASS]
        result['all_draft'] = ct_gate_pass.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_gate_pass.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_gate_pass.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_gate_pass.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_gate_pass.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_gate_pass.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_gate_pass.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_gate_pass.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_gate_pass.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_gate_pass.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_gate_pass.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_gate_pass.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_gate_pass.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_gate_pass.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
