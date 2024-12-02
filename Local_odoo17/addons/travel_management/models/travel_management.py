# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import time
from odoo.exceptions import UserError


class travel_management(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _name = 'travel_management.travel_management'
    _description = 'Travel Management'

    ### Guest Info ###
    name = fields.Char('Travel No')
    customer_name = fields.Char('Customer Name')
    customer_mail = fields.Char('Email ID')
    customer_mobile = fields.Char('Mobile')
    customer_address = fields.Text('Address')
    booked_date = fields.Date('Booked Date')
    
    ### Booking Info ###
    package_id = fields.Many2one('travel_package_master.travel_package_master', 'Package Code', tracking=True)
    package_name = fields.Char('Package Name')
    allowed_guest = fields.Char('Allowed Guest')
    no_of_guest = fields.Integer('No of Guest', default='1')
    allowed_days = fields.Char('Allowed Days')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    pkg_amt_per_person = fields.Float('Package amount(Person)')
    total_amount = fields.Float('Total Amount')
    attachment_ids = fields.Many2many('ir.attachment', 'm2m_travel_management_attachment', 'travel_id',
                                      'attachment_id', string='Attachments', help='Attachments related to this record')
    attachment_char = fields.Char('Attachment2')
    
    state = fields.Selection([('draft', 'Draft'),('confirmed', 'Confirmed'),
        ('validate', 'Validated'),('payment_request', 'Payment Pending'),
        ('payment_received', 'Payment Received'),('approved', 'Booked'),
        ('reject', 'Reject'),('wf_cancel', 'WF Cancel'),('cancel', 'Cancelled'),('closed', 'Closed')
            ], string='Status', readonly=True, default='draft', tracking=True)
    reject_remark = fields.Text('Reject Remark')
    cancel_remark = fields.Text('Cancel Remark')
    verification_remark = fields.Text('Verification Remark')
    
    ## Child Tables Declaration
    line_ids = fields.One2many(
        'ch_guest_details.ch_guest_details',
        'header_id',
        'Child Table', readonly=True)
    
    ### Feedback ###
    rating = fields.Selection([('0', '0'),('1', '1'),
                                ('2', '2'), ('3', '3'),
                                ('4', '4'), ('5', '5')], string='Rating', default='5')
    feedback_url = fields.Char('Feedback URL', default='https://docs.google.com/forms/d/e/1FAIpQLSd65ocalqVdNTv7FFJBCGHvUFfNPK_5EUvBaFdGXHsvVmxOLw/viewform?usp=sf_link')
    feedback = fields.Text('Feedback')
    feedback_done = fields.Boolean('Feedback Done', default=False)
    

    ### Customer Bank Details ###
    initial_cancel = fields.Boolean('Initial Cancel', default=False)
    cus_payment_option = fields.Selection([('bank', 'Bank'),('upi', 'UPI')], string='Payment Refund Option', default='bank')
    cus_account_no = fields.Char('Account No')
    cus_bank = fields.Char('Bank')
    cus_account_holder_name =  fields.Char('Account Holder Name')
    cus_branch_name =  fields.Char('Branch Name')
    cus_bank_ifsc_code =  fields.Char('IFSC Code')
    cus_upi_id =  fields.Char('UPI Id')
    cancelled_by = fields.Selection([('customer', 'Customer'),('organizer', 'Organizer')], string='Cancelled by')
    cancellation_fee = fields.Float('Cancellation Fee(20%)')
    refund_amount = fields.Float('Refund Amount')
    refund_status = fields.Boolean('Refund Success', default=False, tracking=True)
    refund_attachment = fields.Many2many('ir.attachment', 'm2m_refund_attachment', 'tr_refund_id',
                                      'refund_id', string='Refund Ref')


    ###  Payment Details ###
    payment_type = fields.Selection([
        ('send', 'Send'),
        ('receive', 'Receive'),
    ], string='Payment Type', default='receive')
    payment_date = fields.Date('Date')
    payment_mode = fields.Selection([
        ('bank', 'Bank'),
        ('upi', 'UPI'),
        # ~ ('cash', 'Cash'),
        # ~ ('card', 'Card')
    ], string='Payment Received Mode')
    payment_received_amount = fields.Float('Received Amount')
    payment_attachment = fields.Many2many('ir.attachment', 'm2m_payment_attachment', 'tr_pay_id',
                                      'payment_id', string='Payment Ref')
	
    
    ### Entry Info ###
    company_id = fields.Many2one(
        'res.company',
        'Company Name',
        readonly=True,
        default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', store=True
    )
    active = fields.Boolean('Active', default=True)
    # ~ is_booked = fields.Boolean('Booked', default=False)
    user_id = fields.Many2one(
        'res.users',
        'Created By',
        readonly=True,
        default=lambda self: self.env.user.id)
    crt_date = fields.Datetime(
        'Created Date',
        readonly=True,
        default=lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'))
    confirm_date = fields.Datetime('Confirmed Date', readonly=True)
    confirm_user_id = fields.Many2one(
        'res.users', 'Confirmed By', readonly=True)
    validated_date = fields.Datetime('Validated Date', readonly=True)
    validated_user_id = fields.Many2one(
        'res.users', 'Validated By', readonly=True)
    payment_req_date = fields.Datetime('Payment requested Date', readonly=True)
    payment_req_user_id = fields.Many2one(
        'res.users', 'Payment requested By', readonly=True)
    payment_rec_date = fields.Datetime('Payment received Date', readonly=True)
    payment_rec_user_id = fields.Many2one(
        'res.users', 'Payment received By', readonly=True)
    approved_date = fields.Datetime('Approved Date', readonly=True)
    approved_user_id = fields.Many2one(
        'res.users', 'Approved By', readonly=True)
    rejected_date = fields.Datetime('Rejected Date', readonly=True)
    rejected_user_id = fields.Many2one(
        'res.users', 'Rejected By', readonly=True)
    cancel_date = fields.Datetime('Cancelled Date', readonly=True)
    cancel_user_id = fields.Many2one(
        'res.users', 'Cancelled By', readonly=True)
    update_date = fields.Datetime('Last Updated Date', readonly=True)
    update_user_id = fields.Many2one(
        'res.users', 'Last Updated By', readonly=True)

    def validations(self, **kw):
        if not self.line_ids or (self.line_ids and (int(self.no_of_guest) != len(self.line_ids))):
            raise UserError("Guest details is must.")
        
        if self.state == 'confirmed':
            if len([line.id for line in self.line_ids if line.verified]) != len(self.line_ids):
                raise UserError('Guest verification is pending.')

    @api.onchange('package_id')
    def onchange_package_id(self):
        if self.package_id:
            self.package_name = self.package_id.name
            self.allowed_guest = self.package_id.max_guest
            self.allowed_days = self.package_id.max_days
            self.pkg_amt_per_person = self.package_id.pkg_amount
    
    @api.onchange('package_id','no_of_guest','from_date','to_date', 'cancelled_by')
    def onchange_total_amount(self):
        if self.package_id and self.no_of_guest and self.from_date and self.to_date:
            self.total_amount = self.no_of_guest * (int(self.package_id.pkg_amount) * int((self.to_date - self.from_date).days+1))
            if self.cancelled_by:
                self.cancellation_fee = (self.total_amount * (20/100)) if self.cancelled_by == 'customer' else 0 if self.cancelled_by == 'organizer' else 0
                self.refund_amount = self.total_amount - self.cancellation_fee
    
    def entry_confirm(self):
        """ entry_confirm """
        if self.state == 'draft':
            self.validations()
            tmp = self.env['travel_package_master.travel_package_master'].search([('id', '=', 16)])
            import threading
            import time
            def temp():
                i = 0
                while i < 7:
                    i +=1
                    print(tmp,"##################",i)
                    tmp.reject_remark = i
                    time.sleep(1)
            
            tmp2 = self.env['organizer_bank_details.organizer_bank_details'].search([('id', '=', 4)])

            def temp2():
                j = 0
                while j < 7:
                    j +=1
                    print(tmp2,"@@@@@@@@@@@@@@@@@@",j)
                    tmp2.reject_remark = j
                    time.sleep(1)
            
            start_time = time.time()
            # Create two threads
            thread1 = threading.Thread(target=temp)
            thread2 = threading.Thread(target=temp2)

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait for both threads to finish
            thread1.join()
            thread2.join()
            end_time = time.time()

            print("Total execution time:", end_time - start_time, "seconds")

            self.write({'state': 'confirmed',
                        'confirm_user_id': self.env.user.id,
                        'confirm_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def entry_validate(self):
        """ entry_validate """
        if self.state == 'confirmed':
            self.validations()
            self.write({'state': 'validate',
                        'validated_user_id': self.env.user.id,
                        'validated_date': time.strftime('%Y-%m-%d %H:%M:%S')})
            
            # pagination # 
            self.env.context = dict(self.env.context, active_id=self.id)
            pkg = self.env['travel_package_master.travel_package_master'].create(
                            {
                                'name': 'Test',
                                'description': 'Tesing purpose',
                                'starting_point': 'JPT',
                                'max_guest':10,
                                'pkg_amount':1000,
                                'code':'TST',
                                'max_days':20,
                                'pkg_amount':20000})
            return {
                'name': 'Travel Package Master',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'travel_package_master.travel_package_master',
                'res_id': pkg.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                # Pass the context to the action to return to the PI form
                'context': self.env.context,
            }
            
        return True
    
    def entry_payment_request(self, **kw):
        """ entry_payment_request """
        if self.state == 'validate':
            if kw.get('send_mail'):
                template = self.env.ref('travel_management.payment_request_mail')
                template.send_mail(self.id, force_send=True)
                self.write({'state': 'payment_request',
                            'payment_req_user_id': self.env.user.id,
                            'payment_req_date': time.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                ir_model_data = self.env['ir.model.data']
                template_id = ir_model_data._xmlid_lookup('travel_management.payment_request_mail')[1]
                try:
                    compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
                except ValueError:
                    compose_form_id = False

                ctx = dict(self.env.context or {})
                ctx.update({
                    'default_model': 'travel_management.travel_management',
                    'default_res_ids': self.ids,
                    'default_template_id': template_id,
                    #'default_composition_mode': 'comment',
                    #'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
                    'force_email': True,
                    'mark_payment_as_sent': True
                })

                return {
                    'name': _('Compose Email'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(compose_form_id, 'form')],
                    'view_id': compose_form_id,
                    'target': 'new',
                    'context': ctx
                }

        return True
    
    def entry_payment_received(self):
        """ entry_payment_received """
        if self.state == 'payment_request':
            if (self.payment_received_amount != self.total_amount) or  (int(self.payment_received_amount) <= 0):
                raise UserError("Full payment not yet done.")
            self.write({'state': 'payment_received',
                        'payment_rec_user_id': self.env.user.id,
                        'payment_rec_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def entry_approve(self):
        """ entry_approve """
        if self.state == 'payment_received':
            self.name = self.env['ir.sequence'].next_by_code('travel_management.travel_management', sequence_date=False) or '/'
            self.write({'state': 'approved',
                        'booked_date':time.strftime('%Y-%m-%d'),
                        'approved_user_id': self.env.user.id,
                        'approved_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def entry_reject(self):
        """ entry_reject """
        if self.state in ('confirmed','validate','payment_request'):
            if not self.reject_remark:
                raise UserError("Reject remark is must.")
            self.write({'state': 'reject',
                        'rejected_user_id': self.env.user.id,
                        'rejected_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def entry_initial_cancel(self):
        """ entry_initial_cancel """
        self.initial_cancel = True
        self.state= 'wf_cancel'

        return True
    
    def entry_cancel(self):
        """ entry_cancel """
        if self.initial_cancel ==  True and self.refund_status == True and self.state in ('wf_cancel','payment_received','approved'):
            if not self.cancel_remark:
                raise UserError("Cancel remark is must.")
            self.write({'state': 'cancel',
                        'cancel_user_id': self.env.user.id,
                        'cancel_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def entry_refund(self):
        """ entry_refund """
        self.refund_status = True

        return True
    
    def entry_feedback(self):
        """ entry_feedback """
        if not self.feedback:
            raise UserError("Feedback is must")
        self.feedback_done = True

        return True


    def unlink(self):
        """ Unlink Funtion """
        for rec in self:
            if rec.state not in ('draft'):
                raise UserError('Warning, You can not delete this entry')
            if rec.state in ('draft'):
                models.Model.unlink(rec)
        return True

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'update_user_id': self.env.user.id})
        return super(travel_management, self).write(vals)
    
    
    ### subtypes for messaging log using tracking=True ###
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'confirmed':
            return self.env.ref('travel_management.tr_confirmed')
        if 'state' in init_values and self.state == 'validate':
            return self.env.ref('travel_management.tr_validate')
        if 'state' in init_values and self.state == 'payment_request':
            return self.env.ref('travel_management.tr_payment_request')
        if 'state' in init_values and self.state == 'payment_received':
            return self.env.ref('travel_management.tr_payment_received')
        if 'state' in init_values and self.state == 'approved':
            return self.env.ref('travel_management.tr_payment_approved')
        if 'state' in init_values and self.state == 'reject':
            return self.env.ref('travel_management.tr_payment_reject')
        if 'refund_status' in init_values and self.refund_status == True:
            return self.env.ref('travel_management.tr_payment_refund')
        if 'state' in init_values and self.state == 'wf_cancel':
            return self.env.ref('travel_management.tr_payment_wf_cancel')
        if 'state' in init_values and self.state == 'cancel':
            return self.env.ref('travel_management.tr_payment_cancel')
        return super(travel_management, self)._track_subtype(init_values)
    
    def print_booking_details(self):
        return self.env.ref('travel_management.action_report_travel_management').report_action(self)

    ### Wizard write action ###
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_payment_as_sent'):
            self.filtered(lambda o: o.state == 'validate').write({'state': 'payment_request','payment_req_user_id': self.env.user.id,'payment_req_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        tr_ctx = {'mail_post_autofollow': self.env.context.get('mail_post_autofollow', True)}
        return super(travel_management, self.with_context(**tr_ctx)).message_post(**kwargs)
    
    def _get_bank_details_to_report(self):
        return self.env['organizer_bank_details.organizer_bank_details'].search([('name','=',self.company_id.id)],limit=1)
    
    def close_state_update_via_cron(self):
        booked_datas =  self.env['travel_management.travel_management'].search([('state','=','approved'),('to_date','<',time.strftime('%Y-%m-%d'))])
        for data in booked_datas:
            data.state = 'closed'


class ch_guest_details(models.Model):
    """ Guest Details """
    _name = "ch_guest_details.ch_guest_details"
    _description = "Guest Details"

    header_id = fields.Many2one('travel_management.travel_management', string='Travel Management', index=True, ondelete='cascade')

    state = fields.Selection([('draft', 'Draft'),('confirmed', 'Confirmed'),
        ('validate', 'Validated'),('payment_request', 'Payment Pending'),
        ('payment_received', 'Payment Received'),('approved', 'Booked'),
        ('reject', 'Reject')
            ], string='Status', readonly=True, related='header_id.state', store='True')

    name = fields.Char('Guest Name')
    age = fields.Integer('Age')
    sex = fields.Selection([('male','Male'),('female','Female'),('others','Others')], 'Sex')
    mobile_no = fields.Char('Mobile No')
    email = fields.Char('Email', size=256)
    aadhar_no = fields.Char('Aadhar No')
    passport_no = fields.Char('Passport No')
    images = fields.Many2many('ir.attachment', 'm2m_guest_passport_attachment', 'guest_id',
                                      'passport_id', string='Aadhar/Passport Image')
    verified = fields.Boolean('Verified', default=False)
