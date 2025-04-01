# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from odoo.exceptions import UserError

CT_PURCHASE_ORDER = 'ct.purchase.order'
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

MODE_OF_PAYMENT = [('cash', 'Cash'),
                    ('credit', 'Credit'),
                    ('credit_card', 'Credit Card'),
                    ('not_applicable', 'Not Applicable')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

ENTRY_TYPE = [('direct', 'Direct'), ('from_pi', 'From PI')]

class CtPurchaseOrder(models.Model):
    _name = 'ct.purchase.order'
    _description = 'Purchase Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="PO No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, compute='_compute_header_status', default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="PO Date", copy=False, default=fields.Date.today)
    draft_name = fields.Char(string="Draft No", copy=False, index=True, readonly=True, size=30)
    draft_date = fields.Date(string="Draft Date", copy=False, default=fields.Date.today)
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    entry_type = fields.Selection(selection=ENTRY_TYPE, string="PO Mode")
    pr_no = fields.Char(string="PR No", copy=False)
    pr_date = fields.Char(string="PR Date", copy=False)
    comparison_id = fields.Many2one('ct.quotation.comparison') # compute='comparison_compute',readonly=True, store = True
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    address = fields.Char(string="Vendor Address", size=252)
    quotation_ref_no = fields.Char(string="Quotation Ref No", copy=False)
    quotation_ref_date = fields.Date(string="Quotation Ref Date", copy=False)
    currency_id = fields.Many2one('res.currency', store=True)
    bill_type = fields.Selection(MODE_OF_PAYMENT, string="Mode Of Payment", copy=False)
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_term_id = fields.Many2one(
    #     'kg.delivery.master', 'Delivery Term', domain=[
    #         ('active_trans', '!=', False), ('state', '=', 'approved')])
    delivery_date = fields.Date(string="Delivery Date", copy=False)

    
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')

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

    pr_line_ids = fields.Many2many('ct.purchase.request.line', string="Purchase Request", ondelete='cascade', domain="[('status', '=', 'approved'),('header_id.active_trans', '=', True),('header_id.department_id', '=', department_id),('flag_used', '=', False),('po_pending_qty', '>', 0)]")

    line_ids = fields.One2many('ct.purchase.order.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.purchase.order.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.purchase.order.expenses.line', 'header_id', string="Other Charges", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.purchase.order.tax.line', 'header_id', string="Tax Breakup", copy=True, c_rule=True)


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
            dub_expense = set()
            for exp_line in self.line_ids_b:
                if exp_line.amt <= 0:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) amount should be greater than zero")
                if exp_line.disc_per < 0:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) discount should be greater than or equal to zero")
                if exp_line.disc_per > 100:
                    warning_msg.append(f"Expense({exp_line.expense_id.name}) discount should not be greater than hundred percent")
                if exp_line.expense_id.id in dub_expense:
                    warning_msg.append(f"Duplicate expense are not allowed. Ref : {exp_line.expense_id.name}")
                if exp_line.tax_ids:
                    tax_groups = {tax.tax_group_id.name for tax in exp_line.tax_ids}
                    if 'IGST' in tax_groups and tax_groups & {'CGST', 'SGST'}:
                        warning_msg.append(
                            f"Expense ({exp_line.expense_id.name}) - the combination of IGST with CGST or SGST is not allowed."
                        )
                dub_expense.add(exp_line.expense_id.id)


    def validate_detail_lines(self, detail_line, warning_msg, dub_serial):
        if detail_line.qty <= 0:
            warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero")
        if detail_line.unit_price <= 0:
            warning_msg.append(f"Product({detail_line.description}) unit price should be greater than zero")
        if detail_line.disc_per < 0:
            warning_msg.append(f"Product({detail_line.description}) discount should be greater than or equal to zero")
        if detail_line.disc_per > 100:
            warning_msg.append(f"Product({detail_line.description}) discount should not be greater than hundred percent")
        if detail_line.tax_ids:
            tax_groups = {tax.tax_group_id.name for tax in detail_line.tax_ids}
            if 'IGST' in tax_groups and tax_groups & {'CGST', 'SGST'}:
                warning_msg.append(
                    f"Product ({detail_line.description}) - the combination of IGST with CGST or SGST is not allowed."
                )
        self.validate_serial_lines(detail_line, warning_msg, dub_serial)


    def validate_line_items(self, warning_msg):
        if not self.line_ids:
            warning_msg.append("System not allow to confirm/approve with empty line details")
        else:
            dub_product = set()
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
            'confirm': 'ct.purchase.order.draft',
            'approve': CT_PURCHASE_ORDER
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
                                            partner=line.header_id.user_id,
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
            old_grand_total_round_off = data.grand_tot_amt

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

            data.fixed_disc_amt = (
                0.00 
                if data.grand_tot_amt <= 0 or old_grand_total_round_off != data.grand_tot_amt 
                else data.fixed_disc_amt
            )
   
            data.net_amt = data.grand_tot_amt - data.fixed_disc_amt

    @api.depends('line_ids.status')
    def _compute_header_status(self):
        for request in self:
            if request.status in ('approved','part_in'):
            
                line_statuses = request.mapped('line_ids.status')
                
                if all(status == 'closed' for status in line_statuses):
                    request.status = 'closed'
                elif any(status == 'part_in' for status in line_statuses):
                    request.status = 'part_in'
                elif any(status == 'part_in' for status in line_statuses)and not all(status == 'closed' for status in line_statuses):
                    request.status = 'part_in'
                
    
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


    @api.onchange('vendor_id')
    def onchange_supplier(self):
        if self.vendor_id:
            self.address = ", ".join(filter(None, [
                self.vendor_id.street,
                self.vendor_id.street1,
                self.vendor_id.city_id.name,
                self.vendor_id.state_id.name,
                self.vendor_id.country_id.name
            ]))
        else:
            self.address = False

    @api.onchange('delivery_date')
    def onchange_delivery(self):
        if self.delivery_date and self.entry_date and self.delivery_date < self.entry_date:
            raise UserError(_("Delivery date should be greater than or equal to entry date"))
    
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

    @api.onchange('entry_type', 'department_id')
    def onchange_entry_type(self):
        self.line_ids = False
        self.pr_line_ids = [(5, 0, 0)]
        self.pr_no = False
        self.pr_date = False

    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()

            if not self.draft_name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', 'ct.purchase.order.draft')], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
                        (sequence_id.id,
                         sequence_id.code,
                         self.draft_date,
                         None,
                         None,
                         ''))
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
            self.line_ids.write({'status': 'wfa'})
        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_PURCHASE_ORDER)], limit=1)
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
            self.pr_update_logic()
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })
            self.line_ids.write({'status': 'approved'})

        return True

    def save_record(self):
        self.trigger_del = True
        self.line_ids.unlink()
        self.trigger_del = False

        request_nos = set()
        entry_dates = set()
        new_lines = []
        for line in self.pr_line_ids:
            request_nos.add(line.request_no)
            entry_dates.add(line.entry_date.strftime("%d/%m/%Y")) 

            price_list_rec = self.env['ct.vendor.price.list'].search([
                ('product_id', '=', line.product_id.id),
                ('vendor_id', '=', self.vendor_id.id),
                ('brand_id', '=', line.brand_id.id),
                ('status', '=', 'approved'),
                ('active_trans', '=', True)
            ], limit=1)

            if not price_list_rec:
                raise UserError(_(f"There is no approved price for item {line.product_id.name}"))

            if price_list_rec.validity_date and price_list_rec.validity_date < self.draft_date:
                raise UserError(_(f"There is no approved price for item {line.product_id.name}"))

            new_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'description': line.description,
                'uom_id': line.uom_id.id if line.uom_id else False,
                'brand_id': line.brand_id.id if line.brand_id else False,
                'qty': line.qty,
                'pr_line_id': line.id,
                'pi_qty': line.qty,
                'pending_qty': line.qty,
                'unit_price': price_list_rec.unit_price,
                'disc_per': price_list_rec.discount,
                'disc_amt': price_list_rec.discount_amt,
                'tax_ids': price_list_rec.tax_ids,
            }))

        self.pr_no = ",".join(sorted(request_nos))
        self.pr_date = ",".join(sorted(entry_dates))

        if new_lines:
            self.line_ids = new_lines

        return True

    def pr_update_logic(self):
        if self.entry_type == 'from_pi':
            for line in self.line_ids:
                if line.pr_line_id:
                    line.pr_line_id.pending_qty = max(0, line.pr_line_id.pending_qty - line.qty)

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
        return super(CtPurchaseOrder, self).write(vals)


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

        ct_trans = self.env[CT_PURCHASE_ORDER]
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