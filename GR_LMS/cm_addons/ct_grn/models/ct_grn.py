# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from odoo.exceptions import UserError

CT_GRN = 'ct.grn'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'
CT_GRN_LINE = 'ct.grn.line'

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
ENTRY_TYPE =  [('direct','Direct'),
               ('from_po','From PO'),
               ('from_pi','From PR')]

GRN_TYPE = [('dc_invoice', 'Invoice'), ('only_grn', 'DC')]



FREIGHT=[('inclusive', 'Inclusive'),
           ('extra_by_supplier', 'Extra By Supplier'),
           ('extra_at_our_cost', 'Extra at our Cost'),
           ('extra_by_company', 'Extra By Company')]

BILLING_STATUS=[('applicable', 'Applicable'),('not_applicable','Not applicable')]

class CtGRN(models.Model):
    _name = 'ct.grn'
    _description = 'GRN'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="GRN No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="GRN Date", copy=False, default=fields.Date.today)
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    address = fields.Char(string="Vendor Address", size=252)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    pay_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)

    entry_type = fields.Selection(selection=ENTRY_TYPE, string="Mode Of GRN", required=True)
    billing_status = fields.Selection(selection=BILLING_STATUS, string="Billing Status", default='applicable', required=True)
    grn_type = fields.Selection(selection=GRN_TYPE, string="GRN Type", required=False)
    dc_no = fields.Char(string="DC No")
    dc_date = fields.Date(string="DC Date")
    partner_invoice_no = fields.Char(string="Invoice No")
    partner_invoice_date = fields.Date(string="Invoice Date")
    freight = fields.Selection(selection=FREIGHT, string="Freight")

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

    pr_ids = fields.Many2many('ct.purchase.request', string="PR Nos", ondelete='cascade', domain=[('status', 'in', ('approved','part_in')),('active_trans', '=', True)])
    po_ids = fields.Many2many('ct.purchase.order', 'ct_grn_ct_purchase_order_rel', 'grn_id','po_id', string="PO Nos", ondelete='cascade', domain=[('status', 'in', ('approved','part_in')),('active_trans', '=', True)])

    line_ids = fields.One2many(CT_GRN_LINE, 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.grn.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.grn.expenses.line', 'header_id', string="Other Charges", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.grn.tax.line', 'header_id', string="Tax Breakup", copy=True, c_rule=True)


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


    def validate_serial_lines(self, detail_line, warning_msg, dub_serial):
        serial_qty = 0
        for serial_line in detail_line.line_ids:
            serial_qty += serial_line.qty
            if serial_line.qty <= 0:
                warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero in serial no tab {serial_line.serial_no}")
            if serial_line.serial_no in dub_serial:
                warning_msg.append(f"{serial_line.serial_no} duplicate serial no not allowed for product({detail_line.description})")
            if serial_line.expiry_date and serial_line.expiry_date < fields.Date.today():
                warning_msg.append(f"Product({detail_line.description}) expiry date should not be less than current date for serial no {serial_line.serial_no}")
            dub_serial.append(serial_line.serial_no)
        if detail_line.line_ids and serial_qty != detail_line.qty:
            warning_msg.append(f"Product({detail_line.description}) sum of serial no quantity should be equal to product quantity")


    def validate_detail_lines(self, detail_line, warning_msg, dub_serial):
        if detail_line.qty <= 0:
            warning_msg.append(f"Product({detail_line.description}) quantity should be greater than zero")
        if detail_line.unit_price <= 0:
            warning_msg.append(f"Product({detail_line.description}) unit price should be greater than zero")
        if detail_line.disc_per < 0:
            warning_msg.append(f"Product({detail_line.description}) discount should be greater than or equal to zero")
        if detail_line.disc_per > 100:
            warning_msg.append(f"Product({detail_line.description}) discount should not be greater than hundred percent")
        if detail_line.warranty_flag == 'applicable' and detail_line.warranty_category=='limited' and detail_line.warranty_period < 1:
            warning_msg.append(f"Product({detail_line.description}) warranty period should be greater than zero")
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
                if  detail_line.qty > detail_line.pr_pending_qty and detail_line.entry_type=='from_pi':
                    warning_msg.append(f"GRN quantity should not be greater than PR pending quantity. Ref : {detail_line.description}")
                if  detail_line.qty > detail_line.po_pending_qty and detail_line.entry_type=='from_po':
                    warning_msg.append(f"GRN quantity should not be greater than PO pending quantity. Ref : {detail_line.description}")
                else:
                    dub_product.add(combination)
                self.validate_detail_lines(detail_line, warning_msg, dub_serial)
        
    
    def validate_po(self, warning_msg):
        if self.po_ids and len(self.po_ids)>1:
            vendors=[po.vendor_id.id for po in self.po_ids]            
            if len(set(vendors))>1:
                warning_msg.append("Multiple vendors PO not allowed to process in single GRN")
        for po in self.po_ids:
            if po.vendor_id.id != self.vendor_id.id:
                warning_msg.append("PO vendor and GRN vendor not same")
                break

    def validate_dates(self, warning_msg):
        if self.entry_date and  self.dc_date and  self.dc_date > self.entry_date:
            warning_msg.append("DC Date should not be greater than GRN Date")
        if self.entry_date and self.partner_invoice_date and self.partner_invoice_date > self.entry_date:
            warning_msg.append("Invoice Date should not be greater than GRN Date")
        for rec in self.po_ids:
            if rec.entry_date and rec.entry_date > self.entry_date:
                warning_msg.append("GRN date should not be lesser than PO Date")
            if self.partner_invoice_date and rec.entry_date > self.partner_invoice_date:
                warning_msg.append("Invoice date should not be lesser than PO date")
            if self.dc_date and rec.entry_date > self.dc_date:
                warning_msg.append("DC Date Should be Greater or Equal to PO Date")
            
    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            self.validate_line_items(warning_msg)
            self.validate_expense_lines(warning_msg)
            self.validate_dates(warning_msg)
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)
    
    def po_validations(self, **kw):
        warning_msg = []        
        if self.entry_type == 'from_po':
            self.validate_po(warning_msg)

        return self.display_warnings(warning_msg, kw)
    


    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.grn.draft',
            'approve': CT_GRN
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
    def vendor_id_onchange(self):
        self.address = ", ".join(filter(None, [
                self.vendor_id.street,
                self.vendor_id.street1,
                self.vendor_id.city_id.name,
                self.vendor_id.state_id.name,
                self.vendor_id.country_id.name
            ]))
    
    @api.onchange('billing_status')
    def billing_status_onchange(self):
        if self.billing_status:
            self.grn_type = ''
            self.partner_invoice_no=False
            self.partner_invoice_date=False
            self.dc_date=False
            self.dc_no=False
    
    @api.onchange('entry_type')
    def entry_type_onchange(self):
        self.line_ids=False
        self.po_ids=False
        self.pr_ids=False
    
    @api.onchange('grn_type')
    def grn_type_onchange(self):
        if self.grn_type!='dc_invoice':
            self.partner_invoice_no=False
            self.partner_invoice_date=False

    @api.onchange('po_ids','pr_ids')
    def entry_type_onchange(self):
        self.line_ids=False
        self.line_ids_b=False
        if self.po_ids:
            vendors=self.po_ids.mapped('vendor_id.id')
            if len(set(vendors))==1:
                self.vendor_id= vendors[0]
            else:
                raise UserError(_("PO should be from one vendor not multiple"))


    
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

    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

            self.transaction_mail_data_design(
                                            trans_rec = self, entry_action = 'entry_confirm' ,
                                            mail_queue_name = 'Entry Confirm Mail',
                                            subject = "#Transaction Confirmed",
                                            mail_config_name = 'Transaction Confirm Mail'
                                        )

            self.transaction_sms_design(
                                        message_type = 'sms',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm SMS',
                                        content_text = "#SMS:Transaction Confirmed"
                                    )

            self.transaction_sms_design(
                                        message_type = 'whatsapp',
                                        trans_rec = self,
                                        sms_name = 'Entry Confirm WhatsApp',
                                        content_text = "#WhatsApp:Transaction Confirmed"
                                    )

        return True

    def load_product(self):
        
        if self.entry_type:
            if self.entry_type=='from_pi' and self.pr_ids:
                for data in self.pr_ids:
                    for pr_line in  data.line_ids:
                        if pr_line.pending_qty > 0 and pr_line.status in ('approved','part_in') and pr_line.flag_used == False:
                            self.env[CT_GRN_LINE].create({
                                'header_id': self.id,
                                'product_id': pr_line.product_id.id,
                                'warranty_flag': 'applicable' if pr_line.product_id.serial_no_req == 'required' else False,
                                'brand_id': pr_line.brand_id.id,
                                'description': pr_line.product_id.name,
                                'qty': 0.00,
                                'pr_line_id': pr_line.id,
                                'entry_type': self.entry_type,
                                'uom_id': pr_line.uom_id.id,
                                'pr_qty': pr_line.qty,
                                'pr_pending_qty': pr_line.pending_qty,
                                })
                            pr_line.flag_used = True
            if self.entry_type=='from_po' and self.po_ids:
                self.po_validations()
                for data in self.po_ids:
                    for po_line in data.line_ids:
                        if po_line.pending_qty > 0 and po_line.status in ('approved','part_in') and po_line.flag_used == False:
                            self.env[CT_GRN_LINE].create({
                                'header_id': self.id,
                                'product_id': po_line.product_id.id,
                                'warranty_flag': 'applicable' if po_line.product_id.serial_no_req == 'required' else False,
                                'brand_id': po_line.brand_id.id,
                                'description': po_line.product_id.name,
                                'qty': po_line.pending_qty,
                                'po_line_id': po_line.id,
                                'entry_type': self.entry_type,
                                'uom_id': po_line.uom_id.id,
                                'po_qty': po_line.qty,
                                'po_pending_qty': po_line.pending_qty,
                                'unit_price': po_line.unit_price,
                                'disc_per': po_line.disc_per,
                                'disc_amt': po_line.disc_amt,
                                'tax_amt': po_line.tax_amt,
                                'tax_ids': [(6, 0, [tax.id for tax in po_line.tax_ids])] or False
                                })
                            po_line.flag_used = True
                    self.line_ids_b.unlink()
                    for po_exp_line in data.line_ids_b:
                        self.env['ct.grn.expenses.line'].create({
                                    'header_id': self.id,
                                    'expense_id': po_exp_line.expense_id.id,
                                    'description': po_exp_line.description,
                                    'amt': po_exp_line.amt,
                                    'disc_per': po_exp_line.disc_per,
                                    'disc_amt': po_exp_line.disc_amt,
                                    'tax_amt': po_exp_line.tax_amt,
                                    'tax_ids': [(6, 0, [tax.id for tax in po_exp_line.tax_ids])] or False,
                                    'line_tot_amt':po_exp_line.line_tot_amt
                                    })
                    

    
    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_GRN)], limit=1)
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
            
            stock_move_obj = self.env['ct.stock.move']
            stock_lot = self.env['ct.stock.lot']
            
            for grn_line in self.line_ids:
                #Code for Direct GRN
                if self.entry_type in ('direct','from_po','from_pi'):
                    vendor_location = self.env['cm.stock.location'].search([('name','=','Vendor Location')],limit=1)
                    main_store = self.env['cm.stock.location'].search([('name','=','Main Store')],limit=1)

                    stock_move_obj.create({
                        'name':self.name,
                        'entry_date':self.entry_date,
                        'from_location_id':vendor_location.id,
                        'to_location_id':main_store.id,
                        'qty':grn_line.qty,
                        'product_id':grn_line.product_id.id,
                        'description':grn_line.product_id.name,
                        'brand_id':grn_line.brand_id.id,
                        'uom_id':grn_line.uom_id.id,
                        'unit_price':grn_line.unit_price,
                        'currency_id':self.currency_id.id,
                        'entry_mode':'auto',
                        'user_id':self.user_id.id,
                        'ap_rej_user_id':self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT),
                        'status':'approved'
                        })
                
                    #Lot creation
                    if grn_line.product_id.serial_no_req=='required':
                        if not grn_line.line_ids:
                            raise UserError(_(f"The following product need serial no, so kindly enter serial no details in serial no tab, Ref - {grn_line.product_id.name}"))
                    if grn_line.uom_id.id != grn_line.product_id.uom_id.id:
                        po_uom = grn_line.uom_id.id
                        store_uom = grn_line.product_id.uom_id.id
                        po_uom_qty = grn_line.qty
                        store_uom_qty = grn_line.qty*grn_line.product_id.uom_coff
                        price_unit = grn_line.line_tot_amt/grn_line.qty
                    else:
                        po_uom = grn_line.uom_id.id
                        store_uom = grn_line.uom_id.id
                        po_uom_qty = grn_line.qty
                        store_uom_qty = grn_line.qty
                        price_unit = grn_line.line_tot_amt/grn_line.qty
                    
                    serial_no = ''
                    lot_type = ''
                    parent_id = False
                    warranty_date=False
                    if grn_line.warranty_from=='custom':
                        warranty_date = grn_line.warranty_date 
                    elif grn_line.warranty_from == 'from_grn':
                        warranty_date = grn_line.header_id.entry_date
                    elif grn_line.warranty_from == 'from_invoice':
                        warranty_date = grn_line.header_id.partner_invoice_date

                    if grn_line.line_ids:
                        for s_rec in grn_line.line_ids:
                            if grn_line.uom_id.id != grn_line.product_id.uom_id.id:
                                po_uom = grn_line.uom_id.id
                                store_uom = grn_line.product_id.uom_id.id
                                po_uom_qty = s_rec.qty
                                store_uom_qty = s_rec.qty*grn_line.product_id.uom_coff
                                price_unit = grn_line.line_tot_amt/grn_line.qty
                            else:
                                po_uom = grn_line.uom_id.id
                                store_uom = grn_line.uom_id.id
                                po_uom_qty = s_rec.qty
                                store_uom_qty = s_rec.qty
                                price_unit = grn_line.line_tot_amt/grn_line.qty
                            
                            if s_rec.replace_sno:
                                self.env.cr.execute(
                                    """select id from ct_stock_lot where serial_no='%s' order by id desc limit 1""" % (s_rec.serial_no.strip()))
                                serial_no_id = self.env.cr.dictfetchall()
                                if serial_no_id:
                                    serial_no = s_rec.replace_sno
                                    lot_type = 'replacement'
                                    parent_id = serial_no_id[0]['id']
                                else:
                                    serial_no = s_rec.serial_no
                                    lot_type = 'new'                                
                            else:
                                serial_no = s_rec.serial_no
                                lot_type = 'new'
                            self.env.cr.execute("""select id from ct_stock_lot where upper(REPLACE(serial_no, ' ', ''))  = '%s' order by id desc limit 1""" % (serial_no.strip().replace(' ','')))
                            existing_sno = self.env.cr.dictfetchall()

                            if serial_no and existing_sno:
                                raise UserError(_(f"Serial No already exist in the stock, Ref : {serial_no}"))
                            
                            stock_lot.create({
                                'name':self.name,
                                'entry_date':self.entry_date,
                                'serial_no':serial_no,
                                'product_id':grn_line.product_id.id,
                                'description':grn_line.product_id.name,
                                'brand_id':grn_line.brand_id.id,
                                'unit_price':price_unit or grn_line.unit_price,
                                'currency_id':self.currency_id.id,
                                'entry_mode':'auto',
                                'lot_type':lot_type,
                                'store_uom_id':store_uom,
                                'store_uom_qty':store_uom_qty,
                                'store_pend_qty':store_uom_qty,
                                'po_uom_id':po_uom,
                                'po_uom_qty':po_uom_qty,
                                'po_pend_qty':po_uom_qty,
                                'warranty':grn_line.warranty_flag,
                                'from_date':warranty_date ,
                                'remarks':grn_line.remarks,
                                'user_id':self.confirm_user_id.id,
                                'ap_rej_user_id':self.env.user.id,
                                'ap_rej_date': time.strftime(TIME_FORMAT),
                                'parent_id':parent_id,
                                'expiry_date':s_rec.expiry_date if s_rec.expiry_date else grn_line.warranty_to_date,
                                'status':'approved'
                                })
                    else:
                        stock_lot.create({
                            'name':self.name,
                            'entry_date':self.entry_date,
                            'serial_no':self.name,
                            'product_id':grn_line.product_id.id,
                            'description':grn_line.product_id.name,
                            'brand_id':grn_line.brand_id.id,
                            'unit_price': price_unit,
                            'currency_id':self.currency_id.id,
                            'entry_mode':'auto',
                            'lot_type':'new',
                            'store_uom_id':store_uom,
                            'store_uom_qty':store_uom_qty,
                            'store_pend_qty':store_uom_qty,
                            'po_uom_id':po_uom,
                            'po_uom_qty':po_uom_qty,
                            'po_pend_qty':po_uom_qty,
                            'warranty':grn_line.warranty_flag,
                            'from_date':warranty_date ,
                            'expiry_date':grn_line.warranty_to_date,
                            'remarks':grn_line.remarks,
                            'user_id':self.confirm_user_id.id,
                            'ap_rej_user_id':self.env.user.id,
                            'ap_rej_date': time.strftime(TIME_FORMAT),
                            'parent_id':parent_id,
                            'status':'approved'
                            })
                    if grn_line.entry_type == "from_pi" and grn_line.pr_line_id:
                        grn_line.pr_line_id.pending_qty-=grn_line.qty
                        if grn_line.pr_line_id.pending_qty>0:
                            grn_line.pr_line_id.flag_used=False

                    
                    #for Po need to Change logic
                    if grn_line.entry_type == "from_po" and grn_line.po_line_id:
                        grn_line.po_line_id.pending_qty-=grn_line.qty
                        if grn_line.po_line_id.pending_qty>0:
                            grn_line.po_line_id.flag_used=False
            
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
        return super(CtGRN, self).write(vals)


    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_GRN].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.user_id.email]

        return mail_ids
    
    def transaction_mail_data_design(self, **kw):
        self.env.cr.execute(
            """select ctm_template(%s,'%s','%s','%s')""" %
            (self.id,self.status,self.name or '', self.env.user.partner_id.name,))
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
                mail_type=mail_type, model_name=CT_GRN, mail_name=mail_config_name)

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

        ct_trans = self.env[CT_GRN]
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