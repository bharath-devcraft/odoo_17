# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_QUOTATION_SUBMIT = 'ct.quotation.submit'
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

BILL_TYPE =  [('cash','Cash'),
              ('credit','Credit'),
              ('credit_card','Credit Card'),
              ('not_applicable','Not Applicable')]
              
VALIDITY_SELECTION = [('limit', 'Limited'), ('no_limit', 'No Limit')]

IS_WARRANTY = [('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')]
WARRANTY_CATEGORY = [('limited', 'Limited'), ('perpetual', 'Perpetual/Life Time')]
RFQ_MODE = [('pi','PI'),('si','SI')]
WARRANTY_FROM = [('from_grn', 'From GRN Date'),
                 ('from_invoice', 'From Sup Invoice Date'),
                 ('custom', 'Custom / MFG Date')]                     


FREIGHT_TYPE = [('inclusive', 'Inclusive'),
           ('extra_by_supplier', 'Extra By Supplier'), 
           ('extra_at_our_cost', 'Extra at our Cost'),
           ('extra_by_company', 'Extra By Company')]

OTHER_CHARGES_TYPE = [('inclusive', 'Inclusive'), ('exclusive', 'Exclusive')]
PRICE_TERMS = [('inclusive', 'Inclusive of all Tax and Duties'),
               ('exclusive', 'Exclusive of all Tax an Duties')]


class CtQuotationSubmit(models.Model):
    _name = 'ct.quotation.submit'
    _description = 'Quotation Submit'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Quotation Submit No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Quotation Submit Date", copy=False, default=fields.Date.today)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    line_count = fields.Integer(string="Line Count", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", copy=False, default=lambda self: self.env.company.currency_id.id, ondelete='restrict', readonly=True, tracking=True)
    due_date = fields.Date(string="Validity Date", copy=False, tracking=True)
    
    ## New Fields 
    rfq_id = fields.Many2one('ct.rfq', string="RFQ No", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    rfq_name = fields.Char(string="RFQ Name", c_rule=True)
    vendor_name = fields.Char(string="Vendor Name", c_rule=True)
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", index=True, ondelete='restrict')
    vendor_address = fields.Text(string="Vendor Address", copy=False)    
    quotation_ref_no = fields.Char(string="Quotation Ref No", copy=False)
    quotation_ref_date = fields.Date(string="Quotation Ref Date", copy=False)    
    bill_type = fields.Selection(selection=BILL_TYPE, string="Mode of Payment", copy=False, default="credit", readonly=True, tracking=True)
    
    line_total = fields.Float(string="Total", copy=False, default=0, readonly=True, store=True, compute='_compute_all_line')
    is_compared = fields.Boolean(string="Compared", copy=False, store=True, compute='_compute_all_line')
    
    is_warranty = fields.Selection(selection=IS_WARRANTY, string="Warranty", copy=False, tracking=True)
    warranty_category = fields.Selection(selection=WARRANTY_CATEGORY, string="Warranty Category", copy=False, tracking=True)
    warranty_from = fields.Selection(selection=WARRANTY_FROM, string="Warranty From", copy=False, tracking=True)     
    warranty_period = fields.Float(string="Warranty Period(Months)",digits=(12,2), copy=False)
    warranty_date = fields.Date(string="Warranty From Date", copy=False)
    warranty_to_date = fields.Date(string="Warranty To Date", readonly=True, copy=False)
    days = fields.Integer(string="Days", copy=False)    
    
    is_validity = fields.Selection(selection=VALIDITY_SELECTION, string="Price Validity Range", copy=False)
    validity_period = fields.Integer(string="Validity Period(Months)", copy=False)
    validity_period_days = fields.Integer(string="Validity Period(Days)", copy=False)
    validity_date = fields.Date(string="Validity Date", copy=False)
    rfq_mode = fields.Selection(selection=RFQ_MODE, string="RFQ Mode",default="pi", copy=False, tracking=True)    
    
    payment_term_id = fields.Many2one('cm.payment.term', string="Payment Term", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    freight_type = fields.Selection(selection=FREIGHT_TYPE, string="Freight", copy=False)
    other_charges_type = fields.Selection(selection=OTHER_CHARGES_TYPE, string="Other Charges", copy=False)
    price = fields.Selection(selection=PRICE_TERMS, string="Price", default='inclusive')
    warranty = fields.Char(string="Warranty", copy=False)
    specification = fields.Text(string="Specification", copy=False)
    
    
    ##END

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

    line_ids = fields.One2many('ct.quotation.submit.line', 'header_id', string="Details", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.quotation.submit.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.quotation.submit.expenses.line', 'header_id', string="Other Charges", copy=True, c_rule=True)

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
                    detail_line.uom_id.id, 
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
            'approve': CT_QUOTATION_SUBMIT
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
            data.line_total = sum(line.line_tot_amt for line in data.line_ids) + sum(line.line_tot_amt for line in data.line_ids_b)
            data.is_compared = all(line.is_compared for line in data.line_ids)
            data.write({'is_compared': True}) if data.is_compared else None

    @api.onchange('partner_id')
    def onchange_supplier(self):
        if self.partner_id:
            self.address = self.partner_id.street

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

        return True

    @validation
    def entry_approve(self):
        if self.status == 'wfa':
            self.validations(action="approve")           
            
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
        return super(CtQuotationSubmit, self).write(vals)

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

        ct_quotation_submit = self.env[CT_QUOTATION_SUBMIT]
        result['all_draft'] = ct_quotation_submit.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_quotation_submit.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_quotation_submit.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_quotation_submit.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_quotation_submit.search_count([('status', '=', 'cancelled')])
        result['my_draft'] = ct_quotation_submit.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_quotation_submit.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_quotation_submit.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_quotation_submit.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_quotation_submit.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_quotation_submit.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_quotation_submit.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_quotation_submit.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_quotation_submit.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
