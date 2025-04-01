# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError
from collections import defaultdict
from functools import partial

CT_PIPO_ENTRY = 'ct.pipo.entry'
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

class CtPiPoEntry(models.Model):
    _name = 'ct.pipo.entry'
    _description = 'PI - PO Creation'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Doc No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    department_id = fields.Many2one('cm.department', string="Department", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)], tracking=True)
    department_id_name = fields.Char(string="Department Name", related = 'department_id.name',store = True)
    pr_line_ids = fields.Many2many('ct.purchase.request.line', string="Purchase Request", ondelete='cascade', domain="[('status', '=', 'approved'),('header_id.active_trans', '=', True),('header_id.department_id', '=', department_id)]")
    line_count = fields.Integer(string="Line Count", compute="_compute_all_line", store=True)
    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    pr_no = fields.Char('PR No', readonly=True)

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

    line_ids_a = fields.One2many('ct.pipo.entry.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.pipo.entry.supplier.details.line', 'header_id', string="PO Preview", copy=True, c_rule=True)

    @api.depends('pr_line_ids')
    def _compute_all_line(self):
        for rec in self:
            rec.line_count =  len(rec.pr_line_ids)

    @api.onchange('pr_line_ids')
    def onchange_pr_line_ids(self):
        self.pr_no = ",".join(sorted({line.header_id.name for line in self.pr_line_ids}))

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
        if not self.pr_line_ids:
            warning_msg.append("System not allow to confirm/approve with empty purchase request details")
        for sup_line in self.line_ids_b:
            if not sup_line.supplier_id:
                warning_msg.append(_(f"Warning! Please map the supplier in the supplier details for the product: {sup_line.product_id.name}"))
            elif sup_line.supplier_id.status != 'approved':
                warning_msg.append(_(f"Warning! The price list has expired for the mapped supplier: {sup_line.vendor_id.name}. Please map a different supplier and proceed"))        

        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': 'ct.pipo.entry.draft',
            'approve': CT_PIPO_ENTRY
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
            self.supplier_preview()
            # if not self.draft_name:
            #     sequence_id = self.env[IR_SEQUENCE].search(
            #             [('code', '=', 'ct.pipo.entry.draft')], limit=1)
            #     if sequence_id:
            #         self.env.cr.execute(
            #             """select generatesequenceno(%s,%s,%s,%s,%s,%s) """,
            #             (sequence_id.id,
            #              sequence_id.code,
            #              self.draft_date,
            #              None,
            #              None,
            #              ''))
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

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_PIPO_ENTRY)], limit=1)
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
            self.purchase_order_creation()
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

    def supplier_preview(self):
        if self.status in ('draft', 'wfa'):
            self.line_ids_b.unlink()
            vendor_price_list = self.env['ct.vendor.price.list']
            for line in self.pr_line_ids:
                domain = [
                    ('product_id', '=', line.product_id.id),
                    ('brand_id', '=', line.brand_id.id),
                    ('status', '=', 'approved'),
                    ('active_trans', '=', True)
                ]
                price_list_rec = vendor_price_list.search(domain)
                if price_list_rec:
                    values = [{'header_id': self.id, 'product_id': line.product_id.id, 'brand_id':line.brand_id.id, 'supplier_id': price_list_rec.id} 
                            if len(price_list_rec) == 1 
                            else {'header_id': self.id, 'product_id': line.product_id.id, 'brand_id':line.brand_id.id} 
                        ]
                    
                    self.line_ids_b.create(values)

    def purchase_order_creation(self):

        records = []

        for pr_line in self.pr_line_ids:
            price_list = self.env['ct.vendor.price.list'].search([
                ('product_id', '=', pr_line.product_id.id),
                ('status', '=', 'approved'),
                ('active_trans', '=', True)
            ])

            for pl_rec in price_list:
                supplier_products = {
                    sup.product_id.id
                    for sup in self.env['ct.pipo.entry.supplier.details.line'].search([
                        ('product_id', '=', pr_line.product_id.id),
                        ('supplier_id', 'in', [p_id.id for p_id in pl_rec]),
                        ('header_id.status', '=', 'wfa')
                    ])
                }
                if pl_rec.product_id.id in supplier_products or len(price_list) == 1:
                    vendor_price_list = self.env['ct.vendor.price.list'].search([
                        ('id', 'in', [sup_rec.supplier_id.id for sup_rec in self.line_ids_b]),
                        ('status', '=', 'approved'),
                        ('vendor_id', '=', pl_rec.vendor_id.id)
                    ])
                    
                    quotation_refs = list(set(vender_rec.ref_no for vender_rec in vendor_price_list))

                    records.append({
                        'company_id': self.company_id.id,
                        'department_id': self.department_id.id,
                        'entry_type': 'from_pi',
                        'vendor_id': pl_rec.vendor_id.id,
                        'currency_id': pl_rec.currency_id.id,
                        'quotation_ref_no': ', '.join(map(str, quotation_refs)),
                        'quotation_ref_date': pl_rec.entry_date,
                        'bill_type': pl_rec.bill_type,
                        'payment_term_id': pl_rec.payment_term_id.id or None,
                        'pr_line_ids': pr_line,
                    })

        if not records:
            return

        id2record = defaultdict(partial(defaultdict, list))

        for record in records:
            merged_record = id2record[record['vendor_id']]
            for key, value in record.items():
                merged_record[key].append(value)

        result = []
        for record in id2record.values():
            cleaned_record = {}
            for key, value in record.items():
                if isinstance(value, list) and len(set(value)) == 1:  
                    cleaned_record[key] = value[0]
                else:
                    cleaned_record[key] = value
            result.append(cleaned_record)

        for res in result:
            vendor = self.env['cm.vendor.master'].browse(res['vendor_id'])
            if vendor:
                address_parts = [
                    vendor.street,
                    vendor.street1,
                    vendor.city_id.name,
                    vendor.state_id.name,
                    vendor.country_id.name
                ]
                address = ", ".join(filter(None, address_parts))
            else:
                address = ''

            po_rec = self.env['ct.purchase.order'].create({
                'entry_type':'from_pi',
                'currency_id': res['currency_id'],
                'company_id': self.company_id.id,
                'department_id': self.department_id.id,
                'vendor_id': res['vendor_id'],
                'address': address,
                'quotation_ref_no': res['quotation_ref_no'],
                'quotation_ref_date': res['quotation_ref_date'][0] if isinstance(res['quotation_ref_date'], list) else res['quotation_ref_date'],
                'bill_type':res['bill_type'],
                'payment_term_id': res['payment_term_id'] or None,
                'pr_line_ids': [(6, 0, [x.id for x in res['pr_line_ids']])],
                'entry_mode': 'auto',
            })
            po_rec.write({'user_id': self.user_id.id})
            po_rec.save_record()

            for line in po_rec.line_ids:
                pricelist = self.env['ct.vendor.price.list'].search([
                    ('product_id', '=', line.product_id.id),
                    ('brand_id', '=', line.brand_id.id),
                    ('status', '=', 'approved'),
                    ('active_trans', '=', True),
                    ('vendor_id', '=', res['vendor_id'])
                ])
                
                if pricelist:
                    supplier_products = {
                        sup.product_id.id for sup in self.env['ct.pipo.entry.supplier.details.line'].search([
                            ('product_id', '=', line.product_id.id),
                            ('supplier_id', 'in', [p_id.id for p_id in pricelist])
                        ])
                    }
                    
                    for pricelist_rec in pricelist:
                        if pricelist_rec.product_id.id in supplier_products or len(pricelist) == 1:
                            line.write({
                                'brand_id': pricelist_rec.brand_id.id
                            })

                        comp_id = self.env['ct.quotation.comparison'].search([
                            ('id', '=', pricelist_rec.qc_id)
                        ])
                        line.qc_id = comp_id.id

                        brand_id = (
                            line.pr_line_id.brand_id.id
                            if line.pr_line_id and line.pr_line_id.brand_id.id
                            else pricelist_rec.brand_id.id if pricelist_rec.brand_id.id else False
                        )
                        line.write({'brand_id': brand_id})

                        add_charges = [
                            (0, 0, {
                                'expense_id': add.expense_id.id,
                                'description': add.description,
                                'amt': add.amt,
                                'disc_per': add.disc_per,
                                'disc_amt': add.disc_amt,
                                'tax_ids': [(6, 0, [tax.id for tax in add.tax_ids])],
                                'tax_amt': add.tax_amt,
                                'line_tot_amt': add.line_tot_amt,
                            })
                            for add in pricelist_rec.line_ids_b
                        ]

                        if add_charges:
                            po_rec.write({'line_ids_b': add_charges})


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
        return super(CtPiPoEntry, self).write(vals)

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

        ct_nocost_trans = self.env[CT_PIPO_ENTRY]
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
