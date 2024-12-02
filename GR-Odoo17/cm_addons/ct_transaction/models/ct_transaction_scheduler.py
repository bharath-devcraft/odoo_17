# -*- coding: utf-8 -*-

from odoo import models, fields

class CtTransactionScheduler(models.Model):
    _name = 'ct.transaction.scheduler'
    _description = 'Transaction Scheduler'

    def custom_scheduler_mail(self):
        mail_name = "Custom Scheduler Mail"

        approved_count = self.env['ct.transaction'].search_count([('status', '=', 'approved'),('ap_rej_date', '>=', fields.Date.today())])

        if approved_count > 0:
            self.env.cr.execute(
                """select csm_template()""")
            data = self.env.cr.fetchall()
            
            subject = '#Today Approved Transactions#'
            
            if data[0][0]:
                mail_type='scheduler'
                mail_config_name='Custom Scheduler Mail'
                vals = self.env['cp.mail.configuration'].mail_config_mailids_data(mail_type=mail_type,mail_name=mail_config_name)

                email_to = ", ".join(vals.get('email_to', [])) if vals.get('email_to') else ''
                email_cc = ", ".join(vals.get('email_cc', [])) if vals.get('email_cc') else ''
                email_bcc = ", ".join(vals.get('email_bcc', [])) if vals.get('email_bcc') else ''
                email_from = ", ".join(vals.get('email_from', [])) if vals.get('email_from') else ''
                self.env['cp.mail.queue'].create_mail_queue(
                    name = mail_name, trans_rec = self, mail_from = email_from,
                    email_to = email_to, email_cc = email_cc, email_bcc = email_bcc,
                    subject = subject, body = data[0][0])
        return True
