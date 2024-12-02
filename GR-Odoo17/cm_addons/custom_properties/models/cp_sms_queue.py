from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,date,timedelta
import time
from odoo.exceptions import UserError
from collections import Counter
import requests

CUSTOM_STATUS = [('pending', 'Pending'),
                 ('sent', 'Sent')]

ENTRY_MODE =  [('manual','Manual'),
               ('auto', 'Auto')]

MESSAGE_TYPE =  [('sms', 'SMS'),
                 ('whatsapp', 'WhatsApp')]

CP_SMS_QUEUE = 'cp.sms.queue'
RES_USERS = 'res.users'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class CpSmsQueue(models.Model):
    _name = 'cp.sms.queue'
    _description = 'SMS Queue'
    _order = 'crt_date desc'

    name = fields.Char('Name')
    mobile_no = fields.Char('Mobile No')
    content_text = fields.Text('Text')
    message_type = fields.Selection(selection=MESSAGE_TYPE, string='Type')
    sent_time = fields.Datetime('Sent Time')
    status = fields.Selection(selection=CUSTOM_STATUS, string="Status", readonly=True, store=True, copy=False, default='pending')
    transaction_id = fields.Integer('Transaction ID')

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


    def batch_send_sms(self, **kw):
        """Batch send sms function"""

        if self.env.context.get('active_ids'):
            self.send_sms(queue_id=self.env.context.get('active_ids'))

        return True

    def batch_send_whats_app(self, **kw):
        """Batch send whatsapp function"""

        if self.env.context.get('active_ids'):
            self.send_whatsapp(wp_queue_id=self.env.context.get('active_ids'))

        return True

    def send_single_sms(self, pending_rec):
        """Send a single SMS and return whether it was successful."""
        try:
            url = ''
            response = requests.post(url)
            return response.status_code == 200
        except Exception:
            return False

    def get_pending_sms(self, queue_id):
        """Search for pending SMS records."""
        today = date.today()
        search_domain = [('status', '=', 'pending'), ('message_type', '=', 'sms')]

        if queue_id:
            search_domain.append(('id', 'in', queue_id if isinstance(queue_id, list) else [queue_id]))
        else:
            search_domain.extend([
                ('crt_date', '>=', today),
                ('crt_date', '<', today + timedelta(days=1))
            ])

        return self.search(search_domain)

    def get_queue_id(self, **kw):
        """Retrieve the queue ID based on the context or provided keyword arguments."""
        queue_id = kw.get('queue_id')
        if not queue_id:
            context = self._context.copy() or {}
            queue_id = [context.get("queue_id", False)]
        return queue_id

    def send_sms(self, **kw):
        """Send SMS function."""
        queue_id = self.get_queue_id(**kw)
        pending_search = self.get_pending_sms(queue_id)
        
        if not pending_search:
            return False

        for pending_rec in pending_search:
            if self.send_single_sms(pending_rec):
                pending_rec.write({
                    'status': 'sent',
                    'sent_time': time.strftime(TIME_FORMAT)
                })
            else:
                return False
        
        return True

    def send_single_whatsapp(self, pending_rec):
        """Send a single WhatsApp message and return whether it was successful."""
        try:
            url = ''  # Define the actual WhatsApp service URL here
            response = requests.post(url)
            return response.status_code == 200
        except Exception:
            return False

    def get_pending_whatsapp(self, wp_queue_id):
        """Search for pending WhatsApp records."""
        today = date.today()
        search_domain = [('status', '=', 'pending'), ('message_type', '=', 'whatsapp')]

        if wp_queue_id:
            search_domain.append(('id', 'in', wp_queue_id if isinstance(wp_queue_id, list) else [wp_queue_id]))
        else:
            search_domain.extend([
                ('crt_date', '>=', today),
                ('crt_date', '<', today + timedelta(days=1))
            ])

        return self.search(search_domain)

    def get_wp_queue_id(self, **kw):
        """Retrieve the WhatsApp queue ID based on the context or provided keyword arguments."""
        wp_queue_id = kw.get('wp_queue_id')
        if not wp_queue_id:
            context = self._context.copy() or {}
            wp_queue_id = [context.get("wp_queue_id", False)]
        return wp_queue_id
    
    def send_whatsapp(self, **kw):
        """Send WhatsApp message function."""
        wp_queue_id = self.get_wp_queue_id(**kw)
        pending_search = self.get_pending_whatsapp(wp_queue_id)
        
        if not pending_search:
            return False

        for pending_rec in pending_search:
            if self.send_single_whatsapp(pending_rec):
                pending_rec.write({
                    'status': 'sent',
                    'sent_time': time.strftime(TIME_FORMAT)
                })
            else:
                return False  # Return False if any WhatsApp message fails to send
        
        return True

    def create_sms_queue(self, **kw):
        """SMS Queue"""
        message_type = kw.get('message_type', '')
        sms_name = kw.get('sms_name', '')
        mobile_no = kw.get('mobile_no', '')
        content_text = kw.get('content_text', '')
        trans_rec = kw.get('trans_rec', '')
        
        if trans_rec and message_type and sms_name and mobile_no and content_text:
            queue_id = self.env[CP_SMS_QUEUE].create(
                {
                    'message_type': message_type,
                    'name': sms_name,
                    'crt_date': time.strftime(TIME_FORMAT),
                    'company_id': trans_rec.company_id.id if trans_rec.company_id else '',
                    'transaction_id': trans_rec.id,
                    'mobile_no': mobile_no,
                    'content_text':content_text,
                    'entry_mode':'auto',
                })
            return queue_id
            
        return True

    def write(self, vals):
        """ write """
        vals.update({'update_date': time.strftime(TIME_FORMAT),
                     'update_user_id': self.env.user.id})
        return super(CpSmsQueue, self).write(vals)