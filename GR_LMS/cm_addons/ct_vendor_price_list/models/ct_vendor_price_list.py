# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime, timedelta
from odoo.exceptions import UserError

CT_VENDOR_PRICE_LIST = 'ct.vendor.price.list'
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
    ('expired', 'Expired')]

MODE_OF_PURCHASE = [('direct', 'Direct'),
                    ('online', 'Online')]

SOURCE = [('price_list', 'Price List'),
          ('comparison', 'Comparison')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

VALIDITY_SELECTION = [('limit', 'Limited'), ('no_limit', 'No Limit')]

FREIGHT_TYPE = [('inclusive', 'Inclusive'),
                ('extra_by_supplier', 'Extra By Supplier'), 
                ('extra_at_our_cost', 'Extra at our Cost'),
                ('extra_by_company', 'Extra By Company')]

MODE_OF_PAYMENT = [('cash', 'Cash'),
                   ('credit', 'Credit'),
                   ('credit_card', 'Credit Card'),
                   ('not_applicable', 'Not Applicable')]

PRICE_TERMS = [('inclusive', 'Inclusive of all Tax and Duties'),
               ('exclusive', 'Exclusive of all Tax an Duties')]

WARRANTY_FROM = [('from_grn', 'From GRN Date'),
                 ('from_invoice', 'From Sup Invoice Date'),
                 ('custom', 'Custom / MFG Date')]

WARRANTY_CATEGORY = [('limited', 'Limited'), ('perpetual', 'Perpetual/Life Time')]

OTHER_CHARGES = [('inclusive', 'Inclusive'), ('exclusive', 'Exclusive')]

WARRANTY=[('applicable','Applicable'), ('not_applicable','Not Applicable')]

class CtVendorPriceList(models.Model):
    _name = 'ct.vendor.price.list'
    _description = 'Price List'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'
    _rec_name = 'vendor_id'

    name = fields.Char(string="Name", readonly=True, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    expiry_remark = fields.Text(string="Expiry Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    
    ref_no = fields.Char(string="Ref No")
    mode_of_purchase = fields.Selection(selection=MODE_OF_PURCHASE, string="Mode Of Purchase", default='direct', copy=False, tracking=True)
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_name = fields.Char(string="Vendor Name")
    source = fields.Selection(selection=SOURCE, string="SOURCE", copy=False, tracking=True)
    product_id = fields.Many2one('product.template', string="Product Name", index=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], ondelete='restrict')
    description = fields.Char(string="Description", size=252)
    brand_id = fields.Many2one('cm.master', string="Brand", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    uom_id = fields.Many2one('uom.uom', string="UOM", copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    unit_price = fields.Float(string="Unit Price")
    # modify = fields.Char(compute='_get_modify',
    #     string='Modify',
    #     store=True,
    #     size=10,
    #     default='no')

    discount = fields.Float(string="Discount (%)", digits=(12, 2))
    discount_amt = fields.Float(string="Discount Amount", digits=(12, 2))
    is_validity = fields.Selection(VALIDITY_SELECTION, string="Validity", default='no_limit')
    validity_period = fields.Integer("Validity Period(Months)")
    validity_period_days = fields.Integer("Validity Period(Days)",default=0)
    validity_date = fields.Date("Validity Date")
    source = fields.Selection(SOURCE, "Source", default='price_list')
    qc_id = fields.Integer("Source ID")
    tax_group_id = fields.Many2one('account.tax.group', string="Tax Group" , copy=False, ondelete='restrict', tracking=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    tax_ids = fields.Many2many('account.tax', 'price_list_line_tax', 'price_list_id', 'tax_id', string="Taxes", ondelete='restrict', check_company=True, domain=[('status', '=', 'active'),('active_trans', '=', True)], c_rule=True)
    warranty_period = fields.Float(string="Warranty Period(Months)", digits=(12, 2))
    days = fields.Integer(string="Days")
    warranty_date = fields.Date(string="Warranty From Date")
    warranty_to_date = fields.Date(string="Warranty To Date", readonly=True)   
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    # delivery_term_id = fields.Many2one(
    #     'kg.delivery.master', 'Delivery Term', domain=[
    #         ('active_trans', '!=', False), ('state', '=', 'approved')])
    freight_type = fields.Selection(selection=FREIGHT_TYPE, string="Freight")
    warranty = fields.Char(string="Warranty")
    bill_type = fields.Selection(MODE_OF_PAYMENT, string="Mode of Payment", default='credit')
    price = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive')
    more_lp_remark = fields.Text(string="More LP Remarks")                      
    currency_id = fields.Many2one('res.currency', store=True)
    is_warranty = fields.Selection(selection=WARRANTY, string="Is Warranty")
    warranty_from = fields.Selection(selection=WARRANTY_FROM, string="Warranty From")
    warranty_category = fields.Selection(selection=WARRANTY_CATEGORY, string="Warranty Category")
    comparison_ref_no = fields.Char(string="Comparison No")
    other_charges = fields.Selection(selection=OTHER_CHARGES, string="Other Charges")

    comparison_status = fields.Selection([('approved','Approved'),('verified','Verified')], 'Comparison Status',default = 'verified',readonly=True)
    supplier_count = fields.Integer('Supplier Count',readonly=True)

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
    expiry_user_id = fields.Many2one(RES_USERS, string="Expired Date", copy=False, ondelete='restrict', readonly=True)
    expiry_date = fields.Datetime(string="Expired By", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids_a = fields.One2many('ct.transaction.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.vendor.price.list.expenses.line', 'header_id', string="Other Charges", copy=True, c_rule=True)

    @api.onchange('vendor_id')
    def onchange_vendor_id(self):
        if self.vendor_id:
            self.vendor_name = self.vendor_id.name
            self.currency_id = self.vendor_id.currency_id.id

    @api.onchange('is_warranty')
    def change_is_warranty(self):
        self.warranty_period = False
        self.warranty_from = False
        self.warranty_category = False
    
    @api.onchange('warranty_category')
    def change_warranty_category(self):
        if self.warranty_category:
            self.warranty_from = False
            self.warranty_period = False
            self.days = False
            self.warranty_date = False
            self.warranty_to_date = False
    
    @api.onchange('warranty_from')
    def change_warranty_from(self):
        if self.warranty_from:
            self.warranty_period = False
            self.days = False
            self.warranty_date = False
            self.warranty_to_date = False

    @api.onchange('is_validity')
    def change_is_validity(self):
        if self.is_validity:
            self.validity_period = False
            self.validity_period_days = False
            self.validity_date = False

    @api.onchange('entry_date', 'validity_period', 'validity_period_days')
    def onchange_validity_date(self):
        if self.entry_date and self.validity_period:
            entry_date = fields.Date.from_string(self.entry_date)
            validity_date = entry_date + timedelta(days=int(self.validity_period) * 30) + timedelta(days=int(self.validity_period_days))
            self.validity_date = validity_date


    @api.onchange('warranty_date', 'warranty_period', 'days')
    def onchange_warranty_days(self):
        if self.warranty_date and self.warranty_period:
            warranty_date = fields.Date.from_string(self.warranty_date)
            warranty_end_date = warranty_date + timedelta(days=self.warranty_period * 30) - timedelta(days=1)            
            if self.days:
                warranty_end_date += timedelta(days=self.days)
            self.warranty_to_date = warranty_end_date

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
        else:
            self.uom_id = False

    # @api.onchange('tax_group_id')
    # def onchange_tax_group_id(self):
    #     if self.tax_group_id:
    #         tax_ids = self.env['account.tax'].search([
    #             ('tax_group_id', '=', self.tax_group_id.id),
    #             ('status', '=', 'active'),
    #             ('active_trans', '=', True)
    #         ], limit=100).ids
    #         self.tax_ids = [(6, 0, tax_ids)]


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


    def validations(self, **kw):
        warning_msg = []
        if self.status in ('draft', 'wfa'):
            self.validate_expense_lines(warning_msg)
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    # def sequence_no_validations(self, **kw):
    #     warning_msg = []
    #     action_code_map = {
    #         'confirm': 'ct.vendor.price.list.draft',
    #         'approve': CT_VENDOR_PRICE_LIST
    #     }

    #     action = kw.get('action')
    #     if action in action_code_map:
    #         sequence_code = action_code_map[action]
    #         sequence_id = self.env[IR_SEQUENCE].search([('code', '=', sequence_code)], limit=1)
    #         if not sequence_id:
    #             warning_msg.append("The ir sequence has not been created.")
    #     if kw.get('date'):
    #         self.env.cr.execute(
    #             """select value from ir_config_parameter 
    #             where key = 'custom_properties.seq_num_reset' 
    #             order by id desc limit 1;
    #         """)
    #         seq_reset = self.env.cr.fetchone()
    #         if not seq_reset or not seq_reset[0]:
    #             warning_msg.append("The sequence number reset option has not been configured in the custom settings.")
    #         elif seq_reset[0] == 'fiscal_year':
    #             fiscal_year = self.env['cm.fiscal.year'].search([
    #                             ('from_date', '<=', kw.get('date')),('to_date', '>=', kw.get('date')),
    #                             ('status', '=', 'active'),('active', '=', True)])
    #             if not fiscal_year:
    #                 warning_msg.append("The fiscal year has not been created.")

    #     return self.display_warnings(warning_msg, kw)

    @validation
    def entry_confirm(self):
        if self.status == 'draft':
            self.validations()

            # if not self.draft_name:
            #     sequence_id = self.env[IR_SEQUENCE].search(
            #             [('code', '=', 'ct.vendor.price.list.draft')], limit=1)
            #     if sequence_id:
            #         self.env.cr.execute(
            #             """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """,
            #             (sequence_id.id,
            #              sequence_id.code,
            #              self.draft_date,
            #              self.company_id.id,
            #              None,
            #              'company'))
            #         sequence = self.env.cr.fetchone()
            #         sequence = sequence[0]
            #     else:
            #         sequence = ''

            #     if not sequence:
            #         self.sequence_no_validations(date=self.draft_date, action='confirm')

            #     self.draft_name = sequence

            self.write({'status': 'wfa',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")

            # if not self.name:
            #     sequence_id = self.env[IR_SEQUENCE].search(
            #             [('code', '=', CT_VENDOR_PRICE_LIST)], limit=1)
            #     if sequence_id:
            #         self.env.cr.execute(
            #             """select generatesequenceno('%s','%s','%s',%s,%s,'%s') """,
            #             (sequence_id.id,
            #              sequence_id.code,
            #              self.entry_date,
            #              self.company_id.id,
            #              None,
            #              'company'))
            #         sequence = self.env.cr.fetchone()
            #         sequence = sequence[0]
            #     else:
            #         sequence = ''

            #     if not sequence:
            #         self.sequence_no_validations(date=self.entry_date, action='approve')

            #     self.name = sequence
            
            self.expiry_old_product()
            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

        return True
    
    def expiry_old_product(self):
        old_recs = self.env['ct.vendor.price.list'].search([
            ('id', '!=', self.id),
            ('product_id', '=', self.product_id.id),
            ('uom_id', '=', self.uom_id.id),
            ('vendor_id', '=', self.vendor_id.id),
            ('status', '!=', 'expired')
        ])
        old_recs.write({
            'status' : 'expired',
            'expiry_remark' : f"New price list has been added by {self.env.user.name} on {time.strftime('%d-%m-%Y %H:%M')} for the same supplier & product",
            'expiry_user_id': self.env.user.id,
            'expiry_date': time.strftime(TIME_FORMAT)
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

    def entry_expiry(self):
        if self.status == 'approved':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.expiry_remark or not self.expiry_remark.strip():
                raise UserError(_("Expiry remarks is must. Kindly enter the remarks in Expiry Remarks field"))
            if self.expiry_remark and len(self.expiry_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for expiry remarks"))
            self.write({'status': 'expired',
                        'expiry_user_id': self.env.user.id,
                        'expiry_date': time.strftime(TIME_FORMAT)
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
        return super(CtVendorPriceList, self).write(vals)

    def auto_expiry(self):
        expired_records = self.env['ct.vendor.price.list'].search([
            ('validity_date', '<=', fields.Date.today()),
            ('status', '=', 'approved'),
            ('is_validity', '=', 'limit')
        ])
        expired_records.write({
            'status': 'expired',
            'expiry_remark': 'Price list validity date is expired based on supplier quotation submission'
        })

        return True

    @api.model
    def retrieve_dashboard(self):
        result = {}

        ct_trans = self.env[CT_VENDOR_PRICE_LIST]
        result['all_draft'] = ct_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_trans.search_count([('status', '=', 'rejected')])
        result['all_expired'] = ct_trans.search_count([('status', '=', 'expired')])
        result['my_draft'] = ct_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_expired'] = ct_trans.search_count([('status', '=', 'expired'), ('user_id', '=', self.env.uid)])
        result['all_today_count'] = ct_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_trans.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_trans.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result