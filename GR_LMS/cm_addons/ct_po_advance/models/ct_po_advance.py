# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_PO_ADVANCE = 'ct.po.advance'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('wfa', 'WFA'),
    ('approved', 'Approved'),
    ('paid', 'Paid'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

ENTRY_TYPE = [('purchase', 'Purchase'), ('service', 'Service'), ('proforma', 'Proforma')]

TAX = [('Inclusive', 'Inclusive'), ('Exclusive', 'Exclusive')]

PAID_THROUGH = [('credit_card', 'Credit Card'), ('accounts', 'Accounts')]

class CtPoAdvance(models.Model):
    _name = 'ct.po.advance'
    _description = 'PO Advance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Advance No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Advance Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    entry_type = fields.Selection(selection=ENTRY_TYPE, string="Source", default='purchase')
    po_id = fields.Many2one('ct.purchase.order', string="PO No", index=True, ondelete='restrict', tracking=True, domain="[('status', '=', 'approved'),('active_trans', '=', True),('bill_type', '!=', 'cash'),('vendor_id', '=', vendor_id),('payment_term_id.category', '=', 'cash')]")
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tax = fields.Selection(selection=TAX, string="Tax")
    additional_charges = fields.Selection(selection=TAX, string="Additional Charges")
    po_value = fields.Float(string="PO Value", digits=(12, 2))
    po_advance = fields.Float(string="PO Advance (%)", digits = (12,2))
    advance_base_amt = fields.Float(string="Advance Base Amount", default=0.0, digits = (12,2))
    eligible_advance = fields.Float(string="Current Advance (%)", digits = (12,2))
    amt_paid = fields.Float(string="Already Paid Advance", default=0.0, digits=(12, 2))
    round_off_amt = fields.Float(string="Round Off(+/-)", digits = (12,2))
    advance_amt = fields.Float(string="Advance Amount(Released)", digits=(12, 2))
    paid_through = fields.Selection(selection=PAID_THROUGH, string="Paid Through", default='accounts')

    adjusted_amt = fields.Float(string="So Far Adjusted", default=0.0, digits=(12, 2))
    balance_amt = fields.Float(string="Balance Amount", compute='compute_bal_amt', store=True, digits = (12,2))
    refund_amount = fields.Float(string="Refund Amount") 
    round_off_remarks = fields.Text(string="Round Off Remarks")
    flag_used = fields.Boolean('Flag Used', default=False)

    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, related='vendor_id.currency_id', store=True, readonly=True)

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

    line_ids = fields.One2many('ct.po.advance.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.po.advance.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

    @api.depends('advance_amt', 'adjusted_amt')
    def compute_bal_amt(self):
        for rec in self:
            rec.balance_amt = rec.advance_amt - (rec.adjusted_amt + rec.refund_amount)

    def common_onchange_function(self):
        self.payment_term_id = False
        self.department_id = False
        self.po_value = 0
        self.po_advance = 0
        self.advance_base_amt = 0.0
        self.eligible_advance = 0
        self.amt_paid = 0
        self.advance_amt = 0
        self.tax = False
        self.additional_charges =False
        self.round_off_amt = 0.0
        self.line_ids = [(5, 0, 0)]

    @api.onchange('vendor_id')
    def onchange_vendor_id(self):
        self.po_id = False
        self.common_onchange_function()

    @api.onchange('po_id')
    def onchange_po_id(self):
        self.common_onchange_function()

    @api.onchange('round_off_amt', 'eligible_advance', 'po_id', 'advance_base_amt')
    def onchange_round_off(self):
        advance_amt = self.advance_base_amt * (self.eligible_advance / 100)
        self.advance_amt = round(advance_amt, 2) + self.round_off_amt

    @api.onchange('po_id', 'additional_charges', 'tax')
    def onchange_advance_base(self):
        if self.tax and self.additional_charges and self.po_id:
            if self.tax == 'Inclusive' and self.additional_charges == 'Inclusive':
                self.advance_base_amt = round(self.po_id.net_amt, 2)
            elif self.tax == 'Inclusive' and self.additional_charges == 'Exclusive':
                self.advance_base_amt = round(self.po_id.net_amt - self.po_id.other_amt, 2)
            elif self.tax == 'Exclusive' and self.additional_charges == 'Inclusive':
                self.advance_base_amt = round(self.po_id.taxable_amt, 2)
            else:
                self.advance_base_amt = round(self.po_id.tot_amt - self.po_id.disc_amt, 2)


    @api.onchange('po_id', 'advance_base_amt')
    def onchange_set_balance_amt(self):
        self.flag_used = False

        if not self.po_id:
            self.po_value = self.eligible_advance = self.po_advance = self.amt_paid = self.advance_amt = 0
            return

        advance = self.env[CT_PO_ADVANCE].search([
            ('po_id', '=', self.po_id.id), 
            ('status', 'in', ('approved', 'paid'))
        ])

        domain = [('po_id', '=', self.po_id.id), ('status', 'not in', ('rejected', 'cancelled'))]
        if self._origin.id:
            domain.append(('id', '!=', self._origin.id))

        po_rec = self.env[CT_PO_ADVANCE].search(domain)

        for record in po_rec:
            if record.status in ('approved', 'paid'):
                self.flag_used = True
                self.tax = record.tax
                self.additional_charges = record.additional_charges
            else:
                raise UserError("PO Advance already exists for the selected PO")

        eligible_adv = sum(line.eligible_advance for line in advance)
        amount = sum(line.advance_amt for line in advance)

        self.po_advance = self.po_id.payment_term_id.cash_per or 0
        self.payment_term_id = self.po_id.payment_term_id.id
        self.po_value = self.po_id.net_amt
        self.department_id = self.po_id.department_id.id
        self.eligible_advance = round(self.po_advance - eligible_adv, 2)
        self.amt_paid = amount

        self.line_ids = self.load_advance()


    def load_advance(self):
        self.line_ids = [(5,0,0,)]
        old_advance_vals = []
        advance = self.env[CT_PO_ADVANCE].search([('po_id', '=', self.po_id.id)])
        for adv in advance:
            if (adv.id != self.id) and (adv.status in ('approved','paid','cancelled')):
                old_advance_vals.append([0, 0, {
                    'advance_id': adv.id,
                    'advance_date': adv.entry_date,
                    'ref_no': adv.po_id.name,
                    'advance_amt': adv.advance_amt,
                    'status': adv.status
                }])

        return old_advance_vals

    @api.constrains('eligible_advance')
    def check_value(self):
        if not (1 <= self.eligible_advance <= 100):
            raise UserError(_("Current Advance (%) should be greater than 0 and less than or equal to 100."))

    @api.constrains('round_off_remarks','round_off_amt')
    def check_round_off_remarks(self):
        if self.round_off_remarks:
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if self.round_off_remarks and len(self.round_off_remarks.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for round off remarks"))

        if self.round_off_amt >20:
           raise UserError(_("Round off amount should not be greater than Rs.20"))

        if self.round_off_amt != 0 and not self.round_off_remarks:
            raise UserError(_("Round off remarks is must. Kindly enter the remarks in round off remarks field"))

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


    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            if not (1 <= self.eligible_advance <= 100):
                warning_msg.append("Current Advance value should be greater than 0 and less than or equal to 100.")

            advance = self.env[CT_PO_ADVANCE].search([
                ('po_id', '=', self.po_id.id), 
                ('id', '!=', self.id),
                ('status', 'in', ('approved', 'paid'))
            ])
            
            eligible_adv = sum(advance.mapped('advance_amt'))
            total_eligible_amt = round(self.po_value * (self.po_advance / 100), 2) + 5
            
            if round(self.advance_amt + eligible_adv, 2) > total_eligible_amt:
                warning_msg.append("Current advance (%) cannot exceed PO advance (%)")

        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'approve': CT_PO_ADVANCE
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
                        [('code', '=', CT_PO_ADVANCE)], limit=1)
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
        return super(CtPoAdvance, self).write(vals)

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

        ct_nocost_trans = self.env[CT_PO_ADVANCE]
        result['all_draft'] = ct_nocost_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_nocost_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_nocost_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_nocost_trans.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_nocost_trans.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_nocost_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_nocost_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_nocost_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_nocost_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_nocost_trans.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_nocost_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_nocost_trans.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_nocost_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_nocost_trans.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
