# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from odoo.exceptions import UserError

CT_TRANSACTION = 'ct.transaction'
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

PAY_MODE_OPTIONS = [('bank', 'Bank'),
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('neft_rtgs', 'NEFT/RTGS'),
            ('others', 'Others')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CtTransaction(models.Model):
    _name = 'ct.transaction'
    _description = 'Transaction Template'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Doc No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    partner_id = fields.Many2one('res.partner', string="Partner Name", index=True, ondelete='restrict', tracking=True)
    address = fields.Char(string="Address", size=252)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    note = fields.Html(string="Notes", copy=False, sanitize=False)
    draft_name = fields.Char(string="Draft No", copy=False, index=True, readonly=True, size=30)
    draft_date = fields.Date(string="Draft Date", copy=False, default=fields.Date.today)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    division_id = fields.Many2one('cm.master', string="Division", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    department_id = fields.Many2one('cm.master', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    pay_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    delivery_date = fields.Date(string="Delivery Date", copy=False, tracking=True)

    active = fields.Boolean(string="Visible", default=True)
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
    trigger_del = fields.Boolean(string="Trigger Delete", default=False)

    tax_amt = fields.Float(string="Tax Amount(+)", store=True, compute='_compute_all_line')	
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')	
    other_amt = fields.Float(string="Other Charges(+)", store=True, compute='_compute_all_line')
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    taxable_amt = fields.Float(string="Taxable Amount", store=True, compute='_compute_all_line')
    round_off_amt = fields.Float(string="Round Off Amount(+/-)", store=True, compute='_compute_all_line')	
    grand_tot_amt = fields.Float(string="Grand Total", store=True, compute='_compute_all_line')
    fixed_disc_amt = fields.Float(string="Fixed Discount Amount(-)", store=True, compute='_compute_all_line')
    net_amt = fields.Float(string="Net Amount", store=True, compute='_compute_all_line')
    manual_round_off = fields.Boolean(string="Apply Manual Round Off", default=False)

    line_ids = fields.One2many('ct.transaction.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.transaction.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.transaction.expenses.line', 'header_id', string="Other Charges", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.transaction.tax.line', 'header_id', string="Tax Breakup", copy=True, c_rule=True)

    product_ids = fields.Many2many('product.product', string="Product", ondelete='restrict', c_rule=True)

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


    def validate_expense_lines(self, warning_msg):
        if self.line_ids_b:
            for exp_line in self.line_ids_b:
                if exp_line.amt <= 0:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) amount should be greater than zero")
                if exp_line.disc_per < 0:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) discount should be greater than or equal to zero")
                if exp_line.disc_per > 100:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) discount should not be greater than hundred percent")


    def validate_serial_lines(self, detail_line, warning_msg):
        dub_serial = []
        serial_qty = 0
        for serial_line in detail_line.line_ids:
            serial_qty += serial_line.qty
            if serial_line.qty <= 0:
                warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero in serial no tab {serial_line.serial_no}")
            if serial_line.serial_no in dub_serial:
                warning_msg.append(f"{serial_line.serial_no} duplicate serial no not allowed for product({detail_line.description})")
            if serial_line.expiry_date < fields.Date.today():
                warning_msg.append(f"Product({detail_line.description}) expiry date should not be less than current date for serial no {serial_line.serial_no}")
            dub_serial.append(serial_line.serial_no)
        if detail_line.line_ids and serial_qty != detail_line.qty:
            warning_msg.append(f"Product({detail_line.description}) sum of serial no quantity should be equal to product quantity")


    def validate_detail_lines(self, detail_line, warning_msg):
        if detail_line.qty <= 0:
            warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero")
        if detail_line.unit_price <= 0:
            warning_msg.append(f"Product({detail_line.description}) unit price should be greater than zero")
        if detail_line.disc_per < 0:
            warning_msg.append(f"Product({detail_line.description}) discount should be greater than or equal to zero")
        if detail_line.disc_per > 100:
            warning_msg.append(f"Product({detail_line.description}) discount should not be greater than hundred percent")
        
        self.validate_serial_lines(detail_line, warning_msg)


    def validate_line_items(self, warning_msg):
        if not self.line_ids:
            warning_msg.append("System not allow to confirm/approve with empty line details")
        else:
            for detail_line in self.line_ids:
                self.validate_detail_lines(detail_line, warning_msg)


    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            self.validate_line_items(warning_msg)
            self.validate_expense_lines(warning_msg)
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.transaction.draft',
            'approve': CT_TRANSACTION
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

    def _process_tax_line(self, line, product, tax_line, price_unit, qty, discount, price_subtotal, type_tax_use_dict):

        tax_value_return = self.env['account.tax']._convert_to_tax_base_line_dict(
                                            self,
                                            partner=line.header_id.partner_id,
                                            currency=line.header_id.currency_id,
                                            product=product,
                                            taxes=tax_line,
                                            price_unit=price_unit,
                                            quantity=qty,
                                            discount=discount,
                                            price_subtotal=price_subtotal,
                                        )
        tax_results = self.env['account.tax']._compute_taxes([tax_value_return])
        totals = next(iter(tax_results['totals'].values()))
        amount_tax = totals['amount_tax']

        type_tax_use_dict[tax_line.tax_group_id.name] += amount_tax

    def _process_line_items(self, line_items, tax_dict):
        for line in line_items:
            if line.unit_price > 0:
                for tax_line in line.tax_ids:
                    self._process_tax_line(line, line.product_id, tax_line, line.unit_price, line.qty, line.disc_per, line.tot_amt, tax_dict)

    def _process_line_items_b(self, line_items_b, tax_dict):
        for line in line_items_b:
            if line.amt > 0:
                for tax_line in line.tax_ids:
                    self._process_tax_line(line, None, tax_line, line.amt, 1, line.disc_per, line.line_tot_amt, tax_dict)


    def _initialize_tax_dict(self):
        return {
            record['name']: 0
            for record in self.env['account.tax.group'].read_group([], ['name'], ['name'])
        }

    def _compute_footer_calculation(self):
        for data in self:
            data.tot_amt = sum(data.line_ids.mapped('tot_amt'))
            data.other_amt = sum(data.line_ids_b.mapped('amt'))
            data.disc_amt = sum(data.line_ids.mapped('disc_amt')) + sum(data.line_ids_b.mapped('disc_amt'))
            
            old_grand_total = data.taxable_amt + data.tax_amt

            data.taxable_amt = (data.tot_amt + data.other_amt) - data.disc_amt
            data.tax_amt = sum(data.line_ids.mapped('tax_amt')) + sum(data.line_ids_b.mapped('tax_amt'))

            if (old_grand_total != (data.taxable_amt + data.tax_amt)) or (not data.tot_amt):
                data.manual_round_off = False
                data.round_off_amt = 0.00
                data.fixed_disc_amt = 0.00
            
            if not data.manual_round_off:
                data.round_off_amt = round(data.taxable_amt + data.tax_amt) - (data.taxable_amt + data.tax_amt)
                data.round_off_amt = round(data.round_off_amt, 2)

            data.grand_tot_amt = data.taxable_amt + data.tax_amt + data.round_off_amt
            
            data.fixed_disc_amt = 0.00 if data.grand_tot_amt <= 0 else data.fixed_disc_amt
            
            data.net_amt = data.grand_tot_amt - data.fixed_disc_amt
    
    
    @api.depends('line_ids', 'line_ids_b', 'round_off_amt', 'fixed_disc_amt', 'manual_round_off')
    def _compute_all_line(self):
        for data in self:
            data.line_count = len(data.line_ids)
            data._compute_footer_calculation()
            type_tax_use_dict = data._initialize_tax_dict()
            data._process_line_items(data.line_ids, type_tax_use_dict)
            data._process_line_items_b(data.line_ids_b, type_tax_use_dict)
            data.line_ids_c = [(5, 0, 0)]
            tax_values = []
            for tx_name, tx_amt in type_tax_use_dict.items():
                if tx_amt > 0:
                    tax_values.append((0,0,{'tax_name':tx_name,'tax_amt':tx_amt}))
            data.line_ids_c = tax_values

    @api.onchange('partner_id')
    def onchange_supplier(self):
        if self.partner_id:
            self.address = self.partner_id.street

    @api.onchange('delivery_date')
    def onchange_delivery(self):
        if self.delivery_date and self.entry_date and self.delivery_date < self.entry_date:
            raise UserError(_("Delivery date should be greater than or equal to order date"))
    
    @api.onchange('round_off_amt')
    def onchange_round_off_amt(self):
        if self.manual_round_off:
            self.fixed_disc_amt = 0.00
            if self.round_off_amt > (self.taxable_amt + self.tax_amt):
                raise UserError(_("Round Off Amount should not be greater than Grand Total"))
            if self.round_off_amt < 0 and self.grand_tot_amt < 0:
                raise UserError(_("Round Off Amount should not be lesser than Grand Total"))
    
    @api.onchange('fixed_disc_amt')
    def onchange_fixed_disc_amt(self):
        if self.fixed_disc_amt:
            if self.fixed_disc_amt < 0:
                raise UserError(_("Fixed Discount Amount should not be lesser than zero"))
            if self.fixed_disc_amt > self.grand_tot_amt:
                raise UserError(_("Fixed Discount Amount should not be greater than Grand Total"))

    def save_record(self):
        self.trigger_del = True
        
        for line in self.line_ids:
            line.unlink()

        self.trigger_del = False
        if self.product_ids:
            for line in self.product_ids:
                self.line_ids = [(0,0,{
                                        'product_id': line.id,
                                        'description': line.name,
                                        'uom_id': line.uom_po_id.id if line.uom_po_id else '',
                                    })]

        return True

    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()

            if not self.draft_name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', 'ct.transaction.draft')], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """ %
                        (sequence_id.id,
                         sequence_id.code,
                         self.draft_date,
                         self.company_id.id,
                         self.division_id.id,
                         'division'))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.draft_date, action='confirm')

                self.draft_name = sequence

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_confirm' ,
                                            mail_queue_name = 'Entry Confirm Mail',
                                            subject = f"#Transaction {self.draft_name} Confirmed",
                                            mail_config_name = 'Transaction Confirm Mail'
                                        )

            self.transaction_sms_design(
                                        message_type = 'sms',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm SMS',
                                        content_text = f"#SMS:Transaction {self.draft_name} Confirmed"
                                    )

            self.transaction_sms_design(
                                        message_type = 'whatsapp',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm WhatsApp',
                                        content_text = f"#WhatsApp:Transaction {self.draft_name} Confirmed"
                                    )

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_TRANSACTION)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """ %
                        (sequence_id.id,
                         sequence_id.code,
                         self.entry_date,
                         self.company_id.id,
                         self.division_id.id,
                         'division'))
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

            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_approve' ,
                                            mail_queue_name = 'Entry Approve Mail',
                                            subject = f"#Transaction {self.name} Approved",
                                            mail_config_name = 'Transaction Approve Mail'
                                        )

        return True
    
    def entry_reject(self):
        if self.status == 'wfa':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.ap_rej_remark or not self.ap_rej_remark.strip():
                raise UserError(_("Reject remarks is must. Kindly enter the remarks in Approve / Reject Remarks field"))
            if self.ap_rej_remark and len(self.ap_rej_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters are must for Approve / Reject Remarks"))
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
                raise UserError(_(f"Minimum {min_char} characters are must for cancel remarks"))
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
        return super(CtTransaction, self).write(vals)


    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_TRANSACTION].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.user_id.email]

        return mail_ids
    
    def transaction_mail_data_design(self, **kw):
        self.env.cr.execute(
            """select ctm_template(%s,'%s','%s','%s')""" %
            (self.id,self.status,self.name or self.draft_name, self.env.user.partner_id.name,))
        data = self.env.cr.fetchall()

        trans_rec = kw.get('trans_rec', self)
        mail_queue_name = kw.get('mail_queue_name', '')
        mail_config_name = kw.get('mail_config_name', '')
        mail_type = kw.get('mail_type', 'transaction')

        subject = kw.get('subject', '')

        if trans_rec and data[0][0] and mail_queue_name and subject and mail_config_name:

            mail_ids = self.get_default_mail_ids(trans_id=trans_rec.id)
            default_to = mail_ids.get('email_to',[])

            vals = self.env['cp.mail.configuration'].mail_config_mailids_data(
                mail_type=mail_type, model_name=CT_TRANSACTION, mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            if trans_rec.line_ids_a:
                attachment = trans_rec.line_ids_a.mapped('attachment_ids')
            else:
                attachment = False

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_queue_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0], attachment=attachment)

        return True

    def transaction_sms_design(self, **kw):
        trans_rec = kw.get('trans_rec', self)
        sms_name = kw.get('sms_name', '')
        content_text = kw.get('content_text', '')
        message_type = kw.get('message_type', '')

        if trans_rec and sms_name and content_text and message_type:
            default_mobile = [self.user_id.mobile_no] if self.user_id.mobile_no else []

            vals = self.env['cp.sms.configuration'].sms_config_data(
                message_type=message_type, action_name=sms_name)
            mobile_no = ", ".join(set(default_mobile + vals.get('mobile_no', []))) if default_mobile or vals.get('mobile_no') else ''

            self.env['cp.sms.queue'].create_sms_queue(
                message_type = message_type, trans_rec = trans_rec,
                sms_name = sms_name, mobile_no = mobile_no, content_text = content_text)

        return True

    def value_readable_format(self, value, format='%.1f'):
        powers = [10**15, 10**12, 10**9, 10**6, 10**3]
        human_powers = ['Qa','T', 'B', 'M', 'K']

        for power, human_power in zip(powers, human_powers):
            if value >= power:
                return format % (float(value) / power) + ' ' + human_power
            else:
                value = round(value,2)
        return str(value)

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
            'my_today_value': 0,
            'today_highest_tot':0,
            'ref_no':'',
            'company_currency_symbol': self.env.company.currency_id.symbol
        }

        ct_trans = self.env[CT_TRANSACTION]
        result['all_draft'] = ct_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_trans.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_today_value'] = self.value_readable_format(sum(ct_trans.search([('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_today_value'] = self.value_readable_format(sum(ct_trans.search([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        max_transaction = max(ct_trans.search([('crt_date', '>=', fields.Date.today()), ('status', '=', 'approved')]), 
                      key=lambda t: t.net_amt, default=None)
        result['today_highest_tot'] = self.value_readable_format(max_transaction.net_amt) if max_transaction else 0
        result['ref_no'] = max_transaction.name if max_transaction else '-'

        return result
