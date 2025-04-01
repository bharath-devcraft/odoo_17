# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation
import time
from datetime import datetime
from odoo.exceptions import UserError

CT_DELIVERY_CHALLAN = 'ct.delivery.challan'
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

ACCESSORIES =  [('with_accessories','With Accessories'),
               ('without_accessories', 'Without Accessories')]

DC_TYPE =  [('new','New'),
            ('replacement', 'Replacement')]

class CtDeliveryChallan(models.Model):
    _name = 'ct.delivery.challan'
    _description = 'Delivery Challan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="DC No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    entry_date = fields.Date(string="DC Date", copy=False, default=fields.Date.today)
    bc_id = fields.Many2one('ct.business.confirmation', string="BC No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True),('issue_status', '=', 'pending'),('invoice_status', '=', 'pending'),'|',('combined_codes', 'ilike', 'FLBS'), ('combined_codes', 'ilike', 'FLAS')])
    bc_date = fields.Date(string="BC Date", copy=False)
    due_date = fields.Date(string="Validity Date", copy=False)
    service_id = fields.Many2one('cm.service', string="Service Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    vendor_id = fields.Many2one('cm.vendor.master', string="Vendor Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    accessories = fields.Selection(selection=ACCESSORIES, string="Accessories" ,copy=False)
    bill_no = fields.Char(string="E- Way Bill No", copy=False)
    dc_type = fields.Selection(selection=DC_TYPE, string="DC Type" ,copy=False, default='new')

    customer_id = fields.Many2one('cm.customer', string="Customer Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    cus_bill_address = fields.Char(string="Billing Address", default=False)
    gst_no = fields.Char(string="GST No", copy=False, size=15)
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15, copy=False)
    email = fields.Char(string="Email", copy=False, size=252)
    cus_del_address = fields.Char(string="Delivery Address", default=False)

    vehicle_id = fields.Many2one('cm.vehicle.master', string="Vehicle No", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    driver_id = fields.Many2one('cm.driver.master', string="Driver Name", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    dr_mobile_no = fields.Char(string="Mobile No", size=15, copy=False)

    ap_rej_remark = fields.Text(string="Approve / Reject Remarks", copy=False)
    cancel_remark = fields.Text(string="Cancel Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    combined_codes = fields.Char(string="Combined Codes", readonly=True)
    cus_inv_id = fields.Many2one('ct.customer.invoice', string="Customer Invoice No", ondelete='restrict', domain=[('status', '=', 'approved'),('active_trans', '=', True)])

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

    line_ids_a = fields.One2many('ct.delivery.challan.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.delivery.challan.acc.line', 'header_id', string="Flexi Details", copy=True, c_rule=True)

    @api.onchange('service_id')
    def onchange_service_ids(self):
        codes = []
        if self.service_id:
            codes.append(self.service_id.sys_ref)
        self.combined_codes = list(set(codes))

    @api.onchange('bc_id')
    def onchange_bc_id(self):
        self.service_id = False
        self.bc_date = False
        self.customer_id = False
        self.cus_bill_address = False
        self.cus_del_address = False
        self.gst_no = False
        self.contact_person = False
        self.mobile_no = False
        self.email = False
        self.combined_codes = False
        self.vendor_id = False
        self.accessories = False
        self.line_ids_a = [(5, 0, 0)]
        self.line_ids_c = [(5, 0, 0)]

        if not self.bc_id:
            return

        self.service_id = self.bc_id.service_id.id
        self.bc_date = self.bc_id.entry_date
        self.customer_id = self.bc_id.customer_id.id
        self.cus_bill_address = self.bc_id.cus_bill_address
        self.cus_del_address = self.bc_id.cus_del_address
        self.gst_no = self.bc_id.customer_id.gst_no
        self.contact_person = self.bc_id.contact_person
        self.mobile_no = self.bc_id.mobile_no
        self.email = self.bc_id.email
        self.combined_codes = self.bc_id.combined_codes
        self.line_ids_a = [(0, 0, line.copy_data()[0]) for line in self.bc_id.line_ids_a]


        if 'FLBS' in self.combined_codes:
            self.vendor_id = self.bc_id.vendor_id.id
            self.accessories = 'with_accessories' if self.bc_id.accessories_req == 'yes' else 'without_accessories'

        self.line_ids_c = [(0, 0, {
            'flexi_type': rec.flexi_type,
            'flexi_layer_type_id': rec.flexi_layer_type_id.id if rec.flexi_layer_type_id else False,
            'flexi_capacity_id': rec.flexi_capacity_id.id,
            'vendor_id': rec.vendor_id.id if rec.vendor_id else False,
            'qty': rec.pending_qty,
            'accessory_set_id': rec.accessory_set_id.id,
            'pod_services': rec.pod_services,
            'bag_req_date': rec.bag_req_date,
            'bc_line_id': rec.id,
            'line_ids': [(0, 0, {
                'accessories_id': line.accessories_id.id,
                'uom_id': line.uom_id.id,
                'qty': line.qty
            }) for line in rec.line_ids]
        }) for rec in self.bc_id.line_ids_c if rec.pending_qty > 0]

        if 'FLBS' in self.combined_codes:
            self.flexi_bag_id_update()

    def flexi_bag_id_update(self, **kw):
        model_rec = kw.get('model_rec', self)
        for line in model_rec.line_ids_c:
            domain = [
                ('status', '=', 'active'),
                ('active_trans', '=', True),
                ('custom_type', '=', 'flexi_bag'),
                ('flexi_type', '=', line.flexi_type),
                ('layer_type_id', '=', line.flexi_layer_type_id.id),
                ('capacity_id', '=', line.flexi_capacity_id.id),
            ]
            if line.vendor_id:
                domain.append(('vendor_id', '=', line.vendor_id.id))
            
            flexi_bag_rec = self.env['product.template'].search(domain, limit=1)
            line.flexi_bag_id = flexi_bag_rec.id if flexi_bag_rec else False

    @api.onchange('driver_id')
    def onchange_driver_id(self):
        if self.driver_id:
            self.dr_mobile_no = self.driver_id.mobile_no
        else:
            self.dr_mobile_no = False

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
        qty_warning_added = False
        pending_qty_warning_added = False
        serial_warning_added = False
        sub_serial_warning_added = False
        chk_serial_warning_added = False

        if self.entry_mode == 'manual':
            if any(code in self.combined_codes for code in ('FLBS', 'FLAS')) and not self.line_ids_c:
                warning_msg.append("Flexi and accessories details is must.")
            for line in self.line_ids_c:
                if not line.qty or (line.qty <= 0 and not qty_warning_added):
                    warning_msg.append("Flexi and accessories details qty should be greater than zero.")
                    qty_warning_added = True 
                if line.qty and line.qty > line.pending_qty and not pending_qty_warning_added:
                    warning_msg.append("Flexi and accessories details qty should not be greater than pending qty.")
                    pending_qty_warning_added = True

        for line in self.line_ids_c:
            if line.accessory_set_id and not line.lot_ids and not chk_serial_warning_added:
                warning_msg.append("Flexi and accessories details serial no is required.")
                chk_serial_warning_added = True
            if line.lot_ids and line.qty != len(line.lot_ids) and not serial_warning_added:
                warning_msg.append("Flexi and accessories details qty and serial no count should be equal.")
                serial_warning_added = True

            for sub_line in line.line_ids:
                if sub_line.lot_ids and sub_line.qty != len(sub_line.lot_ids) and not sub_serial_warning_added:
                    warning_msg.append("Flexi and accessories sub details qty and serial no count should be equal.")
                    sub_serial_warning_added = True

        if kw.get('action') == 'approve':
            self.validate_approve_action(warning_msg)

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'approve': CT_DELIVERY_CHALLAN
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
                        [('code', '=', CT_DELIVERY_CHALLAN)], limit=1)
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
            
            if self.entry_mode == 'manual':
                for line in self.line_ids_c:
                    if line.bc_line_id:
                        line.bc_line_id.pending_qty -= line.qty

            self.stock_move_creation()

            self.write({'status': 'approved',
                        'ap_rej_user_id': self.env.user.id,
                        'ap_rej_date': time.strftime(TIME_FORMAT)
                        })

            self.flexi_dc_mail_data_design(
                trans_rec = self,
                mail_queue_name = 'Flexi DC Approve Mail',
                subject = f"#delivery-challan-approved# {self.service_id.name} - {self.name}",
                mail_config_name = 'Flexi DC Approve Mail'
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
        return super(CtDeliveryChallan, self).write(vals)

    def auto_delivery_challan_entry_creation(self, **kw):
        cus_inv_rec = kw.get('cus_inv_rec', '')

        if cus_inv_rec and any(code in cus_inv_rec.combined_codes for code in ('FLBS', 'FLAS')):
            dc_model = cus_inv_rec.env['ct.delivery.challan']
            dc_rec = dc_model.create({
                'bc_id': cus_inv_rec.bc_id.id,
                'bc_date': cus_inv_rec.bc_id.entry_date,
                'service_id': cus_inv_rec.service_id.id,
                'customer_id': cus_inv_rec.bc_id.customer_id.id,
                'cus_bill_address': cus_inv_rec.bc_id.cus_bill_address,
                'cus_del_address': cus_inv_rec.bc_id.cus_del_address,
                'gst_no': cus_inv_rec.bc_id.customer_id.gst_no,
                'contact_person': cus_inv_rec.bc_id.contact_person,
                'mobile_no': cus_inv_rec.bc_id.mobile_no,
                'email': cus_inv_rec.bc_id.email,
                'line_ids_a': [(0, 0, line.copy_data()[0]) for line in cus_inv_rec.line_ids_a],
                'combined_codes': cus_inv_rec.combined_codes,
                'cus_inv_id': cus_inv_rec.id,
                'entry_mode': 'auto'
            })

            if dc_rec and 'FLBS' in cus_inv_rec.combined_codes:
                dc_rec.write({
                    'vendor_id': cus_inv_rec.vendor_id.id,
                    'accessories': cus_inv_rec.accessories,
                })

            dc_rec.line_ids_c = [(0, 0, {
                'flexi_type': rec.flexi_type,
                'flexi_layer_type_id': rec.flexi_layer_type_id.id if rec.flexi_layer_type_id else False,
                'flexi_capacity_id': rec.flexi_capacity_id.id,
                'vendor_id': rec.vendor_id.id if rec.vendor_id else False,
                'qty': rec.qty,
                'accessory_set_id': rec.accessory_set_id.id,
                'pod_services': rec.pod_services,
                'bag_req_date': rec.bag_req_date,
                'line_ids': [(0, 0, {
                    'accessories_id': line.accessories_id.id,
                    'uom_id': line.uom_id.id,
                    'qty': line.qty
                }) for line in rec.line_ids]
            }) for rec in cus_inv_rec.line_ids_c]

            if 'FLBS' in cus_inv_rec.combined_codes:
                dc_rec.flexi_bag_id_update(model_rec=dc_rec)

    def stock_move_creation(self):
        for line in self.line_ids_c:
            if line.lot_ids:
                self.create_stock_move(line, line.flexi_bag_id)
                for lot_line in line.lot_ids:
                    lot_line.store_pend_qty -= 1
                    lot_line.po_pend_qty -= 1

            for sub_line in line.line_ids:
                if sub_line.lot_ids:
                    self.create_stock_move(sub_line, sub_line.accessories_id)
                    for lot_line in sub_line.lot_ids:
                        lot_line.store_pend_qty -= 1
                        lot_line.po_pend_qty -= 1

    def create_stock_move(self, line, product):
        stock_move_obj = self.env['ct.stock.move']
        main_store = self.env['cm.stock.location'].search([('name', '=', 'Main Store')], limit=1)
        sub_store = self.env['cm.stock.location'].search([('name', '=', 'Sub Store')], limit=1)

        stock_move_obj.create({
            'name': self.name,
            'entry_date': self.entry_date,
            'from_location_id': main_store.id,
            'to_location_id': sub_store.id,
            'qty': line.qty,
            'product_id': product.id,
            'description': product.name,
            'unit_price': line.lot_ids[0].unit_price if line.lot_ids else 0.0,
            'uom_id': product.uom_id.id if product.uom_id else False,
            'entry_mode': 'auto',
            'user_id': self.user_id.id,
            'ap_rej_user_id': self.env.user.id,
            'ap_rej_date': self.ap_rej_date,
            'status': 'approved'
        })

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_DELIVERY_CHALLAN].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def flexi_dc_mail_data_design(self, **kw):
        self.env.cr.execute(
                "SELECT ctm_flexi_dc_approve_mail(%s, %s, %s, %s, %s)",
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
                mail_type=mail_type, model_name=CT_DELIVERY_CHALLAN, mail_name=mail_config_name)

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

        ct_trans = self.env[CT_DELIVERY_CHALLAN]
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
