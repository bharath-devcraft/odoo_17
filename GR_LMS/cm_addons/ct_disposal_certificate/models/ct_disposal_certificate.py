# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_DISPOSAL_CERTIFICATE = 'ct.disposal.certificate'
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

DISPOSAL_CATEGORY =  [('export_disposal', 'Export Disposal'),
                      ('expired_disposal', 'Expired Disposal'),
                      ('import_disposal', 'Import Disposal')]

class CtDisposalCertificate(models.Model):
    _name = 'ct.disposal.certificate'
    _description = 'Disposal Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'crt_date desc,name desc'

    name = fields.Char(string="Name")
    jc_id = fields.Many2one('ct.job.card', string="JC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    bc_id = fields.Many2one('ct.business.confirmation', string="BC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])
    customer_id = fields.Many2one('cm.customer', string="Customer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    address = fields.Char(string="Address", copy=False)
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)

    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    v_address = fields.Char(string="Address", copy=False)
    v_contact_person = fields.Char(string="Contact Person", size=50)
    v_mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    v_email = fields.Char(string="Email", copy=False, size=252)

    flexi_bag_id = fields.Many2one('product.template', string="Bag Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True),('custom_type', '=', 'flexi_bag')])
    uom_id = fields.Many2one('uom.uom', string="UOM", ondelete='restrict')
    qty = fields.Float(string="Qty", digits=(2, 3))

    certificate_no = fields.Char(string="Certificate No", copy=False)
    certificate_date = fields.Date(string="Certificate Date", copy=False)
    disposal_category = fields.Selection(selection=DISPOSAL_CATEGORY, string="Disposal Category", copy=False)
    disposal_date = fields.Date(string="Disposal Date", copy=False)
    disposal_loc = fields.Char(string="Disposal Location", copy=False)
    lot_ids = fields.Many2many('ct.stock.lot', string="Serial No", domain="[('product_id','=',flexi_bag_id),('store_pend_qty','=',0),('po_pend_qty','=',0)]")
    certificate_ids = fields.Many2many('ir.attachment', string="Certificate", ondelete='restrict', check_company=True)
    dc_id = fields.Many2one('ct.delivery.challan', string="DC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])

    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one(RES_COMPANY, copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, required=True)
    fy_control_date = fields.Date(string="FY Control Date", related='certificate_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Date.today, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    ap_rej_user_id = fields.Many2one(RES_USERS, string="Approved / Rejected By", copy=False, ondelete='restrict', readonly=True)
    ap_rej_date = fields.Datetime(string="Approved / Rejected Date", copy=False, readonly=True)
    cancel_user_id = fields.Many2one(RES_USERS, string="Cancelled By", copy=False, ondelete='restrict', readonly=True)
    cancel_date = fields.Datetime(string="Cancelled Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids_a = fields.One2many('ct.disposal.certificate.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)

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
        
        if self.lot_ids and self.qty != len(self.lot_ids):
            warning_msg.append("Qty and serial no count should be equal.")
        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'approve': CT_DISPOSAL_CERTIFICATE
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

            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            self.flexi_disposal_certificate_mail_data_design(
                trans_rec = self,
                mail_queue_name = 'Flexi Disposal Certificate Approve Mail',
                subject = f"#disposal-certificate# {self.customer_id.name}",
                mail_config_name = 'Flexi Disposal Certificate Approve Mail'
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
        return super(CtDisposalCertificate, self).write(vals)


    def job_card_close_auto_disposal_certificate_entry_creation(self, **kw):
        jc_rec = kw.get('jc_rec', '')

        if jc_rec:
            vendor_address = ", ".join(filter(None, [
                jc_rec.bc_id.vendor_id.street,
                jc_rec.bc_id.vendor_id.street1,
                jc_rec.bc_id.vendor_id.city_id.name,
                jc_rec.bc_id.vendor_id.state_id.name,
                jc_rec.bc_id.vendor_id.country_id.name,
                jc_rec.bc_id.vendor_id.pin_code
            ]))

            bag_line = jc_rec.line_ids_c[:1]

            dis_cer_model = jc_rec.env['ct.disposal.certificate']
            dis_cer_model.create({
                'name': jc_rec.name,
                'jc_id': jc_rec.id,
                'bc_id': jc_rec.bc_id.id,
                'customer_id': jc_rec.customer_id.id,
                'address': jc_rec.service_address,
                'contact_person': jc_rec.exp_contact_person,
                'mobile_no': jc_rec.exp_mobile_no,
                'email': jc_rec.exp_email,
                'vendor_id': jc_rec.bc_id.vendor_id.id,
                'v_address': vendor_address,
                'v_contact_person': jc_rec.bc_id.vendor_id.contact_person,
                'v_mobile_no': jc_rec.bc_id.vendor_id.mobile_no,
                'v_email': jc_rec.bc_id.vendor_id.email,
                'flexi_bag_id': bag_line.flexi_bag_id.id if bag_line else False,
                'uom_id': bag_line.uom_id.id if bag_line else False,
                'qty': bag_line.qty if bag_line else 0.0,
                'line_ids_a': [(0, 0, line.copy_data()[0]) for line in jc_rec.line_ids_a],
                'entry_mode': 'auto'
            })

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_DISPOSAL_CERTIFICATE].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def flexi_disposal_certificate_mail_data_design(self, **kw):
        self.env.cr.execute(
                "SELECT ctm_flexi_disposal_certificate_approve_mail(%s, %s, %s, %s, %s)",
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
                mail_type=mail_type, model_name=CT_DISPOSAL_CERTIFICATE, mail_name=mail_config_name)

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

        ct_trans = self.env[CT_DISPOSAL_CERTIFICATE]
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
