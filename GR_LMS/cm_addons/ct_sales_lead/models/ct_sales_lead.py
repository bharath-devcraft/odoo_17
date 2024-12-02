# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation,valid_mobile_no,valid_email
import time
from datetime import datetime, date, timedelta
from collections import defaultdict

from odoo.exceptions import UserError

CT_SALES_LEAD = 'ct.sales.lead'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('won', 'Won'),
    ('lost', 'Lost')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

CUSTOMER_TYPE =  [('new','New'),
               ('existing', 'Existing')]

LEAD_TYPE =  [('marketing_lead','Marketing Lead'),
               ('tender', 'Tender')]

STAGES = [
    ('potential', 'Potential'),
    ('interested', 'Interested'),
    ('qualified', 'Qualified'),
    ('not_interested', 'Not Interested')]

class CtSalesLead(models.Model):
    _name = 'ct.sales.lead'
    _description = 'Sales Lead'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    name = fields.Char(string="Lead No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    customer_type = fields.Selection(selection=CUSTOMER_TYPE, string="Customer Type", copy=False, tracking=True)
    lead_type = fields.Selection(selection=LEAD_TYPE, string="Lead Type", copy=False, default= 'marketing_lead', tracking=True)
    customer_id = fields.Many2one('cm.customer', string="Customer Name",copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customer_name = fields.Char(string="Customer Name", size=50)
    contact_person = fields.Char(string="Contact Person", size=50)
    mobile_no = fields.Char(string="Mobile No", size=15)
    address = fields.Char(string="Address", size=252)
    email = fields.Char(string="Email", copy=False, size=252)
    enq_source_id = fields.Many2one('cm.enquiry.source', string="Lead Source", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    service_name = fields.Char(string="Required Services", size=252)
    next_followup_date = fields.Date(string="Next Follow Up Date", copy=False, tracking=True)
    product = fields.Char(string="Product", size=252, copy=False)
    last_followup_date = fields.Date(string="Last Followup Date", copy=False, tracking=True)
    feedback = fields.Text(string="Rating Feedback", copy=False)
    rej_remark_id = fields.Many2one('cm.rejection.remark', string="Rejection Remark", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    lost_remark = fields.Text(string="Lost Remarks", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)

    active = fields.Boolean(string="Visible", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    won_lost_user_id = fields.Many2one(RES_USERS, string="Won / Lost By", copy=False, ondelete='restrict', readonly=True)
    won_lost_date = fields.Datetime(string="Won / Lost Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)

    line_ids = fields.One2many('ct.sales.lead.progress.log.line', 'header_id', string="Progress Log", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.sales.lead.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.sales.lead.additional.contact.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)

    @api.constrains('mobile_no')
    def mobile_no_validation(self):
        if self.mobile_no and not valid_mobile_no(self.mobile_no):
            raise UserError(_(f"Mobile number is  invalid. Please enter correct mobile number, Ref : {self.mobile_no}"))

    @api.constrains('email')
    def email_validation(self):
        if self.email and not valid_email(self.email):
            raise UserError(_(f"Email is invalid. Please enter the correct email, Ref : {self.email}"))

    @api.constrains('line_ids_b','email','mobile_no')
    def contact_details_validations(self):
        mobile_nos = {self.mobile_no}
        emails = {self.email.replace(" ", "").upper() if self.email else self.email}
        for item in self.line_ids:
            if item.email:
                emails.add(item.email.replace(" ", "").upper())
            if item.mobile_no:
                mobile_nos.add(item.mobile_no)
        if self.mobile_no:
            if len(mobile_nos) < (1 + len([item for item in self.line_ids if item.mobile_no])):
                raise UserError(_("Duplicate mobile numbers are not allowed within the provided contact details"))
        if self.email:
            if len(emails) < (1 + len([item for item in self.line_ids if item.email])):
                raise UserError(_("Duplicate emails are not allowed within the provided contact details"))

    @api.onchange('customer_type')
    def onchange_customer_type(self):
        self.customer_id = False
        self.customer_name = False
        self.address = False

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            self.customer_name = self.customer_id.name
            self.address = ", ".join(filter(None, [
                self.customer_id.street,
                self.customer_id.street1,
                self.customer_id.city_id.name,
                self.customer_id.state_id.name,
                self.customer_id.country_id.name
            ]))
        else:
            self.address = False

    @api.onchange('next_followup_date', 'last_followup_date')
    def onchange_next_followup_date(self):
        if self.next_followup_date and self.next_followup_date < fields.Date.today():
            raise UserError(_("Next Follow up date should not be lesser than current date"))
        if self.next_followup_date and self.last_followup_date  and self.next_followup_date < self.last_followup_date:
            raise UserError(_("Next follow up Date should not be lesser than last followup date"))
    
    @api.onchange('line_ids')
    def onchange_line_ids(self):
        if self.line_ids and self.status != 'draft':
            self.last_followup_date = self.next_followup_date
            line_rec = self.line_ids.filtered(lambda line: line.crt_date).sorted('crt_date', reverse=True)[:1]
            self.next_followup_date = line_rec.next_followup_date
            self.feedback = line_rec.remarks

    def display_warnings(self, warning_msg, kw):
        if warning_msg:
            formatted_messages = "\n".join(warning_msg)
            if not kw.get('mode_of_call'):
                raise UserError(_(formatted_messages))
            else:
                return [formatted_messages]
        else:
            return False

    def validations(self, **kw):
        warning_msg = []

        return self.display_warnings(warning_msg, kw)

    def sequence_no_validations(self, **kw):
        warning_msg = []
        action_code_map = {
            'confirm': CT_SALES_LEAD
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

            if not self.name:
                sequence_id = self.env[IR_SEQUENCE].search(
                        [('code', '=', CT_SALES_LEAD)], limit=1)
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
                    self.sequence_no_validations(date=self.entry_date, action='confirm')

                self.name = sequence
            
            self.write({'status': 'open',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime(TIME_FORMAT)
                        })
            
            self.sales_lead_mail_data_design(
                                        trans_rec = self,
                                        mail_queue_name = 'Sales Lead Confirm Mail',
                                        subject = f"#new-sale-lead# {self.customer_name}",
                                        mail_config_name = 'Sales Lead Confirm Mail'
                                    )

        return True
    
    @validation
    def entry_won(self):
        if self.status == 'open':
            self.write({'status': 'won',
                        'won_lost_user_id': self.env.user.id,
                        'won_lost_date': time.strftime(TIME_FORMAT)
                        })
        return True
    
    def entry_lost(self):
        if self.status == 'open':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.rej_remark_id or (not self.lost_remark or not self.lost_remark.strip()):
                raise UserError(_("Lost reason is must. Kindly enter the lost reason and remark in lost reason tab"))
            if self.lost_remark and len(self.lost_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters are must for lost remarks"))
            self.write({'status': 'lost',
                        'won_lost_user_id': self.env.user.id,
                        'won_lost_date': time.strftime(TIME_FORMAT)
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
        return super(CtSalesLead, self).write(vals)

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_SALES_LEAD].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def sales_lead_mail_data_design(self, **kw):
        self.env.cr.execute(
            """select ctm_sales_lead_confirm_mail(%s,'%s','%s','%s')""" %
            (self.id,self.status,self.name or self.draft_name, self.env.user.partner_id.name,))
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
                mail_type=mail_type, model_name=CT_SALES_LEAD, mail_name=mail_config_name)

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

    def progress_log_flag_update(self):
        self.line_ids.search([
            ('readonly_flag', '=', False),
            ('crt_date', '<', fields.Date.today())
        ]).write({'readonly_flag': True})
        return True

    @api.model
    def retrieve_dashboard(self):
        result = {
            'all_draft': 0,
            'all_open': 0,
            'all_won': 0,
            'all_lost': 0,
            'my_draft': 0,
            'my_open': 0,
            'my_won': 0,
            'my_lost': 0,
            'all_today_count': 0,
            'all_today_value': 0,
            'my_today_count': 0,
            'my_today_value': 0
        }

        sales_lead = self.env[CT_SALES_LEAD]
        result['all_draft'] = sales_lead.search_count([('status', '=', 'draft')])
        result['all_open'] = sales_lead.search_count([('status', '=', 'open')])
        result['all_won'] = sales_lead.search_count([('status', '=', 'won')])
        result['all_lost'] = sales_lead.search_count([('status', '=', 'lost')])
        result['my_draft'] = sales_lead.search_count([('status', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['my_open'] = sales_lead.search_count([('status', '=', 'open'), ('user_id', '=', self.env.uid)])
        result['my_won'] = sales_lead.search_count([('status', '=', 'won'), ('user_id', '=', self.env.uid)])
        result['my_lost'] = sales_lead.search_count([('status', '=', 'cancelled'), ('user_id', '=', self.env.uid)])
        
        result['all_today_count'] = sales_lead.search_count([('crt_date', '>=', fields.Date.today())])
        result['all_month_count'] = sales_lead.search_count([('crt_date', '>=', datetime.today().replace(day=1))])
        result['my_today_count'] = sales_lead.search_count([('user_id', '=', self.env.uid),('crt_date', '>=', fields.Date.today())])
        result['my_month_count'] = sales_lead.search_count([('user_id', '=', self.env.uid), ('crt_date', '>=',datetime.today().replace(day=1))])

        return result

    def sale_lead_followup_date_popup(self):
        today = fields.Date.today()
        trans_rec = self.env['ct.sales.lead']
        
        missed_deliveries = trans_rec.search([
            ('status', '=', 'open'),
            ('next_followup_date', '<=', today),
            ('next_followup_date', '>=', today - timedelta(days=10))
        ])

        if missed_deliveries:

            def aggregate_notifications(deliveries):
                user_transactions = defaultdict(list)
                for trans in deliveries:
                    user_transactions[trans.confirm_user_id].append(trans)

                def format_transaction(rec):
                    return f"{rec.name} - {rec.customer_name}"

                return {
                    user_id: ',\n '.join([format_transaction(rec) for rec in rec_data])
                    for user_id, rec_data in user_transactions.items()
                }

            missed_trans_data = aggregate_notifications(missed_deliveries)

            notifications = []

            notify_rec = self.env['cp.popup.notification']
            today_date = date.today()

            for user,rec_value in missed_trans_data.items():
                notify_rec_name = 'Sales Lead Overdue'
                notif_exist_record = notify_rec.search([
                    ('name', '=', notify_rec_name),
                    ('user_id', '=', user.id),
                    ('entry_date', '=', today_date)
                ], limit=1)

                if not notif_exist_record:

                    message = f"Sales Lead :\n {rec_value}"
                    notif = [{
                            'user_id': user.id,
                            'title': 'Followup Call Reminder',
                            'message': message,
                            'timer': -8420,
                            'notify_at': '2024-07-17 06:29:00',
                            'notify_name': notify_rec_name,
                            'close': 'no',}]
                    notifications.append([user.partner_id, 'custom.notification', notif])

            if len(notifications) > 0:
                self.env['bus.bus']._sendmany(notifications)