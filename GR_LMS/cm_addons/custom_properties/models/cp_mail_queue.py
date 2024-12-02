from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,date,timedelta
import time
from odoo.exceptions import UserError
import base64
import os
import smtplib
import logging
from odoo import tools

_logger = logging.getLogger(__name__)

CP_MAIL_QUEUE = 'cp.mail.queue'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CUSTOM_STATUS = [('pending', 'Pending'),
                 ('sent', 'Sent')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

class CpMailQueue(models.Model):
    _name = 'cp.mail.queue'
    _description = 'Mail Queue'
    _order = 'crt_date desc'

    name = fields.Char('Name', index=True, copy=False)
    mail_from = fields.Char('From')
    mail_to = fields.Char('To')
    mail_cc = fields.Char('Cc')
    mail_bcc = fields.Char('Bcc')
    subject = fields.Char('Subject')
    body = fields.Html('Body', sanitize=False)
    sent_time = fields.Datetime('Sent Time')
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True, copy=False, default='pending')
    transaction_id = fields.Integer('Transaction ID')
    
    # Child table declaration
    line_ids = fields.One2many('cp.mail.queue.line', 'header_id', string='Mail Queue Lines', copy=True)

    ### Entry Info ###
    active = fields.Boolean(string="Visible", default=True)
    entry_mode = fields.Selection(selection=ENTRY_MODE, string="Entry Mode", readonly=True, copy=False,
                                  tracking=True, default='manual')
    company_id = fields.Many2one('res.company', required=True, copy=False,
                      readonly=True, default=lambda self: self.env.company, ondelete='restrict')
    user_id = fields.Many2one(RES_USERS, string="Created By", readonly=True, copy=False,
                                    ondelete='restrict', default=lambda self: self.env.user.id)
    crt_date = fields.Datetime(string="Creation Date", readonly=True, copy=False, default=fields.Datetime.now)
    update_user_id = fields.Many2one(RES_USERS, string="Last Update By", readonly=True, copy=False,
                                    ondelete='restrict')
    update_date = fields.Datetime(string="Last Update Date", readonly=True, copy=False)


    def batch_send_mail(self, **kw):
        """Batch send mail function"""

        if self.env.context.get('active_ids'):
            self.send_mail(queue_id=self.env.context.get('active_ids'))

        return True

    def process_email_attachments(self, que_rec):
        """Process email attachments and return a list of tuples containing attachment data."""
        attachment = []
        mimetype = None
        for attach_line in que_rec.line_ids:
            for ir_att in attach_line.attachment:
                if ir_att.store_fname:
                    filestore_path = self.env['ir.attachment']._filestore()
                    file_path = os.path.join(filestore_path, ir_att.store_fname)
                    if file_path:
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                            file_data = base64.b64encode(file_data).decode('utf-8')
                            mimetype = ir_att.mimetype or mimetype
                            attachment.append((ir_att.name, base64.b64decode(file_data), mimetype))
        return attachment

    def build_and_send_email(self, ir_mail_server, que_rec, attachment):
        """Build and send an email based on the queue record and attachments."""
        email_from = que_rec.mail_from
        email_to = que_rec.mail_to or ' '
        email_cc = que_rec.mail_cc or ' '
        email_bcc = que_rec.mail_bcc or ' '

        if email_to != ' ' or email_cc != ' ' and que_rec.body:
            msg = ir_mail_server.build_email(
                email_from=email_from,
                email_to=[email_to],
                subject=que_rec.subject,
                attachments=attachment,
                body=que_rec.body,
                body_alternative=tools.html2plaintext(que_rec.body),
                email_cc=[email_cc],
                email_bcc=[email_bcc],
                reply_to=email_cc,
                object_id=que_rec.id and ('%s-%s' % (que_rec.id, CP_MAIL_QUEUE)),
                subtype='html',
                subtype_alternative='plain'
            )

            ir_mail_server.send_email(msg, mail_server_id=1)
            que_rec.write({'status': 'sent', 'sent_time': time.strftime(TIME_FORMAT)})

    def handle_email_failure(self, exception, que_rec):
        """Handle email sending failure and log it to failure history."""
        additional_info = f"Ref: Mail Queue Id - {str(que_rec.id)} and Subject - {str(que_rec.subject)}"
        error_message = f"{str(exception)}\n\n{additional_info}"
        self.env['failure.history'].create({
            'name': 'Send Mail',
            'error': error_message,
        })

    def send_queued_emails(self, que_search):
        """Main function to send queued emails."""
        if que_search:
            ir_mail_server = self.env['ir.mail_server']
            for que_rec in que_search:
                try:
                    attachment = self.process_email_attachments(que_rec)
                    self.build_and_send_email(ir_mail_server, que_rec, attachment)
                except Exception as exception:
                    self.handle_email_failure(exception, que_rec)

        return True

    def send_mail(self, **kw):
        """Send mail function."""
        today = date.today()

        queue_id = kw.get('queue_id')
        if not queue_id:
            context = self._context.copy() or {}
            queue_id = [context.get("queue_id", False)]

        if queue_id and (queue_id[0] if isinstance(queue_id, list) else True):
            que_search = self.search(
                [('id', 'in', queue_id if isinstance(queue_id, list) else [queue_id]), ('status', '=', 'pending')]
            )
        else:
            que_search = self.search(
                [('status', '=', 'pending'), ('crt_date', '>=', today),
                ('crt_date', '<', today + timedelta(days=1))]
            )

        return self.send_queued_emails(que_search)

    def create_mail_queue(self, **kw):
        """Mail Queue"""

        name = kw.get('name', '')
        trans_rec = kw.get('trans_rec', '')
        mail_from = kw.get('mail_from', '') or 'erp-support@kggroup.in'
        email_to = kw.get('email_to', '')
        email_cc = kw.get('email_cc', '')
        email_bcc = kw.get('email_bcc', '')
        subject = kw.get('subject', '')
        body = kw.get('body', '')
        attachment = kw.get('attachment', False)
           
        if name and email_to and subject and body:

            queue_id = self.env[CP_MAIL_QUEUE].create(
                {
                    'name': name,
                    'crt_date': time.strftime(TIME_FORMAT),
                    'company_id': trans_rec.company_id.id if trans_rec and hasattr(trans_rec, 'company_id') else self.env.company.id,
                    'mail_from':mail_from,
                    'mail_to': email_to,
                    'mail_cc': email_cc,
                    'mail_bcc': email_bcc,
                    'transaction_id': trans_rec.id if trans_rec else False,
                    'subject': subject,
                    'body': body,
                    'entry_mode':'auto'})

            if queue_id and attachment and isinstance(attachment, models.BaseModel) and attachment._name == 'ir.attachment':
                for attach in attachment:
                    self.env['cp.mail.queue.line'].create(
                                        {'header_id': queue_id.id, 'attachment': attach})
            return queue_id

        return True

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CpMailQueue, self).write(vals)
