
import time
import logging
from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import Counter
from dateutil.relativedelta import relativedelta


_logger = logging.getLogger(__name__)

class CpPopupNotification(models.Model):
    _name = 'cp.popup.notification'
    _description = 'Custom Popup Notification'

    name = fields.Char('Purpose', index=True, copy=False)
    entry_date = fields.Date(string="Entry Date", copy=False, default=fields.Date.today)
    user_id = fields.Many2one('res.users', string="User Name")
    
    def unlink(self):
        """ Unlink """
        for rec in self:
            models.Model.unlink(rec)
        return True

    def write(self, vals):
        """ write """
        return super(CpPopupNotification, self).write(vals)

    def notify_popup(self):
        """ Sends through the bus the next popup of given partners
            Transaction delivery notifications """

        today = fields.Date.today()
        trans_rec = self.env['ct.transaction']
        upcoming_deliveries = trans_rec.search([
            ('status', '=', 'approved'),
            ('delivery_date', '>', today),
            ('delivery_date', '<=', today + timedelta(days=5))
        ])
        
        missed_deliveries = trans_rec.search([
            ('status', '=', 'approved'),
            ('delivery_date', '<', today),
            ('delivery_date', '>=', today - timedelta(days=5))
        ])

        def aggregate_notifications(deliveries):
            user_transactions = {}
            for transaction in deliveries:
                user_id = transaction.ap_rej_user_id
                name = transaction.name or  ''
                if user_id not in user_transactions:
                    user_transactions[user_id] = []
                user_transactions[user_id].append(name)
            return {
                user_id: ', '.join(names)
                for user_id, names in user_transactions.items()
            }

        upcoming_trans_data = aggregate_notifications(upcoming_deliveries)
        missed_trans_data = aggregate_notifications(missed_deliveries)

        notifications = []

        notify_rec = self.env['cp.popup.notification']
        today_date = date.today()

        for user,rec_value in upcoming_trans_data.items():
            notify_rec_name = 'Transaction Upcoming Delivery'
            notif_exist_record = notify_rec.search([
                ('name', '=', notify_rec_name),
                ('user_id', '=', user.id),
                ('entry_date', '=', today_date)
            ], limit=1)
            
            if not notif_exist_record:
            
                message = 'Reminder: The following transaction has an upcoming delivery date : %s' % (rec_value)
                notif = [{
                        'user_id': user.id, 
                        'title': 'Upcoming Delivery',
                        'message': message,
                        'timer': -8420,
                        'notify_at':'2024-07-17 06:29:00',
                        'notify_name': notify_rec_name,
                        'close': 'yes',}]
                notifications.append([user.partner_id, 'custom.notification', notif])
        
        for user,rec_value in missed_trans_data.items():
            notify_rec_name = 'Transaction Overdue Delivery'
            notif_exist_record = notify_rec.search([
                ('name', '=', notify_rec_name),
                ('user_id', '=', user.id),
                ('entry_date', '=', today_date)
            ], limit=1)

            if not notif_exist_record:

                message = 'Alert: The following transactions have overdue delivery dates: %s' % (rec_value)
                notif = [{
                        'user_id': user.id,
                        'title': 'Overdue Delivery',
                        'message': message,
                        'timer': -8420,
                        'notify_at': '2024-07-17 06:29:00',
                        'notify_name': notify_rec_name,
                        'close': 'no',}]
                notifications.append([user.partner_id, 'custom.notification', notif])

        if len(notifications) > 0:
            self.env['bus.bus']._sendmany(notifications)

    def notification_unlink(self):
        """ Based on daily scheduler entry will be deleted on popup notification table"""
        self.search([('entry_date', '<=', fields.Date.today())]).unlink()

        return True