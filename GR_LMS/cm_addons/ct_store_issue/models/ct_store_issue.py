# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_STORE_ISSUE = 'ct.store.issue'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

MODE_OF_ISSUE = [('direct', 'Direct')]

ISSUE_TYPE=[('material', 'Material'),('service', 'Service')]

class CtStoreIssue(models.Model):
    _name = 'ct.store.issue'
    _description = 'Store Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Issue No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Issue Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    
    issue_type = fields.Selection(selection=ISSUE_TYPE, string = "Issue Type", required=True, default="material")
    mode_of_issue = fields.Selection(selection=MODE_OF_ISSUE, string="Mode Of Issue", default='direct')

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

    line_ids = fields.One2many('ct.store.issue.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.store.issue.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

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
        for serial_line in detail_line.lot_ids:
            serial_qty += serial_line.store_pend_qty
            if serial_line.store_pend_qty <= 0:
                warning_msg.append(f"Product({detail_line.product_id.name}) quantity should be greater than zero in lot/serial no tab {serial_line.serial_no}")
        if detail_line.lot_ids and serial_qty < detail_line.qty:
            warning_msg.append(f"Product({detail_line.description}) sum of serial no quantity lesser than issue quantity")
        if detail_line.product_id.serial_no_req == 'required' and len(detail_line.lot_ids) != detail_line.qty:
            warning_msg.append(f"Product {detail_line.product_id.name} requires {detail_line.qty} serial numbers, but {len(detail_line.lot_ids)} were selected.")

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
            'confirm': 'ct.store.issue.draft',
            'approve': 'ct.store.issue'
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
                        [('code', '=', 'ct.store.issue')], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s, %s, %s, %s, %s, %s) """ ,
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
                
            stock_locations = {rec.name: rec.id for rec in self.env['cm.stock.location'].search([('name', 'in', ['Main Store', 'Sub Store'])])}
            main_store_id = stock_locations.get('Main Store', False)
            sub_store_id = stock_locations.get('Sub Store', False)

            if not main_store_id or not sub_store_id:
                raise UserError("Main Store or Sub Store location not found!")

            stock_move_obj = self.env['ct.stock.move']
            item_issue_obj = self.env['ct.item.wise.issue.line']

            stock_moves = []
            item_issues = []
            
            current_user_id = self.env.user.id
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for line in self.line_ids:
                unit_price = line.lot_ids[0].unit_price if line.lot_ids else 0.0

                stock_moves.append({
                    'name': self.name,
                    'entry_date': self.entry_date,
                    'from_location_id': main_store_id,
                    'to_location_id': sub_store_id,
                    'qty': line.qty,
                    'product_id': line.product_id.id,
                    'uom_id':line.uom_id.id,
                    'description': line.product_id.name,
                    'brand_id': line.brand_id.id,
                    'unit_price': unit_price,
                    'currency_id': self.currency_id.id,
                    'entry_mode': 'auto',
                    'user_id': self.user_id.id,
                    'ap_rej_user_id': current_user_id,
                    'ap_rej_date': current_date,
                    'status': 'approved',
                })

                issue_qty = (
                    line.qty * line.product_id.uom_coff
                    if line.product_id.uom_id.id != line.product_id.uom_po_id.id
                    and line.product_id.uom_coff > 1
                    and line.uom_id.id == line.product_id.uom_po_id.id
                    else line.qty
                )

                remaining_qty = issue_qty
                for lot_line in sorted(line.lot_ids, key=lambda l: l.id):  
                    if remaining_qty <= 0:
                        break

                    move_qty = min(remaining_qty, lot_line.store_pend_qty)  
                    if move_qty > 0:
                        item_issues.append({
                            'header_id': line.id,
                            'issue_line_id': line.id,
                            'product_id': line.product_id.id,
                            'uom_id': line.uom_id.id,
                            'grn_qty': lot_line.store_pend_qty,
                            'issue_qty': move_qty,
                            'price_unit': lot_line.unit_price,
                            'expiry_date': lot_line.expiry_date,
                            'serial_no': lot_line.serial_no.strip() if lot_line.serial_no else False,
                            'lot_id': lot_line.id,
                        })
                        lot_line.store_pend_qty -= move_qty
                        lot_line.po_pend_qty = lot_line.store_pend_qty / line.product_id.uom_coff if lot_line.store_pend_qty > 0 else 0.0
                        remaining_qty -= move_qty

                # if remaining_qty > 0:
                #     raise UserError("Not enough available stock for.")

            if stock_moves:
                stock_move_obj.create(stock_moves)

            if item_issues:
                item_issue_obj.create(item_issues)

            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

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
        return super(CtStoreIssue, self).write(vals)

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

        ct_store_issue = self.env[CT_STORE_ISSUE]
        result['all_draft'] = ct_store_issue.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_store_issue.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_store_issue.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_store_issue.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_store_issue.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_store_issue.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_store_issue.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_store_issue.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_store_issue.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_store_issue.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_store_issue.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_store_issue.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_store_issue.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_store_issue.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
