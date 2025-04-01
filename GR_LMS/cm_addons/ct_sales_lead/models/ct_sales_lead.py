# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.custom_properties.decorators import validation,valid_mobile_no,valid_email
import time
from datetime import datetime, date, timedelta
from collections import defaultdict
from collections import Counter

from odoo.exceptions import UserError

CT_SALES_LEAD = 'ct.sales.lead'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
IR_CONFIG_PARAMETER = 'ir.config_parameter'
IR_SEQUENCE = 'ir.sequence'
CM_SERVICE = 'cm.service'
CT_SALES_LEAD_SERVICE_DETAILS_WIZARD = 'ct.sales.lead.service.details.wizard'
CM_COUNTRY_CODE = 'cm.country.code'

CUSTOM_STATUS = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('won', 'Won'),
    ('lost', 'Lost')]

PROGRESS_STATUS = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('enquiry_draft', 'Enquiry Draft'),
    ('quotation_draft', 'Quotation Draft'),
    ('quotation_wfa', 'Quotation WFA'),
    ('quotation_sent', 'Quotation Sent'),
    ('order_released', 'Order Released'),
    ('enquiry_cancelled', 'Enquiry Cancelled'),
    ('quotation_rejected', 'Quotation Rejected'),  
    ('quotation_cancelled', 'Quotation Cancelled')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

CUSTOMER_TYPE =  [('new','New'),
               ('existing', 'Existing / New Service')]

LEAD_TYPE =  [('marketing_lead','Marketing Lead'),
               ('tender', 'Tender')]

STAGES = [
    ('potential', 'Potential'),
    ('interested', 'Interested'),
    ('qualified', 'Qualified'),
    ('not_interested', 'Not Interested')]

CUSTOM_WIZARD_STATUS = [
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('new_lead', 'New Lead')]

APPOINTMENT_TYPE = [
    ('virtual', 'Virtual'),
    ('site_visit', 'Site Visit')]

class CtSalesLead(models.Model):
    _name = 'ct.sales.lead'
    _description = 'Sales Lead'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _order = 'entry_date desc,name desc'

    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        if 'entry_mode' in res and res['entry_mode'] == 'manual':
            ser_recs = self.env[CM_SERVICE].search([
                ('category', '=', 'main'),
                ('status', '=', 'active'),
                ('active_trans', '=', True)
            ])
            if ser_recs:
                res['line_ids_c'] = [
                    (0, 0, {
                        'service_id': rec.id,
                        'entry_mode': 'auto'
                    })
                    for rec in ser_recs
                ]

        return res

    name = fields.Char(string="Lead No", readonly=True, index=True, copy=False, size=30, c_rule=True)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    customer_type = fields.Selection(selection=CUSTOMER_TYPE, string="Customer / Service Type", copy=False, tracking=True)
    lead_type = fields.Selection(selection=LEAD_TYPE, string="Lead Type", copy=False, default= 'marketing_lead', tracking=True)
    customer_id = fields.Many2one('cm.customer', string="Customer Name",copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customer_name = fields.Char(string="Customer Name", size=50)
    customer_type_ids = fields.Many2many('cm.customer.type', string="Customer Type", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    customer_division = fields.Char(string="Customer Division", size=50)
    designation = fields.Char(string="Designation", size=50)
    appointment_type = fields.Selection(selection=APPOINTMENT_TYPE, string="Appointment Type", copy=False, tracking=True)
    contact_person = fields.Char(string="Contact Person", size=50)
    mb_cc_id = fields.Many2one(CM_COUNTRY_CODE, string="Mobile Country Code", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    mobile_no = fields.Char(string="Mobile No", size=15)
    address = fields.Char(string="Address", size=252)
    country_id = fields.Many2one('res.country', string="Country", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    email = fields.Char(string="Email", copy=False, size=252)
    enq_source_id = fields.Many2one('cm.enquiry.source', string="Lead Source", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    service_ids = fields.Many2many(CM_SERVICE, string="Additional Services", ondelete='restrict', domain="[('status', '=', 'active'),('active_trans', '=', True)]")
    sales_exec_user_id = fields.Many2one(RES_USERS, string="Primary Sales Executive", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    sec_sales_exec_user_id = fields.Many2one(RES_USERS, string="Secondary Sales Executive", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    next_followup_date = fields.Date(string="Next Follow Up Date", copy=False, tracking=True)
    product = fields.Char(string="Product", size=252, copy=False)
    product_sds_ids = fields.Many2many('ir.attachment', string="Product SDS", ondelete='restrict', check_company=True)
    last_followup_date = fields.Date(string="Last Followup Date", copy=False, tracking=True)
    feedback = fields.Text(string="Rating Feedback", copy=False)
    tat = fields.Integer(string="TAT", copy=False, compute='_get_tat_count')
    rej_remark_id = fields.Many2one('cm.rejection.remark', string="Rejection Remark", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    lost_remark = fields.Text(string="Lost Remarks", copy=False)
    visitor_summary = fields.Html(string="Discussion Points", copy=False)
    remarks = fields.Text(string="Remarks", copy=False)
    con_opp = fields.Text(string="Conclusion / Opportunity", copy=False)
    company_physical = fields.Text(string="Company Physically Verified", copy=False)
    bus_vert_id = fields.Many2one('cm.business.vertical', string="Business Vertical", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", copy=False, default="draft", readonly=True, store=True, tracking=True)
    progress_status = fields.Selection(selection=PROGRESS_STATUS, string="Progress Status", copy=False, default="draft", readonly=True, store=True, tracking=True)

    active = fields.Boolean(string="Visible in View", default=True)
    active_rpt = fields.Boolean(string="Visible In Reports", default=True)
    active_trans = fields.Boolean(string="Visible In Transactions", default=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, ondelete='restrict', readonly=True, domain=[('status', '=', 'active'),('active_trans', '=', True)])
    fy_control_date = fields.Date(string="FY Control Date", related='entry_date', store=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", copy=False, default="manual", readonly=True, tracking=True)
    sales_lead_id = fields.Many2one(CT_SALES_LEAD, string="Parent Ref",copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
    user_id = fields.Many2one(RES_USERS, string="Created By", copy=False, default=lambda self: self.env.user.id, ondelete='restrict', readonly=True)
    crt_date = fields.Datetime(string="Creation Date", copy=False, default=fields.Datetime.now, readonly=True)
    confirm_user_id = fields.Many2one(RES_USERS, string="Confirmed By", copy=False, ondelete='restrict', readonly=True)
    confirm_date = fields.Datetime(string="Confirmed Date", copy=False, readonly=True)
    won_lost_user_id = fields.Many2one(RES_USERS, string="Won / Lost By", copy=False, ondelete='restrict', readonly=True)
    won_lost_date = fields.Datetime(string="Won / Lost Date", copy=False, readonly=True)
    update_user_id = fields.Many2one(RES_USERS, string="Last Updated By", copy=False, ondelete='restrict', readonly=True)
    update_date = fields.Datetime(string="Last Updated Date", copy=False, readonly=True)
    readonly_flag = fields.Boolean(string="Readonly Flag", default=False, copy=False, readonly=True)

    line_ids = fields.One2many('ct.sales.lead.progress.log.line', 'header_id', string="Progress Log", copy=True, c_rule=True)
    line_ids_a = fields.One2many('ct.sales.lead.attachment.line', 'header_id', string="Attachments", copy=True, c_rule=True)
    line_ids_b = fields.One2many('ct.sales.lead.additional.contact.line', 'header_id', string="Additional Contacts", copy=True, c_rule=True)
    line_ids_c = fields.One2many('ct.sales.lead.service.details.line', 'header_id', string="Service Details", copy=True, c_rule=True)

    @api.depends('status', 'confirm_date')
    def _get_tat_count(self):
        for record in self:
            if record.status == 'open' and record.confirm_date:
                record.tat = (datetime.now() - record.confirm_date).days
            elif record.status != 'lost' and record.won_lost_date:
                record.tat = (record.won_lost_date - record.confirm_date).days
            else:
                record.tat = 0

    @api.constrains('email')
    def email_validation(self):
        if self.email and not valid_email(self.email):
            raise UserError(_(f"Email is invalid. Please enter the correct email, Ref : {self.email}"))

    @api.onchange('sales_exec_user_id', 'sec_sales_exec_user_id')
    def sales_execute_validation(self):
        if self.sales_exec_user_id and self.sec_sales_exec_user_id:
            if self.sales_exec_user_id.id == self.sec_sales_exec_user_id.id:
                raise UserError(
                    _("Primary sales executive and Secondary sales executive cannot be the same. Please select a different executive."))

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
        self.country_id = False

    @api.onchange('product_sds_ids')
    def check_product_sds_attach_ids(self):
        valid_attachments = self.product_sds_ids.filtered(lambda att: att.mimetype == 'application/pdf')

        if len(valid_attachments) < len(self.product_sds_ids):
            self.product_sds_ids = valid_attachments
            return {
                'warning': {
                    'title': _("Invalid File Format"),
                    'message': _("Only PDF files are allowed in the SDS Document field."),
                }
            }

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            self.customer_name = self.customer_id.name
            self.address = ", ".join(filter(None, [
                self.customer_id.street,
                self.customer_id.street1,
                self.customer_id.city_id.name,
                self.customer_id.state_id.name
            ]))
            self.country_id = self.customer_id.country_id.id
            self.contact_person = self.customer_id.contact_person
            self.mobile_no = self.customer_id.mobile_no
            self.email = self.customer_id.email
        else:
            self.address = False
            self.country_id = False
            self.contact_person = False
            self.mobile_no = False
            self.email = False

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id:
            record = self.env['cm.country.code'].search([('country_id', '=', self.country_id.id)], limit=1)
            c_code = record.id if record else False
            self.mb_cc_id = c_code
        else:
            self.mb_cc_id = False


    @api.onchange('next_followup_date', 'last_followup_date')
    def onchange_next_followup_date(self):
        if self.next_followup_date and self.next_followup_date < fields.Date.today():
            raise UserError(_("Next Follow up date should not be lesser than current date"))


    
    @api.onchange('line_ids')
    def onchange_line_ids(self):
        if self.line_ids and self.status != 'draft':
            self.last_followup_date = self.next_followup_date
            line_rec = self.line_ids[-1] if self.line_ids else False
            self.feedback = line_rec.remarks
            self.next_followup_date = line_rec.next_followup_date


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
        if not self.line_ids_c or self.line_ids_c and not any(self.line_ids_c.mapped('is_select')):
            warning_msg.append("System will not allow confirmation without selecting at least one service.")
        else:
            dub_rec = [line.service_id.name for line in self.line_ids_c ]
            count = Counter(dub_rec)
            duplicates = [item for item, freq in count.items() if freq > 1]
            if duplicates:
                warning_msg.append(f"Duplicate service not allowed. Ref: {','.join(duplicates)}")

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
                warning_msg.append("Sequence number configuration issue. Kindly contact LMS team.")
        if kw.get('date'):
            self.env.cr.execute(
                """select value from ir_config_parameter 
                where key = 'custom_properties.seq_num_reset' 
                order by id desc limit 1;
            """)
            seq_reset = self.env.cr.fetchone()
            if not seq_reset or not seq_reset[0]:
                warning_msg.append("The sequence number reset option has not been configured. Kindly contact LMS team.")
            elif seq_reset[0] == 'fiscal_year':
                fiscal_year = self.env['cm.fiscal.year'].search([
                                ('from_date', '<=', kw.get('date')),('to_date', '>=', kw.get('date')),
                                ('status', '=', 'active'),('active', '=', True)])
                if not fiscal_year:
                    warning_msg.append("Financial year configuration issue. Kindly contact LMS team")

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
                        'progress_status': 'open',
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
            self.validations()
        if self.rej_remark_id or self.lost_remark:
            raise UserError(_("Lost Reason or remarks given, with lost reason cannot proceed won"))
        selected = self.line_ids_c.filtered(lambda l: l.is_select)
        selected_lines = [line for line in self.line_ids_c if line.is_select]

        if len(selected_lines) == 1:
            wizard = self.env['ct.sales.lead.service.details.wizard'].create({
                'header_id': self.id,
                'line_ids': [(0, 0, {
                    'details_id': selected_lines[0].id,
                    'status': 'won',
                })]
            })
            wizard.wizard_submit_button()
        elif len(selected_lines) > 1:
            return {
                'name': 'Enquiry Details',
                'type': 'ir.actions.act_window',
                'res_model': 'ct.sales.lead.service.details.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_id': self.id},
            }
        self.line_ids_c = [(6, 0, selected.ids)]


    def entry_lost(self):
        if self.status == 'open':
            min_char = self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length')
            if not self.rej_remark_id or (not self.lost_remark or not self.lost_remark.strip()):
                raise UserError(_("Lost reason is must. Kindly enter the lost reason and remark in lost reason tab."))
            if self.lost_remark and len(self.lost_remark.strip()) < int(min_char):
                raise UserError(_(f"Minimum {min_char} characters are must for lost remarks."))
            self.write({'status': 'lost',
                        'progress_status': 'lost',
                        'won_lost_user_id': self.env.user.id,
                        'won_lost_date': time.strftime(TIME_FORMAT)
                        })
            selected_lines = self.line_ids_c.filtered(lambda l: l.is_select)
            self.line_ids_c = [(6, 0, selected_lines.ids)]

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

        if self.next_followup_date and self.next_followup_date <= fields.Date.today():
            vals['readonly_flag'] = True
        return super(CtSalesLead, self).write(vals)

    def  get_default_mail_ids(self, **kw):
        mail_ids = {}
        trans_rec = self.env[CT_SALES_LEAD].search([('id', '=', kw.get('trans_id', False))])

        if trans_rec and trans_rec.user_id.email:
            mail_ids['email_to'] = [trans_rec.confirm_user_id.email]

        return mail_ids
    
    def sales_lead_mail_data_design(self, **kw):
        self.env.cr.execute(
                "SELECT ctm_sales_lead_confirm_mail(%s, %s, %s, %s)",
                (self.id, self.status, self.name or self.draft_name, self.env.user.partner_id.name)
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
                mail_type=mail_type, model_name=CT_SALES_LEAD, mail_name=mail_config_name)

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
        trans_rec = self.env[CT_SALES_LEAD]
        
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


class CtSalesLeadServiceDetailsWizard(models.TransientModel):
    _name = 'ct.sales.lead.service.details.wizard'
    _description = 'Service Details Wizard'

    header_id = fields.Many2one(CT_SALES_LEAD, string="Header Ref", index=True, required=True, ondelete='cascade', c_rule=True)
    line_ids = fields.One2many('ct.sales.lead.service.details.wizard.line', 'header_id', string="Enquiry Details", copy=True, c_rule=True)

    @api.model
    def default_get(self, fields_list):
        res = super(CtSalesLeadServiceDetailsWizard, self).default_get(fields_list)
        lead_id = self.env.context.get('active_id')
        if lead_id:
            lead = self.env[CT_SALES_LEAD].browse(lead_id)
            res['header_id'] = lead.id
            service_lines = [
                (0, 0, {
                    'is_select': line.is_select,
                    'service_id': line.service_id.id,
                    'status': 'won',
                    'rej_remark_id': line.rej_remark_id.id,
                    'lost_remark': line.lost_remark,
                    'details_id': line.id,
                }) for line in lead.line_ids_c if line.is_select
            ]
            res['line_ids'] = service_lines
        return res

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
        status_list = []
        min_list = []
        min_char = int(
            self.env[IR_CONFIG_PARAMETER].sudo().get_param('custom_properties.min_char_length', default=0)
        )
        for line in self.line_ids:
            service_name = line.service_id.name
            if not line.status:
                status_list.append(service_name)
            elif line.status == 'lost' and (not line.lost_remark or len(line.lost_remark.strip()) < min_char):
                min_list.append(service_name)
        if status_list:
            warning_msg.append(f"Please select a status to proceed. Reference: {','.join(status_list)}")
        if min_list:
            warning_msg.append(f"Minimum {min_char} characters are must for lost remarks. Ref : {','.join(min_list)}")

        return self.display_warnings(warning_msg, kw)

    def wizard_submit_button(self):
        self.validations()
        lead_line = []
        is_won = False

        if all(line.status == 'new_lead' for line in self.line_ids):
            raise UserError("All services cannot be selected as a lead.")
        for line in self.line_ids:
            if line.status == 'won':
                self.enquiry_creation(line.details_id)
                is_won = True
            elif line.status == 'new_lead':
                lead_line.append(line.details_id)

            line.details_id.write({
                'status': line.status,
                'rej_remark_id': line.rej_remark_id.id if line.status == 'lost' else False,
                'lost_remark': line.lost_remark if line.status == 'lost' else False,
            })

        if lead_line:
            self.lead_creation(self.header_id, lead_line)

        self.header_id.line_ids_c.filtered(lambda v: v.is_select is not True).unlink()
        self.header_id.write({
                'status': 'won' if is_won else 'lost',
                'progress_status': 'enquiry_draft' if is_won else 'lost',
                'won_lost_user_id': self.env.user.id,
                'won_lost_date': time.strftime(TIME_FORMAT),
                'tat': (datetime.now() - self.header_id.confirm_date).days
                })

    def enquiry_creation(self, line):
        lead = line.header_id
        draft_enq = self.env['ct.enquiry'].create({
            'bkg_party_id' : lead.customer_id.id if lead.customer_type == 'existing' else False,
            'new_bkg_party' : lead.customer_name if lead.customer_type == 'new' else False,
            'service_id' : line.service_id.id if line.service_id else False,
            'service_ids' : lead.service_ids,
            'enq_source_id' : lead.enq_source_id.id if lead.enq_source_id else False,
            'contact_person' : lead.contact_person,
            'tank_qty' : line.tank_count if line.tank_count > 0 else 1,
            'mobile_no' : lead.mobile_no,
            'email' : lead.email,
            'sales_lead_id' : lead.id,
            'lead_remark' : lead.remarks,
            'entry_mode' : 'auto',
            'product' : lead.product,
            'sds_attach_ids': lead.product_sds_ids,
            'generated_user_id': lead.sales_exec_user_id.id if lead.sales_exec_user_id else False

        })
        draft_enq.onchange_service_ids()


    def lead_creation(self, lead, lead_line):
        draft_rec = self.env[CT_SALES_LEAD].create({
            'customer_type' : lead.customer_type,
            'customer_id' : lead.customer_id.id if lead.customer_id else False,
            'customer_name' : lead.customer_name,
            'lead_type' : lead.lead_type,
            'contact_person' : lead.contact_person,
            'mobile_no' : lead.mobile_no,
            'email' : lead.email,
            'address' : lead.address,
            'enq_source_id' : lead.enq_source_id.id,
            'service_ids': [(6, 0, lead.service_ids.ids)],
            'sales_exec_user_id' : lead.sales_exec_user_id.id,
            'sec_sales_exec_user_id' : lead.sec_sales_exec_user_id.id,
            'product' : lead.product,
            'product_sds_ids': [(6, 0, lead.product_sds_ids.ids)],
            'last_followup_date' : lead.last_followup_date,
            'feedback' : lead.feedback,
            'next_followup_date' : lead.next_followup_date,
            'remarks':f"This lead created by auto. Ref - {lead.name}",
            'sales_lead_id' : lead.id,
            'country_id': lead.country_id.id,
            'bus_vert_id': lead.bus_vert_id.id,
            'customer_type_ids': [(6, 0, lead.customer_type_ids.ids)],
            'appointment_type': lead.appointment_type,
            'customer_division': lead.customer_division,
            'designation': lead.designation,
            'entry_mode' : 'auto'
        })
        line_vals = [
            {
                'header_id': draft_rec.id,
                'is_select': line.is_select,
                'service_id': line.service_id.id,
                'tank_count': line.tank_count,
                'business_value': line.business_value,
                'product_name': line.product_name,
                'pol': line.pol,
                'pod': line.pod,
                'currency_id': line.currency_id.id,
            }
            for line in lead_line
        ]
        log_vals = [
            {
                'header_id': draft_rec.id,
                'remarks': line.remarks,
                'next_followup_date': line.next_followup_date,
                'user_id': line.user_id.id,
                'crt_date': line.crt_date
            }
            for line in lead.line_ids
        ]
        if log_vals:
            draft_rec.line_ids.create(log_vals)

        if line_vals:
            draft_rec.line_ids_c.create(line_vals)

        contacts_line_vals = [
            {
                'header_id': draft_rec.id,
                'contact_person': line.contact_person,
                'designation': line.designation,
                'dep_name': line.dep_name,
                'work_location': line.work_location,
                'mobile_no': line.mobile_no,
                'whatsapp_no': line.whatsapp_no,
                'phone_no': line.phone_no,
                'email': line.email,
                'skype': line.skype,
            }
            for line in lead.line_ids_b
        ]
        if contacts_line_vals:
            draft_rec.line_ids_b.create(contacts_line_vals)

        draft_rec.entry_confirm()

    class CtSalesLeadServiceDetailsWizardLine(models.TransientModel):
        _name = 'ct.sales.lead.service.details.wizard.line'
        _description = 'Service Details Wizard Line'
        _order = 'status'

        header_id = fields.Many2one(CT_SALES_LEAD_SERVICE_DETAILS_WIZARD, string="Header Ref")
        is_select = fields.Boolean(string="Select")
        service_id = fields.Many2one(CM_SERVICE, string="Service Name", copy=False, ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
        status = fields.Selection(selection=CUSTOM_WIZARD_STATUS, string="Status")
        rej_remark_id = fields.Many2one('cm.rejection.remark', string="Rejection Remark", ondelete='restrict', domain=[('status', '=', 'active'),('active_trans', '=', True)])
        lost_remark = fields.Text(string="Lost Remarks", copy=False)
        details_id = fields.Many2one('ct.sales.lead.service.details.line', string="Details")

    @api.onchange('status')
    def onchange_status(self):
        self.rej_remark_id = False
        self.lost_remark = False
