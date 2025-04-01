# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation,is_special_char
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_VENDOR_INVOICE = 'ct.vendor.invoice'
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

PAY_MODE_OPTIONS = [('cash', 'Cash'),
                    ('credit', 'Credit'),
                    ('credit_card', 'Credit Card')]

class CtVendorInvoice(models.Model):
    _name = 'ct.vendor.invoice'
    _description = 'Vendor Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Invoice No", copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Invoice Date", copy=False, default=fields.Date.today)
    bc_id = fields.Many2one('ct.business.confirmation', string="BC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])
    bc_date = fields.Date(string="BC Date", copy=False)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])

    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    address = fields.Char(string="Address", default=False)

    payment_mode = fields.Selection(selection=PAY_MODE_OPTIONS, string="Mode Of Payment", copy=False)
    due_date = fields.Date(string="Payment Due Date", copy=False)
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])


    tax_amt = fields.Float(string="Tax Amount", store=True, compute='_compute_all_line')	
    tot_amt = fields.Float(string="Total Amount", store=True, compute='_compute_all_line')	
    other_amt = fields.Float(string="Other Charges(+)", store=True, compute='_compute_all_line')
    disc_amt = fields.Float(string="Discount Amount(-)", store=True, compute='_compute_all_line')
    taxable_amt = fields.Float(string="Taxable Amount", store=True, compute='_compute_all_line')
    round_off_amt = fields.Float(string="Round Off Amount(+/-)", store=True, compute='_compute_all_line')	
    grand_tot_amt = fields.Float(string="Grand Total", store=True, compute='_compute_all_line')
    fixed_disc_amt = fields.Float(string="Fixed Discount Amount(-)", store=True, compute='_compute_all_line')
    net_amt = fields.Float(string="Net Amount", store=True, compute='_compute_all_line')
    manual_round_off = fields.Boolean(string="Apply Manual Round Off")

    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    currency_id = fields.Many2one('res.currency', string="Currency", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])

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

    line_ids_a = fields.One2many('ct.vendor.invoice.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_e = fields.One2many('ct.vendor.invoice.pri.details.line', 'header_id', string="Vendor Details", copy=True, c_rule=True)
    line_ids_f = fields.One2many('ct.vendor.invoice.advance.line', 'header_id', string="Advance", copy=True, c_rule=True)
    line_ids_g = fields.One2many('ct.vendor.invoice.tax.line', 'header_id', string="Tax Breakup", copy=True, c_rule=True)

    @api.depends('line_ids_e', 'round_off_amt', 'fixed_disc_amt', 'manual_round_off')
    def _compute_all_line(self):
        for data in self:            
            data._compute_footer_calculation()
            type_tax_use_dict = data._initialize_tax_dict()
            data._process_line_items(data.line_ids_e, type_tax_use_dict)
            data.line_ids_g = [(5, 0, 0)]
            tax_values = []
            for tx_name, tx_amt in type_tax_use_dict.items():
                if tx_amt > 0:
                    tax_values.append((0,0,{'tax_name':tx_name,'tax_amt':tx_amt}))
            data.line_ids_g = tax_values 

    def _compute_footer_calculation(self):
        for data in self:
            data.tot_amt = sum(data.line_ids_e.mapped('tot_amt'))
            data.taxable_amt = sum(data.line_ids_e.mapped('taxable_amt'))
            data.disc_amt = sum(data.line_ids_e.mapped('disc_amt'))
            
            old_grand_total = data.taxable_amt + data.tax_amt

            data.taxable_amt = (data.taxable_amt + data.other_amt) - data.disc_amt
            data.tax_amt = sum(data.line_ids_e.mapped('tax_amt'))

            if (old_grand_total != (data.taxable_amt + data.tax_amt)) or (not data.tot_amt):
                data.manual_round_off = False
                data.round_off_amt = 0.00
                data.fixed_disc_amt = 0.00
            
            if not data.manual_round_off:
                data.round_off_amt = round(data.taxable_amt + data.tax_amt) - (data.taxable_amt + data.tax_amt)
                data.round_off_amt = round(data.round_off_amt, 2)

            data.grand_tot_amt = data.tot_amt + data.round_off_amt
            
            data.fixed_disc_amt = 0.00 if data.grand_tot_amt <= 0 else data.fixed_disc_amt
            
            
            data.net_amt = (data.grand_tot_amt) - data.fixed_disc_amt

    def _initialize_tax_dict(self):
        return {
            record['name']: 0
            for record in self.env['account.tax.group'].read_group([], ['name'], ['name'])
        } 

    def _process_line_items(self, line_items, tax_dict):
        for line in line_items:
            if line.unit_price > 0:
                for tax_line in line.tax_ids:
                    self._process_tax_line(line, tax_line, line.unit_price, line.qty, line.disc_per, line.tot_amt, tax_dict)

    def _process_tax_line(self, line, tax_line, price_unit, qty, discount, price_subtotal, type_tax_use_dict):

        tax_value_return = self.env['account.tax']._convert_to_tax_base_line_dict(
                                            self,
                                            partner=False,
                                            currency= line.currency_id,
                                            product=  False,
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

    @api.constrains('name')
    def name_validation(self):
        if self.name and self.vendor_id:
            if is_special_char(self.env, self.name):
                raise UserError(_("Special character is not allowed in invoice no field"))

            name = self.name.upper().replace(" ", "")
            self.env.cr.execute(""" select upper(name)
            from ct_vendor_invoice where upper(REPLACE(name, ' ', ''))  = '%s'
            and vendor_id = %s and id != %s""" %(name, self.vendor_id.id, self.id))
            if self.env.cr.fetchone():
                raise UserError(_("Invoice no must be unique"))

    @api.onchange('round_off_amt')
    def onchange_round_off_amt(self):
        if self.manual_round_off and self.entry_mode != 'auto':
            self.fixed_disc_amt = 0.00
            if self.round_off_amt > (self.taxable_amt + self.tax_amt):
                raise UserError(_("Round Off Amount should not be greater than Grand Total"))
            if self.round_off_amt < 0 and self.grand_tot_amt < 0:
                raise UserError(_("Round Off Amount should not be lesser than Grand Total"))


    @api.onchange('fixed_disc_amt')
    def onchange_fixed_disc_amt(self):
        if self.fixed_disc_amt  and self.entry_mode != 'auto':
            if self.fixed_disc_amt < 0:
                raise UserError(_("Fixed Discount Amount should not be lesser than zero"))
            if self.fixed_disc_amt > self.grand_tot_amt:
                raise UserError(_("Fixed Discount Amount should not be greater than Grand Total"))

    @api.onchange('line_ids_e')
    def onchange_currency_id(self):
        currency_ids = self.line_ids_e.mapped('currency_id.id')
        self.currency_id = currency_ids[0] if currency_ids else self.env.user.company_id.currency_id.id

    @api.onchange('bc_id')
    def onchange_bc_id(self):
        if self.bc_id:
            self.bc_date = self.bc_id.entry_date
            self.service_id = self.bc_id.service_id.id
        else:
            self.bc_date = False
            self.service_id = False

    @api.onchange('vendor_id')
    def onchange_vendor_id(self):
        if self.vendor_id:
            address = ", ".join(filter(None, [
                    self.vendor_id.street,
                    self.vendor_id.street1,
                    self.vendor_id.city_id.name,
                    self.vendor_id.state_id.name,
                    self.vendor_id.country_id.name,
                    self.vendor_id.pin_code
                ]))
            self.address = address
        else:
            self.address = False

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
        if self.entry_date < self.bc_date:
            warning_msg.append("Invoice date should not be lesser than bc date.")
        if not self.line_ids_e:
            warning_msg.append("System not allow to confirm or approve without charges details.")
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

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

            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            self.flexi_vendor_invoice_mail_data_design(
                trans_rec = self,
                mail_queue_name = 'Flexi Vendor Invoice Approve Mail',
                subject = f"#vendor-invoice-approved# {self.service_id.name} - {self.bc_id.name}",
                mail_config_name = 'Flexi Vendor Invoice Approve Mail'
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
        return super(CtVendorInvoice, self).write(vals)

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_VENDOR_INVOICE].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def flexi_vendor_invoice_mail_data_design(self, **kw):
        self.env.cr.execute(
                "SELECT ctm_flexi_vendor_invoice_approve_mail(%s, %s, %s, %s, %s)",
                (self.id, self.status, self.name, self.env.user.partner_id.name, '')
            )
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
                mail_type=mail_type, model_name=CT_VENDOR_INVOICE, mail_name=mail_config_name)

            email_to = ", ".join(set(default_to + vals.get('email_to', []))) if default_to or vals.get('email_to') else ''
            email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
            email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
            email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''

            self.env['cp.mail.queue'].create_mail_queue(
                name = mail_queue_name, trans_rec = trans_rec, mail_from = email_from,
                email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                subject = subject, body = data[0][0], attachment=False)

        return True

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

        ct_trans = self.env[CT_VENDOR_INVOICE]
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
        result['all_month_count'] = ct_trans.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_trans.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
