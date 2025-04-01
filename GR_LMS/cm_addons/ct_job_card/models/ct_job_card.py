# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

CT_JOB_CARD = 'ct.job.card'
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
    ('cancelled', 'Cancelled'),
    ('closed', 'Closed')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

NATURE_OF_JOB =  [('container_survey','Container Survey'),
                  ('loading', 'Loading'),
                  ('unloading', 'Unloading'),
                  ('cross_loading', 'Cross Loading'),
                  ('disposal_assistance', 'Disposal Assistance'),
                  ('expiry_audit', 'Expiry Audit')]

SERVICE_PROVIDER =  [('internal','Internal'),
                     ('external', 'External')]

AVAILABLE_LOCATION =  [('own_warehouse','Own Warehouse'),
                       ('customer_place', 'Customer Place')]

AUDIT_RESULT =  [('reusable','Reusable'),
                 ('non_reusable', 'Non-Reusable')]

class CtJobCard(models.Model):
    _name = 'ct.job.card'
    _description = 'Job Card'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="JC No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="JC Date", copy=False, default=fields.Date.today)

    bc_id = fields.Many2one('ct.business.confirmation', string="BC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True),('issue_status', '=', 'pending'),('invoice_status', '=', 'pending')])
    bc_date = fields.Date(string="BC Date", copy=False)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    nature_of_job = fields.Selection(selection=NATURE_OF_JOB, string="Nature of Job", copy=False)
    service_provider = fields.Selection(selection=SERVICE_PROVIDER, string="Service Provider", copy=False)
    bcc_date = fields.Date(string="BCC Date", copy=False, help="Best Case Completion")

    customer_id = fields.Many2one('cm.customer', string="Customer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    service_address = fields.Char(string="Service Address", default=False)
    service_date = fields.Date(string="Service Date", copy=False)

    emp_id = fields.Many2one('cm.employee', string="Service Engineer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])

    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)

    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    contact_person = fields.Char(string="Contact Person", size=50)

    available_loc = fields.Selection(selection=AVAILABLE_LOCATION, string="Available Location", copy=False)
    dc_id = fields.Many2one('ct.delivery.challan', string="DC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])
    audit_date = fields.Date(string="Audit Date", copy=False)
    audit_eng_id = fields.Many2one(RES_USERS, string="Audit Engineer", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    flexi_bag_id = fields.Many2one('product.template', string="Bag Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_bag')])
    serial_no = fields.Char(string="Serial No", copy=False)
    mfg_date = fields.Date(string="Mfg Date", copy=False)
    expiry_date = fields.Date(string="Expiry Date", copy=False)
    audit_result = fields.Selection(selection=AUDIT_RESULT, string="Audit Result", copy=False)
    extended_usage = fields.Integer(string="Extended Usage (Months)", copy=False)
    extended_expiry_date = fields.Date(string="Extended Expiry Date", copy=False)
    audit_address = fields.Char(string="Audit Address", default=False)
    exp_vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    exp_contact_person = fields.Char(string="Contact Person", size=50)
    exp_mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    exp_email = fields.Char(string="Email", copy=False, size=252)

    closer_remark = fields.Text(string="Closer Remarks", copy=False)
    closer_date = fields.Date(string="Closer Date", copy=False)

    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    combined_codes = fields.Char(string="Combined Codes", readonly=True)

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
    close_user_id = fields.Many2one(RES_USERS, string="Closed By", copy=False, ondelete='restrict', readonly=True)
    close_date = fields.Datetime(string="Closed Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids_a = fields.One2many('ct.job.card.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.job.card.bag.details.line', 'header_id', string="Bag Details", copy=True, c_rule=True)
    line_ids_d = fields.One2many('ct.job.card.container.details.line', 'header_id', string="Container Details", copy=True, c_rule=True)
    line_ids_e = fields.One2many('ct.job.card.checklist.line', 'header_id', string="Checklist Details", copy=True, c_rule=True)
    line_ids_f = fields.One2many('ct.job.card.expense.details.line', 'header_id', string="Expense Details", copy=True, c_rule=True)
    line_ids_g = fields.One2many('ct.job.card.advance.details.line', 'header_id', string="Advance Details", copy=True, c_rule=True)

    @api.onchange('bc_id')
    def onchange_bc_id(self):
        if self.bc_id:
            self.bc_date = self.bc_id.entry_date
            self.customer_id = self.bc_id.customer_id.id
            self.service_address = self.bc_id.cus_del_address
            self.service_id = self.bc_id.service_id.id
            self.exp_contact_person = self.bc_id.contact_person
            self.exp_mobile_no = self.bc_id.mobile_no
            self.exp_email = self.bc_id.email
        else:
            self.bc_date = False
            self.customer_id = False
            self.service_address = False
            self.service_id = False
            self.exp_contact_person = False
            self.exp_mobile_no = False
            self.exp_email = False

    @api.onchange('bc_id', 'nature_of_job')
    def onchange_bag_details_creation(self):
        self.line_ids_c = [(5, 0, 0)]
        if (self.bc_id and self.nature_of_job in 
            ('container_survey','loading','unloading','cross_loading','disposal_assistance')):

            line_ids_c = []
            for rec in self.bc_id.line_ids_c:
                if rec.pending_qty > 0:
                    domain = [
                        ('status', '=', 'active'),
                        ('active_trans', '=', True),
                        ('custom_type', '=', 'flexi_bag'),
                        ('flexi_type', '=', rec.flexi_type),
                        ('layer_type_id', '=', rec.flexi_layer_type_id.id),
                        ('capacity_id', '=', rec.flexi_capacity_id.id),
                    ]
                    if rec.vendor_id:
                        domain.append(('vendor_id', '=', rec.vendor_id.id))

                    flexi_bag_rec = self.env['product.template'].search(domain, limit=1)
                    if flexi_bag_rec:
                        line_ids_c.append((0, 0, {
                            'flexi_bag_id': flexi_bag_rec.id if flexi_bag_rec else False,
                            'uom_id': flexi_bag_rec.uom_id.id if flexi_bag_rec else False,
                            'vendor_id': rec.vendor_id.id if rec.vendor_id else False,
                            'qty': rec.pending_qty,
                        }))
            self.line_ids_c = line_ids_c

    @api.onchange('service_id')
    def onchange_service_ids(self):
        self.combined_codes = []
        if self.service_id:
            self.combined_codes = [self.service_id.sys_ref]

    @api.onchange('entry_date')
    def onchange_entry_date(self):
        if self.entry_date:
            days_added = 0
            two_working_days = self.entry_date
            while days_added < 2:
                two_working_days += timedelta(days=1)
                if two_working_days.weekday() < 5:
                    days_added += 1
            self.bcc_date = two_working_days
        else:
            self.bcc_date = False

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.nature_of_job == 'expiry_audit':
            if self.customer_id:
                self.exp_contact_person = self.customer_id.contact_person
                self.exp_mobile_no = self.customer_id.mobile_no
                self.exp_email = self.customer_id.email
            else:
                self.exp_contact_person = False
                self.exp_mobile_no = False
                self.exp_email = False

    @api.onchange('nature_of_job')
    def onchange_nature_of_job(self):
        self.bc_id = False
        self.customer_id = False
        self.exp_contact_person = False
        self.exp_mobile_no = False
        self.exp_email = False
        self.service_address = False
        self.service_date = False

        self.available_loc = False
        self.dc_id = False
        self.exp_vendor_id = False
        self.flexi_bag_id = False
        self.serial_no = False
        self.mfg_date = False
        self.expiry_date = False
        self.audit_date = False
        self.audit_eng_id = False
        self.audit_address = False
        self.audit_result = False

    @api.onchange('service_provider')
    def onchange_service_provider(self):
        self.emp_id = False
        self.vendor_id = False
        self.contact_person = False
        self.mobile_no = False
        self.email = False

    @api.onchange('emp_id')
    def onchange_emp_id(self):
        if self.emp_id:
            self.mobile_no = self.emp_id.mobile_no
            self.email = self.emp_id.email
        else:
            self.mobile_no = False
            self.email = False

    @api.onchange('vendor_id')
    def onchange_vendor_id(self):
        if self.vendor_id:
            self.contact_person = self.vendor_id.contact_person
            self.mobile_no = self.vendor_id.mobile_no
            self.email = self.vendor_id.email
        else:
            self.contact_person = False
            self.mobile_no = False
            self.email = False

    
    @api.onchange('audit_result', 'extended_usage', 'expiry_date')
    def onchange_find_extended_expiry_date(self):
        if self.audit_result == 'reusable' and self.expiry_date:
            self.extended_expiry_date = self.expiry_date + relativedelta(months=int(self.extended_usage if self.extended_usage else 0))
        else:
            self.extended_expiry_date = False
            self.extended_usage = False

    @api.onchange('available_loc')
    def onchange_available_loc(self):
        if self.available_loc and self.available_loc == 'own_warehouse':
            self.audit_address = 'Own Warehouse'
        else:
            self.audit_address = False

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
        if any(code in self.combined_codes for code in ('FLBS', 'FLAS')) and not self.line_ids_c:
            warning_msg.append("Bag details is must.")
        if self.nature_of_job == 'disposal_assistance' and 'FLBS' not in self.combined_codes:
            warning_msg.append("For disposal assistance jobs, only flexi bag sale service is permitted")
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'approve': CT_JOB_CARD
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
                        [('code', '=', CT_JOB_CARD)], limit=1)
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
            
            self.auto_customer_invoice_entry_creation_from_jc()

            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            self.flexi_job_card_mail_data_design(
                trans_rec = self,
                mail_queue_name = 'Flexi Job Card Approve Mail',
                subject = f"#new-job-card# {self.service_id.name} - {self.name}",
                mail_config_name = 'Flexi Job Card Approve Mail'
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

    def entry_close(self):
        if self.status == 'approved':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.closer_remark or not self.closer_remark.strip():
                raise UserError(_("Closer remarks is must. Kindly enter the remarks in Closer Remarks field"))
            if self.closer_remark and len(self.closer_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters is required for closer remarks"))
            if not self.closer_date:
                raise UserError(_("Closer date is must. Kindly enter the closer date field"))
            if self.closer_date < self.entry_date:
                raise UserError(_("Closer date should be greater than JC date"))
            
            if self.nature_of_job == 'disposal_assistance' and 'FLBS' in self.combined_codes:
                self.env['ct.disposal.certificate'].job_card_close_auto_disposal_certificate_entry_creation(jc_rec=self)

            self.auto_payment_voucher_entry_creation_from_jc()

            self.write({'status': 'closed',
                        'close_user_id': self.env.user.id,
                        'close_date': time.strftime(TIME_FORMAT)
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
        return super(CtJobCard, self).write(vals)

    def auto_customer_invoice_entry_creation_from_jc(self):
        if 'FLOS' in self.combined_codes:
            price_rec = [(0, 0, {
                    'chrg_head_id': rec.chrg_head_id.id,
                    'description': rec.description,
                    'uom_id': rec.uom_id.id,
                    'qty': rec.qty,
                    'unit_price': rec.unit_price,
                    'currency_id': rec.currency_id.id,
                    'tax_ids': [(6, 0, rec.tax_ids.ids)],
                    'disc_amt': rec.disc_amt,
                    'disc_per': rec.disc_per,
                    'unitprice_wt': rec.unitprice_wt,
                    'taxable_amt': rec.taxable_amt,
                    'tax_amt': rec.tax_amt,
                    'tot_amt': rec.tot_amt,
                    'line_tot_amt': rec.line_tot_amt,
                }) for rec in self.bc_id.line_ids_e]

            invoice_model = self.env['ct.customer.invoice']
            invoice_model.create({
                'bc_id': self.bc_id.id,
                'service_id': self.service_id.id,
                'payment_mode': self.bc_id.payment_mode,
                'customer_id': self.bc_id.customer_id.id,
                'cus_bill_address': self.bc_id.cus_bill_address,
                'cus_del_address': self.bc_id.cus_del_address,
                'gst_no': self.bc_id.customer_id.gst_no,
                'pan_no': self.bc_id.customer_id.pan_no,
                'contact_person': self.bc_id.contact_person,
                'mobile_no': self.bc_id.mobile_no,
                'email': self.bc_id.email,
                'po_no': self.bc_id.po_no,
                'po_date': self.bc_id.po_date,
                'operational_type': self.bc_id.operational_type,
                'flexi_stuff_qty': self.bc_id.flexi_stuff_qty,
                'stuff_date': self.bc_id.stuff_date,
                'stuff_address': self.bc_id.stuff_address,
                'line_ids_e': price_rec,
                'line_ids_a': [(0, 0, line.copy_data()[0]) for line in self.line_ids_a],
                'round_off_amt': self.bc_id.round_off_amt,
                'net_amt': self.bc_id.net_amt,
                'manual_round_off': self.bc_id.manual_round_off,
                'combined_codes': self.combined_codes,
                'model_ref_no': self.name,
                'entry_mode': 'auto'
            })

    def auto_payment_voucher_entry_creation_from_jc(self):
        if self.line_ids_f and self.service_provider == 'internal':
            expense_rec = [(0, 0, {
                    'chrg_head_id': rec.chrg_head_id.id,
                    'emp_id': rec.emp_id.id,
                    'value': rec.value,
                    'currency_id': rec.currency_id.id,
                    'notes': rec.notes
                }) for rec in self.line_ids_f]
        
            advance_rec = [(0, 0, {
                    'chrg_head_id': rec.chrg_head_id.id,
                    'emp_id': rec.emp_id.id,
                    'value': rec.value,
                    'currency_id': rec.currency_id.id,
                    'notes': rec.notes
                }) for rec in self.line_ids_g]

            payment_voucher_model = self.env['ct.payment.voucher']
            pay_rec = payment_voucher_model.create({
                'bc_id': self.bc_id.id,
                'bc_date': self.bc_date,
                'service_id': self.service_id.id,
                'jc_id': self.id,
                'jc_date': self.entry_date,
                'emp_id': self.emp_id.id ,
                'emp_hod_id': self.emp_id.id,
                'mobile_no': self.mobile_no,
                'email': self.email,
                'line_ids_b': expense_rec,
                'line_ids_c': advance_rec,
                'entry_mode': 'auto'
            })
            pay_rec.onchange_currency_id()

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_JOB_CARD].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def flexi_job_card_mail_data_design(self, **kw):
        self.env.cr.execute(
                "SELECT ctm_flexi_job_card_approve_mail(%s, %s, %s, %s, %s)",
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
                mail_type=mail_type, model_name=CT_JOB_CARD, mail_name=mail_config_name)

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
            'all_closed': 0,
            'my_draft': 0,
            'my_wfa': 0,
            'my_approved': 0,
            'my_rejected': 0,
            'my_cancelled': 0,
            'my_closed': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0
        }

        ct_trans = self.env[CT_JOB_CARD]
        result['all_draft'] = ct_trans.search_count([('status', '=', 'draft')])
        result['all_wfa'] = ct_trans.search_count([('status', '=', 'wfa')])
        result['all_approved'] = ct_trans.search_count([('status', '=', 'approved')])
        result['all_rejected'] = ct_trans.search_count([('status', '=', 'rejected')])
        result['all_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled')])
        result['all_closed'] = ct_trans.search_count([('status', '=', 'closed')])
        result['my_draft'] = ct_trans.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_wfa'] = ct_trans.search_count([('status', '=', 'wfa'), ('user_id', '=', self.env.uid)])
        result['my_approved'] = ct_trans.search_count([('status', '=', 'approved'), ('user_id', '=', self.env.uid)])
        result['my_rejected'] = ct_trans.search_count([('status', '=', 'rejected'), ('user_id', '=', self.env.uid)])
        result['my_cancelled'] = ct_trans.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        result['my_closed'] = ct_trans.search_count([('status', '=', 'closed'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = ct_trans.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = ct_trans.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = ct_trans.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = ct_trans.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result
