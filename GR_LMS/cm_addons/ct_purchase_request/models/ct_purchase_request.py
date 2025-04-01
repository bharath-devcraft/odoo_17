# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_PURCHASE_REQUEST = 'ct.purchase.request'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('part_in', 'Part-Inward'),
    ('closed', 'Closed'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CtPurchaseRequest(models.Model):
    _name = 'ct.purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Request No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False,compute='_compute_header_status', default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Request Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    delivery_date = fields.Date(string="Delivery Date", copy=False, tracking=True)
    requested_id = fields.Many2one(RES_USERS, string="Requested By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict')

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
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids = fields.One2many('ct.purchase.request.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.purchase.request.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    @api.depends('line_ids.status')
    def _compute_header_status(self):
        for request in self:
            if request.status in ('approved','part_in'):
                line_statuses = request.mapped('line_ids.status')
                
                if all(status == 'closed' for status in line_statuses):
                    request.status = 'closed'
                elif any(status == 'part_in' for status in line_statuses):
                    request.status = 'part_in'
                elif any(status == 'closed' for status in line_statuses) and not all(status == 'closed' for status in line_statuses):
                    request.status = 'part_in'


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
                    detail_line.uom_id.id
                )
                if combination in dub_product:
                    warning_msg.append(f"Duplicate product are not allowed. Ref : {detail_line.description}")
                else:
                    dub_product.add(combination)


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
            'approve': CT_PURCHASE_REQUEST
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

    @api.onchange('delivery_date')
    def onchange_delivery(self):
        if self.delivery_date and self.entry_date and self.delivery_date < self.entry_date:
            raise UserError(_("Delivery date should be greater than or equal to entry date"))

    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()           

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })
            self.line_ids.write({'status': 'wfa'})

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_PURCHASE_REQUEST)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
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
            
            for line_item in self.line_ids:
                line_item.pending_qty = line_item.qty
                line_item.po_pending_qty = line_item.qty
				
            
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
            self.line_ids.write({'status': 'approved'})

        return True
    
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
        if self.status == 'approved':
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
        return super(CtPurchaseRequest, self).write(vals)

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

        ct_purchase_request = self.env[CT_PURCHASE_REQUEST]
        result['all_draft'] = ct_purchase_request.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_purchase_request.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_purchase_request.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_purchase_request.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_purchase_request.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_purchase_request.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_purchase_request.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_purchase_request.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_purchase_request.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_purchase_request.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_purchase_request.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_purchase_request.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_purchase_request.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_purchase_request.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
