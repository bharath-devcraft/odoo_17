# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_QUOTATION_COMPARISON = 'ct.quotation.comparison'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RES_COMPANY = 'res.company'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'
CM_VENDOR_MASTER = 'cm.vendor.master'
RES_CURRENCY = 'res.currency'

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

PRICE_TERMS = [('inclusive', 'Inclusive of all Tax and Duties'),
               ('exclusive', 'Exclusive of all Tax an Duties')]

FREIGHT_TYPE = [('inclusive', 'Inclusive'),
                ('extra_by_supplier', 'Extra By Supplier'),
                ('extra_at_our_cost', 'Extra at our Cost'),
                ('extra_by_company', 'Extra By Company')]

class CtQuotationComparison(models.Model):
    _name = 'ct.quotation.comparison'
    _description = 'Quotation Comparison'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Comparison No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    entry_date = fields.Date(string="Comparison Date", copy=False, default=fields.Date.today)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)

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

    rfq_name = fields.Char(string="RFQ Name", c_rule=True)
    rfq_id = fields.Many2one('ct.rfq', string="RFQ No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])
    warranty_remarks = fields.Text(string="Warranty Remarks", copy=False)
    qs_details = fields.Many2many('ct.quotation.submit', string="Quotation Submit", ondelete='cascade', domain="[('status', '=', 'approved'),('active_trans', '=', True),('is_compared', '=', False), ('line_total', '>', 0)]")

    vendor_1_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_2_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_3_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_4_currency_partner_mapping = fields.Many2one(RES_CURRENCY, string="Currency", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    round_off_remark = fields.Text(string="Round Off Remarks")
    vendor_1_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 1", readonly=True)
    vendor_1_name = fields.Char(string="Vendor", readonly=False, size=200)
    vendor_1_total_amt = fields.Float(string="Total Amount", store=True, digits=(12, 2))
    vendor_1_other_amt = fields.Float(string="Other Charges(+)", store=True, digits=(12, 2))
    vendor_1_discount_amt = fields.Float(string="Discount Amount(-)", store=True, digits=(12, 2))
    vendor_1_taxable_amt = fields.Float(string="Taxable Amount", store=True, digits=(12, 2))
    vendor_1_tax_amt = fields.Float(string="Tax Amount(+)", store=True, digits=(12, 2))
    vendor_1_round_off_amt = fields.Float(string="Round Off(+/-)",  store=True,digits=(12, 2))
    vendor_1_net_amt = fields.Float(string="Net Amount", store=True, digits=(12, 2))


    vendor_2_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 2", readonly=True)
    vendor_2_name = fields.Char(string="Vendor", readonly=False, size=200)
    vendor_2_total_amt = fields.Float(string="Total Amount", store=True, digits=(12, 2))
    vendor_2_other_amt = fields.Float(string="Other Charges(+)", store=True, digits=(12, 2))
    vendor_2_discount_amt = fields.Float(string="Discount Amount(-)", store=True, digits=(12, 2))
    vendor_2_taxable_amt = fields.Float(string="Taxable Amount", store=True, digits=(12, 2))
    vendor_2_tax_amt = fields.Float(string="Tax Amount(+)", store=True, digits=(12, 2))
    vendor_2_round_off_amt = fields.Float(string="Round Off(+/-)", store=True, digits=(12, 2))
    vendor_2_net_amt = fields.Float(string="Net Amount", store=True, digits=(12, 2))

    vendor_3_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 3", readonly=True)
    vendor_3_name = fields.Char(string="Vendor", readonly=False, size=200)
    vendor_3_total_amt = fields.Float(string="Total Amount", store=True, digits=(12, 2))
    vendor_3_other_amt = fields.Float(string="Other Charges(+)", store=True, digits=(12, 2))
    vendor_3_discount_amt = fields.Float(string="Discount Amount(-)", store=True, digits=(12, 2))
    vendor_3_taxable_amt = fields.Float(string="Taxable Amount", store=True, digits=(12, 2))
    vendor_3_tax_amt = fields.Float(string="Tax Amount(+)", store=True, digits=(12, 2))
    vendor_3_round_off_amt = fields.Float(string="Round Off(+/-)", store=True, digits=(12, 2))
    vendor_3_net_amt = fields.Float(string="Net Amount", store=True, digits=(12, 2))

    vendor_4_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 4", readonly=True)
    vendor_4_name = fields.Char(string="Vendor", readonly=False, size=200)
    vendor_4_total_amt = fields.Float(string="Total Amount", store=True, digits=(12, 2))
    vendor_4_other_amt = fields.Float(string="Other Charges(+)", store=True, digits=(12, 2))
    vendor_4_discount_amt = fields.Float(string="Discount Amount(-)", store=True, digits=(12, 2))
    vendor_4_taxable_amt = fields.Float(string="Taxable Amount", store=True, digits=(12, 2))
    vendor_4_tax_amt = fields.Float(string="Tax Amount(+)", store=True, digits=(12, 2))
    vendor_4_round_off_amt = fields.Float(string="Round Off(+/-)", store=True, digits=(12, 2))
    vendor_4_net_amt = fields.Float(string="Net Amount", store=True, digits=(12, 2))

    vendor_5_id = fields.Many2one(CM_VENDOR_MASTER, string="Vendor 5", readonly=True)
    vendor_5_name = fields.Char(string="Vendor", readonly=False, size=200)
    vendor_5_total_amt = fields.Float(string="Total Amount", store=True, digits=(12, 2))
    vendor_5_other_amt = fields.Float(string="Other Charges(+)", store=True, digits=(12, 2))
    vendor_5_discount_amt = fields.Float(string="Discount Amount(-)", store=True, digits=(12, 2))
    vendor_5_taxable_amt = fields.Float(string="Taxable Amount", store=True, digits=(12, 2))
    vendor_5_tax_amt = fields.Float(string="Tax Amount(+)", store=True, digits=(12, 2))
    vendor_5_round_off_amt = fields.Float(string="Round Off(+/-)", digits=(12, 2))
    vendor_5_net_amt = fields.Float(string="Net Amount", store=True, digits=(12, 2))

    payment_terms_vendor_1 = fields.Many2one('cm.payment.term', string="Payment", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_terms_vendor_1 = fields.Many2one(
    #     'kg.delivery.master', 'Delivery', readonly=True, states={
    #         'draft': [
    #             ('readonly', False)]})
    price_terms_vendor_1 = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive', readonly=True)
    specification_terms_vendor_1 = fields.Text(string="Specification")
    freight_type_vendor_1 = fields.Selection(selection=FREIGHT_TYPE, string="Freight", readonly=True)
    warranty_vendor_1 = fields.Char(string="Warranty")
    quotation_ref_no_vendor_1 = fields.Char(string="Quotation Ref No")
    quotation_ref_date_vendor_1 = fields.Date(string="Quotation Ref Date")
    remarks_vendor_1 = fields.Text(string="Remarks")

    
    payment_terms_vendor_2 = fields.Many2one('cm.payment.term', string="Payment", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_terms_vendor_2 = fields.Many2one(
    #     'kg.delivery.master', 'Delivery', readonly=True, states={
    #         'draft': [
    #             ('readonly', False)]})
    price_terms_vendor_2 = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive', readonly=True)
    specification_terms_vendor_2 = fields.Text(string="Specification")
    freight_type_vendor_2 = fields.Selection(selection=FREIGHT_TYPE, string="Freight",readonly=True)
    warranty_vendor_2 = fields.Char(string="Warranty")
    quotation_ref_no_vendor_2 = fields.Char(string="Quotation Ref No")
    quotation_ref_date_vendor_2 = fields.Date(string="Quotation Ref Date")
    remarks_vendor_2 = fields.Text(string="Remarks")

    payment_terms_vendor_3 = fields.Many2one('cm.payment.term', string="Payment", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_terms_vendor_3 = fields.Many2one(
    #     'kg.delivery.master', 'Delivery', readonly=True, states={
    #         'draft': [
    #             ('readonly', False)]})
    price_terms_vendor_3 = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive', readonly=True)
    specification_terms_vendor_3 = fields.Text(string="Specification")
    freight_type_vendor_3 = fields.Selection(selection=FREIGHT_TYPE, string="Freight",readonly=True)
    warranty_vendor_3 = fields.Char(string="Warranty")
    quotation_ref_no_vendor_3 = fields.Char(string="Quotation Ref No")
    quotation_ref_date_vendor_3 = fields.Date(string="Quotation Ref Date")
    remarks_vendor_3 = fields.Text(string="Remarks")


    payment_terms_vendor_4 = fields.Many2one('cm.payment.term', string="Payment", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_terms_vendor_4 = fields.Many2one(
    #     'kg.delivery.master', 'Delivery', readonly=True, states={
    #         'draft': [
    #             ('readonly', False)]})
    price_terms_vendor_4 = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive', readonly=True)
    specification_terms_vendor_4 = fields.Text(string="Specification")
    freight_type_vendor_4 = fields.Selection(selection=FREIGHT_TYPE, string="Freight",readonly=True)
    warranty_vendor_4 = fields.Char(string="Warranty")
    quotation_ref_no_vendor_4 = fields.Char(string="Quotation Ref No")
    quotation_ref_date_vendor_4 = fields.Date(string="Quotation Ref Date")
    remarks_vendor_4 = fields.Text(string="Remarks")

    warranty_remarks = fields.Text(string="Warranty Remarks")
    is_compared = fields.Boolean(string="Compared")
    specification_1 = fields.One2many('ct.quotation.comparison.specification.line', 'header_id_1', string="Specification")
    specification_2 = fields.One2many('ct.quotation.comparison.specification.line', 'header_id_2', string="Specification")
    specification_3 = fields.One2many('ct.quotation.comparison.specification.line', 'header_id_3', string="Specification")
    specification_4 = fields.One2many('ct.quotation.comparison.specification.line', 'header_id_4', string="Specification")
    
    more_lp_remark = fields.Text(string="More LP Remarks")
    created_user_remarks = fields.Text(string="Less Supplier Remarks(Created User)")
    verified_user_remarks = fields.Text(string="Less Supplier Remarks(Verified User)")

    line_ids = fields.One2many('ct.quotation.comparison.line', 'header_id', string="Quotation Comparison Line", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.quotation.comparison.line', 'header_id', 'Item Details', ondelete='cascade', copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.quotation.comparison.line', 'header_id', 'Item Details', ondelete='cascade', copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.quotation.comparison.line', 'header_id', 'Item Details', ondelete='cascade', copy=True, c_rule=True)
    line_ids_d = fields.One2many('ct.quotation.comparison.line', 'header_id', 'Item Details', ondelete='cascade', copy=True, c_rule=True)
    line_ids_e = fields.One2many('ct.quotation.comparison.line', 'header_id', 'Item Details', ondelete='cascade', copy=True, c_rule=True)
    line_ids_f = fields.One2many('ct.quotation.comparison.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_expense_ids_a = fields.One2many('ct.quotation.comparison.expenses.line', 'header_id', 'Other Charges', ondelete='cascade', copy=True, c_rule=True)
    line_expense_ids_b = fields.One2many('ct.quotation.comparison.expenses.line', 'header_id', 'Other Charges', ondelete='cascade', copy=True, c_rule=True)
    line_expense_ids_c = fields.One2many('ct.quotation.comparison.expenses.line', 'header_id', 'Other Charges', ondelete='cascade', copy=True, c_rule=True)
    line_expense_ids_d = fields.One2many('ct.quotation.comparison.expenses.line', 'header_id', 'Other Charges', ondelete='cascade', copy=True, c_rule=True)
    line_expense_ids_e = fields.One2many('ct.quotation.comparison.expenses.line', 'header_id', 'Other Charges', ondelete='cascade', copy=True, c_rule=True)

    @api.onchange('rfq_id')
    def onchange_rfq_name(self):
        self.rfq_name = self.rfq_id.rfq_name if self.rfq_id else False

        self.env['ct.quotation.comparison.line'].search([('header_id', '=', self._origin.id)]).unlink()
        self.env['ct.quotation.comparison.expenses.line'].search([('header_id', '=', self._origin.id)]).unlink()

        self.reset_vendor_fields()

        self.qs_details = [(5, 0, 0)]

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
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'approve': CT_QUOTATION_COMPARISON
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
                        [('code', '=', CT_QUOTATION_COMPARISON)], limit=1)
                if sequence_id:
                    self.env.cr.execute(
                        """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
                        (sequence_id.id,
                         sequence_id.code,
                         self.entry_date,
                         self.company_id.id,
                         None,
                         'company'))
                    sequence = self.env.cr.fetchone()
                    sequence = sequence[0]
                else:
                    sequence = ''

                if not sequence:
                    self.sequence_no_validations(date=self.entry_date, action='approve')

                self.name = sequence

            self.quotation_submit_line_locking()
            self.approved_price_list_creation()
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

    def reset_vendor_fields(self):
        vendor_fields_common = [
            "total_amt", "other_amt", "discount_amt", "tax_amt", "taxable_amt", 
            "round_off_amt", "net_amt", "id", "name"
        ]
        
        vendor_fields_specific = [
            "payment_terms", "price_terms", "specification_terms", 
            "freight_type", "remarks", "warranty", 
            "quotation_ref_no", "quotation_ref_date"
        ] #delivery_terms

        for i in range(1, 5):
            for field in vendor_fields_common:
                setattr(self, f"vendor_{i}_{field}", '')

            for field in vendor_fields_specific:
                setattr(self, f"{field}_vendor_{i}", '')

        self.more_lp_remark = ''
        self.round_off_remark = ''

    def qs_load_details(self):
        self.env.cr.execute("DELETE FROM ct_quotation_comparison_line WHERE header_id = %s", (self.id,))
        self.env.cr.execute("DELETE FROM ct_quotation_comparison_expenses_line WHERE header_id = %s", (self.id,))

        self.reset_vendor_fields()

        self.qs_details = [(5, 0, 0)]

        qs_model = self.env['ct.quotation.submit']
        domain = [
            ('status', '=', 'approved'),
            ('active_trans', '=', True),
            ('rfq_id', '=', self.rfq_id.id),
            ('is_compared', '=', False),
            ('line_total', '>', 0)
        ]
        qs_recs = qs_model.search(domain).ids
        if qs_recs:
            self.qs_details = [(6, 0, qs_recs)]

    def qs_compare(self):
        self.env.cr.execute("DELETE FROM ct_quotation_comparison_line WHERE header_id = %s", (self.id,))
        self.env.cr.execute("DELETE FROM ct_quotation_comparison_expenses_line WHERE header_id = %s", (self.id,))

        self.reset_vendor_fields()

        if len(self.qs_details) > 4:
            raise UserError(_("Limit exceeded! You can only submit up to 4 times."))

        vendor_count = 1
        for qs_rec in self.qs_details:
            vendor_data = {
                f'vendor_{vendor_count}_id': qs_rec.vendor_id.id or 1,
                f'vendor_{vendor_count}_name': qs_rec.vendor_name or '',
                f'payment_terms_vendor_{vendor_count}': qs_rec.payment_term_id.id,
                # f'delivery_terms_vendor_{vendor_count}': qs_rec.delivery_term_id.id,
                f'price_terms_vendor_{vendor_count}': qs_rec.price,
                f'specification_terms_vendor_{vendor_count}': qs_rec.specification or '',
                f'freight_type_vendor_{vendor_count}': qs_rec.freight_type or '',
                f'remarks_vendor_{vendor_count}': qs_rec.remarks or '-',
                f'warranty_vendor_{vendor_count}': qs_rec.warranty or '-',
                f'quotation_ref_no_vendor_{vendor_count}': qs_rec.quotation_ref_no,
                f'quotation_ref_date_vendor_{vendor_count}': qs_rec.quotation_ref_date,
                f'vendor_{vendor_count}_currency_partner_mapping': qs_rec.currency_id.id,
            }

            self.write(vendor_data)

            comparison_line = self.env['ct.quotation.comparison.line']
            s_no = 0
            specifications = []
            for qs_line_rec in qs_rec.line_ids:
                if qs_line_rec.is_compared:
                    continue

                s_no += 1
                specify = qs_line_rec.specification or ''
                if specify:
                    specifications.append(f"{s_no}. {specify}")

                dup_product_id = comparison_line.search([
                    ('description', '=', qs_line_rec.description),
                    ('uom_id', '=', qs_line_rec.uom_id.id),
                    ('header_id', '=', self.id)
                ], limit=1)
                vendor_data = {
                    f'vendor_{vendor_count}_qs_line_id': qs_line_rec.id,
                    f'vendor_{vendor_count}_price': qs_line_rec.unit_price,
                    f'vendor_{vendor_count}_value': qs_line_rec.line_tot_amt,
                    f'vendor_{vendor_count}_discount': qs_line_rec.disc_per or 0,
                    f'vendor_{vendor_count}_discount_amt': qs_line_rec.disc_amt or 0,
                    f'vendor_{vendor_count}_tax_amt': qs_line_rec.tax_amt or 0,
                    f'vendor_{vendor_count}_warranty_period': qs_line_rec.warranty_period or 0,
                    f'vendor_{vendor_count}_warranty_from': qs_line_rec.warranty_from or '',
                }
                if not dup_product_id:
                    qc_line_id = comparison_line.create({
                        'header_id': self.id,
                        'product_id': qs_line_rec.product_id.id or None,
                        'description': qs_line_rec.description,
                        'brand_id': qs_line_rec.brand_id.id,
                        'brand_desc': qs_line_rec.brand_desc or '',
                        'uom_id': qs_line_rec.uom_id.id,
                        'qty': qs_line_rec.qty,
                    })
                    qc_line_id.write(vendor_data)
                else:
                    dup_product_id.write(vendor_data)

                if qs_line_rec.tax_ids:
                    tax_list = qs_line_rec.tax_ids.ids
                    tax_column = f'vendor_{vendor_count}_tax_ids'
                    (qc_line_id if not dup_product_id else dup_product_id).write({tax_column: [(6, 0, tax_list)]})

            specification_string = '\n'.join(specifications)
            if specification_string:
                setattr(self, f"specification_terms_vendor_{vendor_count}", specification_string)

            expense_comparison = self.env['ct.quotation.comparison.expenses.line']
            expense_data = []
            for qs_expense_line in qs_rec.line_ids_b:
                expense_data.append({
                    'header_id': self.id,
                    f'vendor_{vendor_count}_expense_id': qs_expense_line.expense_id.id,
                    f'vendor_{vendor_count}_description': qs_expense_line.description,
                    f'vendor_{vendor_count}_amt': qs_expense_line.amt,
                    f'vendor_{vendor_count}_line_tot_amt': qs_expense_line.line_tot_amt,
                    f'vendor_{vendor_count}_disc_per': qs_expense_line.disc_per,
                    f'vendor_{vendor_count}_disc_amt': qs_expense_line.disc_amt or 0,
                    f'vendor_{vendor_count}_tax_ids': [(6, 0, qs_expense_line.tax_ids.ids)] if qs_expense_line.tax_ids else False,
                    f'vendor_{vendor_count}_tax_amt': qs_expense_line.tax_amt or 0,
                })
            expense_comparison.create(expense_data)

            vendor_count +=1


        for line_rec in self.line_ids:
            value_list = []
            value_map = {}
            field_names = [f"vendor_{j}_value" for j in range(1, vendor_count)]
            values = line_rec.read(field_names)[0]

            for j in range(1, vendor_count):
                value = values.get(f"vendor_{j}_value", 0.0) or 0.0
                value_list.append(value)
                value_map[j] = value

            if not any(value_list):
                continue

            min_value = min(filter(lambda v: v > 0, value_list), default=0.0)

            if min_value > 0:
                min_indexes = [index for index, value in value_map.items() if value == min_value]

                for min_index in min_indexes:
                    self.env.cr.execute(
                        "UPDATE ct_quotation_comparison_line SET vendor_%s_select='t' WHERE id=%%s" % min_index,
                        (line_rec.id,)
                    )
                    # self.env.cr.execute(
                    #     """
                    #     UPDATE ct_quotation_comparison_line
                    #     SET brand_id = (SELECT brand_id FROM ch_quotation_submission_line WHERE id = vendor_%s_qs_line_id),
                    #         brand_desc = (SELECT brand_desc FROM ch_quotation_submission_line WHERE id = vendor_%s_qs_line_id)
                    #     WHERE id=%%s
                    #     """ % (min_index, min_index),
                    #     (line_rec.id,)
                    # )

        self.is_compared = True
        self.calculate_total()

    def quotation_submit_line_locking(self):
        for line in self.line_ids:
            qs_line_id = False

            if line.vendor_1_select:
                qs_line_id = line.vendor_1_qs_line_id
            elif line.vendor_2_select:
                qs_line_id = line.vendor_2_qs_line_id
            elif line.vendor_3_select:
                qs_line_id = line.vendor_3_qs_line_id
            elif line.vendor_4_select:
                qs_line_id = line.vendor_4_qs_line_id


            if qs_line_id:
                qs_line_recs = self.env['ct.quotation.submit.line'].search([
                    ('id', '=', qs_line_id),
                    ('product_id', '=', line.product_id.id),
                    ('brand_id', '=', line.brand_id.id),
                    ('uom_id', '=', line.uom_id.id)
                ])

                qs_line_recs.write({'is_compared': True})

    def approved_price_list_creation(self):
        for line in self.line_ids:
            selected_index = next((j for j in range(1, 5) if getattr(line, f'vendor_{j}_select', False)), None)
            if not selected_index:
                continue

            qc_data = self.env['ct.quotation.comparison.line'].search_read(
                [('id', '=', line.id)],
                [f'vendor_{selected_index}_qs_line_id', f'vendor_{selected_index}_price',
                 f'vendor_{selected_index}_discount', f'vendor_{selected_index}_discount_amt']
            )

            if not qc_data:
                continue

            qs_line_id = qc_data[0].get(f'vendor_{selected_index}_qs_line_id')
            qs_line_rec = self.env['ct.quotation.submit.line'].browse(qs_line_id)

            self.env['ct.vendor.price.list'].search([
                ('vendor_id', '=', qs_line_rec.header_id.vendor_id.id),
                ('product_id', '=', qs_line_rec.product_id.id),
                ('brand_id', '=', qs_line_rec.brand_id.id),
                ('uom_id', '=', qs_line_rec.uom_id.id)
            ]).write({
                'status': 'expired',
                'expiry_remark': 'Comparison has been revised, status changed to expired'
            })

            comparison_date = self.entry_date.strftime('%d/%m/%Y')
            price_list_vals = {
                'qc_id': self.id,
                'ref_no': qs_line_rec.header_id.quotation_ref_no,
                'entry_date': qs_line_rec.header_id.quotation_ref_date,
                'vendor_id': qs_line_rec.header_id.vendor_id.id,
                'vendor_name': qs_line_rec.header_id.vendor_name or '',
                'product_id': qs_line_rec.product_id.id,
                'description': qs_line_rec.description or '',
                'brand_id': qs_line_rec.brand_id.id,
                'uom_id': qs_line_rec.uom_id.id,
                'unit_price': qs_line_rec.unit_price,
                'discount': qs_line_rec.disc_per,
                'discount_amt': qs_line_rec.disc_amt,
                'source': 'comparison',
                'is_validity': qs_line_rec.header_id.is_validity,
                'validity_period_days': qs_line_rec.header_id.validity_period_days if qs_line_rec.header_id.is_validity == 'limit' else 0,
                'validity_period': qs_line_rec.header_id.validity_period if qs_line_rec.header_id.is_validity == 'limit' else 0,
                'validity_date': qs_line_rec.header_id.validity_date if qs_line_rec.header_id.is_validity == 'limit' else False,
                'status': 'approved',
                'entry_mode': 'auto',
                'payment_term_id': qs_line_rec.header_id.payment_term_id.id,
                # 'delivery_term_id': qs_line_rec.header_id.delivery_term_id.id,
                'freight_type': qs_line_rec.header_id.freight_type,
                'other_charges': qs_line_rec.header_id.other_charges_type or 0.0,
                'warranty': qs_line_rec.header_id.warranty or '',
                'price': qs_line_rec.header_id.price or '',
                'is_warranty': qs_line_rec.is_warranty,
                'warranty_category': qs_line_rec.warranty_category,
                'currency_id': qs_line_rec.header_id.currency_id.id,
                'warranty_period': qs_line_rec.warranty_period or 0.0,
                'days': qs_line_rec.days or 0,
                'warranty_date': qs_line_rec.warranty_date or False,
                'warranty_to_date': qs_line_rec.warranty_to_date or False,
                'comparison_ref_no': f"{self.name}-{comparison_date}",
                # 'tax_group_id': qs_line_rec.tax_group_id.id,
                'tax_ids': [(6, 0, qs_line_rec.tax_ids.ids)],
                'bill_type': qs_line_rec.header_id.bill_type or False,
                'warranty_from': qs_line_rec.warranty_from or '',
                'confirm_user_id': self.env.user.id,
                'confirm_date': fields.Datetime.now(),
                'ap_rej_user_id': self.env.user.id,
                'ap_rej_date': fields.Datetime.now(),
                'comparison_status': 'verified',
                'supplier_count': len(self.qs_details),
                'more_lp_remark': self.more_lp_remark
            }
            price_list_rec = self.env['ct.vendor.price.list'].create(price_list_vals)

            if qs_line_rec.header_id.line_ids_b:
                expense_vals = [{
                    'header_id': price_list_rec.id,
                    'expense_id': exp.expense_id.id,
                    'amt': exp.amt,
                    'disc_amt': exp.disc_amt,
                    'disc_per': exp.disc_per,
                    'tax_ids': [(6, 0, exp.tax_ids.ids)],
                    'description': exp.description
                } for exp in qs_line_rec.header_id.line_ids_b]

                self.env['ct.vendor.price.list.expenses.line'].create(expense_vals)


    def update_record(self):
        self.calculate_total()


    def calculate_total(self):
        vendors = ["vendor_1", "vendor_2", "vendor_3", "vendor_4"]
        for vendor in vendors:
            setattr(self, f"{vendor}_total_amt", "")
            setattr(self, f"{vendor}_other_amt", "")
            setattr(self, f"{vendor}_discount_amt", "")
            setattr(self, f"{vendor}_tax_amt", "")
            setattr(self, f"{vendor}_taxable_amt", "")
            # setattr(self, f"{vendor}_subtotal", "")
            setattr(self, f"{vendor}_net_amt", "")

        if self.line_ids:
            # for qc_line in self.line_ids:
            #     qc_line.calculate_subtotal()

            for vendor in vendors:
                price_attr = f"{vendor}_price"
                value_attr = f"{vendor}_value"
                discount_attr = f"{vendor}_discount"
                amt_attr = f"{vendor}_amt"
                subtotal_attr = f"{vendor}_subtotal"
                tax_amt_attr = f"{vendor}_tax_amt"
                round_off_attr = f"{vendor}_round_off_amt"
                
                if any(getattr(line, price_attr, 0) for line in self.line_ids):
                    total_amt = sum(getattr(line, price_attr, 0) * line.qty for line in self.line_ids if getattr(line, value_attr, 0))
                    other_amt = sum(getattr(line, amt_attr, 0) for line in self.line_expense_ids_a)
                    other_subtotal = sum(getattr(line, subtotal_attr, 0) for line in self.line_expense_ids_a)
                    other_tax_amt = sum(getattr(line, tax_amt_attr, 0) for line in self.line_expense_ids_a)
                    other_dis_amt = sum(getattr(line, amt_attr, 0) * (getattr(line, discount_attr, 0) / 100) for line in self.line_expense_ids_a)
                    discount_amt = sum((getattr(line, price_attr, 0) * line.qty) * (getattr(line, discount_attr, 0) / 100) for line in self.line_ids) + other_dis_amt
                    tax_amt = sum(getattr(line, tax_amt_attr, 0) for line in self.line_ids) + other_tax_amt
                    taxable_amt = round((total_amt + other_amt) - (discount_amt + other_dis_amt), 2)
                    subtotal = sum(getattr(line, value_attr, 0) for line in self.line_ids) + other_subtotal
                    net_amt = subtotal + getattr(self, round_off_attr, 0)
                    
                    setattr(self, f"{vendor}_total_amt", total_amt)
                    setattr(self, f"{vendor}_other_amt", other_amt)
                    setattr(self, f"{vendor}_discount_amt", discount_amt)
                    setattr(self, f"{vendor}_tax_amt", tax_amt)
                    setattr(self, f"{vendor}_taxable_amt", taxable_amt)
                    # setattr(self, f"{vendor}_subtotal", subtotal)
                    setattr(self, f"{vendor}_net_amt", net_amt)

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
        return super(CtQuotationComparison, self).write(vals)

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

        ct_trans = self.env[CT_QUOTATION_COMPARISON]
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
        # result['all_today_value'] = self.value_readable_format(sum(ct_trans.search([('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        # result['my_today_value'] = self.value_readable_format(sum(ct_trans.search([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())]).mapped('net_amt')))
        # max_transaction = max(ct_trans.search([('crt_date', '>=', fields.Date.today()), ('status', '=', 'approved')]), 
        #               key=lambda t: t.net_amt, default=None)
        # result['today_highest_tot'] = self.value_readable_format(max_transaction.net_amt) if max_transaction else 0
        # result['ref_no'] = max_transaction.name if max_transaction else '-'

        return result
