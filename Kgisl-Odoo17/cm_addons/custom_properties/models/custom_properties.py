#-*- coding: utf-8 -*-

import odoo.addons
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError, UserError
import odoo.modules
import os
import time
from datetime import datetime, date
from datetime import timedelta


class CustomProperties(models.Model):
    _name = 'custom.properties'
    _description = 'Custom Properties'

    name = fields.Char()
       
    @api.model
    def auto_execute_psql_procedures(self) -> None:
        """ .sql files in the psql_procedures folder will auto execute while module install/upgrade """
        try:
            for root_folder in odoo.addons.__path__:
                file_list = f"{root_folder}/{self._name.replace('.', '_')}/psql_procedures/"
                for sql_file in [files for files in os.listdir(file_list if os.path.exists(file_list)\
                             else None) if files.endswith(".sql")]:
                    f = odoo.tools.misc.file_path(f'{file_list}/{sql_file}')
                    with odoo.tools.misc.file_open(f) as base_sql_file:
                         self.env.cr.execute(base_sql_file.read())
        except FileNotFoundError:
            raise UserError(f"File not found: '.sql' (provided by module '{self._name}').")

    @api.model
    def auto_execute_psql_triggers(self) -> None:
        """Automatically executes .sql files in the psql_triggers folder during module installation or upgrade."""
        try:
            for root_folder in odoo.addons.__path__:
                self._execute_sql_files(root_folder, 'psql_triggers')
        except FileNotFoundError as e:
            raise UserError(f"File not found: {str(e)} (provided by module '{self._name}').")
        except Exception as e:
            raise UserError(f"An error occurred during the execution of SQL files: {str(e)}")

    def _execute_sql_files(self, root_folder: str, subfolder: str) -> None:
        """Helper method to execute all .sql files in a given subfolder."""
        sql_folder = os.path.join(root_folder, self._name.replace('.', '_'), subfolder)
        if not os.path.exists(sql_folder):
            return

        for sql_file in os.listdir(sql_folder):
            if sql_file.endswith(".sql"):
                sql_file_path = tools.misc.file_path(os.path.join(sql_folder, sql_file))
                with tools.misc.file_open(sql_file_path) as base_sql_file:
                    self.env.cr.execute(base_sql_file.read())


    @api.model
    def retrieve_allowed_char(self):
        return self.env['ir.config_parameter'].sudo().get_param('custom_properties.skip_chars') or ""

    def _notify_popup(self):
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
